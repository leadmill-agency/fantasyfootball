import fs from "fs";
import path from "path";
import { getAvailableWeeks, getTeamSnapshot } from "./data";

type AdpEntry = { player: string; adp: number | null };

let adpCache: Map<string, number | null> | null = null;

function adpOf(player: string): number | null {
  if (!adpCache) {
    const raw = JSON.parse(
      fs.readFileSync(path.join(process.cwd(), "data", "adp.json"), "utf8")
    );
    adpCache = new Map(
      (raw.players as AdpEntry[]).map((p) => [p.player, p.adp])
    );
  }
  return adpCache.get(player) ?? null;
}

/** Market value proxy, same curve as the grading model. */
function value(adp: number | null): number {
  return adp === null ? 1 : 100 * Math.exp(-0.028 * (adp - 1));
}

export type PositionEdge = {
  position: string;
  a: number;
  b: number;
  winner: "a" | "b" | "even";
};

/**
 * Positional comparison from ADP-derived starter values. Traceable to the
 * ADP source; no editorial judgment involved.
 */
export function comparePositions(
  teamA: string,
  teamB: string
): PositionEdge[] {
  // Use each team's most recent snapshot that carries a roster, so a week
  // whose lineup capture failed falls back to the previous week's lineup.
  const rosterOf = (teamId: string) => {
    for (const w of [...getAvailableWeeks()].reverse()) {
      const r = getTeamSnapshot(teamId, w)?.roster;
      if (r) return r;
    }
    return undefined;
  };
  const rosterA = rosterOf(teamA);
  const rosterB = rosterOf(teamB);
  if (!rosterA || !rosterB) return [];

  const groups = ["QB", "RB", "WR", "TE", "FLEX"];
  const edges: PositionEdge[] = groups.map((g) => {
    const sum = (roster: typeof rosterA) =>
      roster.starters
        .filter((s) => s.slot === g)
        .reduce((acc, s) => acc + value(adpOf(s.player)), 0);
    const a = sum(rosterA);
    const b = sum(rosterB);
    const winner = Math.abs(a - b) < 1 ? "even" : a > b ? "a" : "b";
    return { position: g, a, b, winner };
  });

  const benchSum = (roster: typeof rosterA) =>
    roster.bench.reduce((acc, p) => acc + value(adpOf(p.player)), 0);
  const da = benchSum(rosterA);
  const db = benchSum(rosterB);
  edges.push({
    position: "DEPTH",
    a: da,
    b: db,
    winner: Math.abs(da - db) < 1 ? "even" : da > db ? "a" : "b",
  });
  return edges;
}

import fs from "fs";
import path from "path";
import { getLatestWeek, getTeamSnapshot } from "./data";

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
  const week = getLatestWeek();
  const snapA = getTeamSnapshot(teamA, week);
  const snapB = getTeamSnapshot(teamB, week);
  if (!snapA || !snapB) return [];

  const groups = ["QB", "RB", "WR", "TE", "FLEX"];
  const edges: PositionEdge[] = groups.map((g) => {
    const sum = (snap: typeof snapA) =>
      snap!.roster.starters
        .filter((s) => s.slot === g)
        .reduce((acc, s) => acc + value(adpOf(s.player)), 0);
    const a = sum(snapA);
    const b = sum(snapB);
    const winner = Math.abs(a - b) < 1 ? "even" : a > b ? "a" : "b";
    return { position: g, a, b, winner };
  });

  const benchSum = (snap: typeof snapA) =>
    snap!.roster.bench.reduce((acc, p) => acc + value(adpOf(p.player)), 0);
  const da = benchSum(snapA);
  const db = benchSum(snapB);
  edges.push({
    position: "DEPTH",
    a: da,
    b: db,
    winner: Math.abs(da - db) < 1 ? "even" : da > db ? "a" : "b",
  });
  return edges;
}

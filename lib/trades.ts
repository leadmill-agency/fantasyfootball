import fs from "fs";
import path from "path";
import { z } from "zod";
import { getAvailableResultWeeks, getWeeklyResults } from "./realStandings";

const WeekLineSchema = z.object({
  points: z.number(),
  started: z.boolean(),
});

const ReceivedPlayerSchema = z.object({
  player: z.string(),
  position: z.string(),
  nflTeam: z.string(),
  weeks: z.record(z.string(), WeekLineSchema),
  endedWeek: z.number().optional(),
});

const TradeSideSchema = z.object({
  teamId: z.string(),
  received: z.array(ReceivedPlayerSchema),
});

const TradeSchema = z.object({
  id: z.string(),
  processedAt: z.string(),
  processedWeek: z.number(),
  firstWeek: z.number(),
  vetoes: z.number().nullable(),
  upholds: z.number().nullable(),
  summary: z.string(),
  sides: z.tuple([TradeSideSchema, TradeSideSchema]),
});

const TradesFileSchema = z.object({
  note: z.string().optional(),
  trades: z.array(TradeSchema),
});

export type Trade = z.infer<typeof TradeSchema>;
export type ReceivedPlayer = z.infer<typeof ReceivedPlayerSchema>;

export type SideWeek = { week: number; lineup: number; raw: number };

export type SideLedger = {
  teamId: string;
  received: ReceivedPlayer[];
  weeks: SideWeek[];
  lineupTotal: number;
  rawTotal: number;
  recordSince: { wins: number; losses: number };
  topPlayer?: { player: string; lineup: number };
};

export type TradeLedger = {
  trade: Trade;
  weeks: number[];
  sides: [SideLedger, SideLedger];
  /** Positive = sides[0] ahead on lineup points. */
  lineupGap: number;
  rawGap: number;
  leaderTeamId: string | null;
  /** Rows for a cumulative chart: { week: "Trade"|"W4", [teamId]: cumulative lineup points }. */
  chart: { week: string; [teamId: string]: string | number }[];
};

const r2 = (n: number) => Math.round(n * 100) / 100;

export function getTrades(): Trade[] {
  const file = path.join(process.cwd(), "data", "trades.json");
  if (!fs.existsSync(file)) return [];
  const parsed = TradesFileSchema.parse(JSON.parse(fs.readFileSync(file, "utf8")));
  return parsed.trades;
}

function recordSince(teamId: string, fromWeek: number, throughWeek: number) {
  const rec = { wins: 0, losses: 0 };
  for (const wk of getAvailableResultWeeks()) {
    if (wk < fromWeek || wk > throughWeek) continue;
    const res = getWeeklyResults(wk);
    if (!res) continue;
    for (const m of res.matchups) {
      if (m.homeTeamId === teamId) {
        m.homeScore > m.awayScore ? rec.wins++ : rec.losses++;
      } else if (m.awayTeamId === teamId) {
        m.awayScore > m.homeScore ? rec.wins++ : rec.losses++;
      }
    }
  }
  return rec;
}

/** Build the full ledger for one trade through the latest results week. */
export function buildLedger(trade: Trade): TradeLedger {
  const resultWeeks = getAvailableResultWeeks();
  const latest = resultWeeks.length ? resultWeeks[resultWeeks.length - 1] : trade.firstWeek;
  const weeks: number[] = [];
  for (let w = trade.firstWeek; w <= latest; w++) weeks.push(w);

  const sides = trade.sides.map((side): SideLedger => {
    const perWeek = weeks.map((week) => {
      let lineup = 0;
      let raw = 0;
      for (const p of side.received) {
        if (p.endedWeek !== undefined && week > p.endedWeek) continue;
        const line = p.weeks[String(week)];
        if (!line) continue;
        raw += line.points;
        if (line.started) lineup += line.points;
      }
      return { week, lineup: r2(lineup), raw: r2(raw) };
    });
    const lineupTotal = r2(perWeek.reduce((a, w) => a + w.lineup, 0));
    const rawTotal = r2(perWeek.reduce((a, w) => a + w.raw, 0));
    const top = side.received
      .map((p) => ({
        player: p.player,
        lineup: r2(
          Object.values(p.weeks).reduce((a, l) => a + (l.started ? l.points : 0), 0)
        ),
      }))
      .sort((a, b) => b.lineup - a.lineup)[0];
    return {
      teamId: side.teamId,
      received: side.received,
      weeks: perWeek,
      lineupTotal,
      rawTotal,
      recordSince: recordSince(side.teamId, trade.firstWeek, latest),
      topPlayer: top,
    };
  }) as [SideLedger, SideLedger];

  const lineupGap = r2(sides[0].lineupTotal - sides[1].lineupTotal);
  const rawGap = r2(sides[0].rawTotal - sides[1].rawTotal);
  const leaderTeamId =
    Math.abs(lineupGap) < 0.005 ? null : lineupGap > 0 ? sides[0].teamId : sides[1].teamId;

  const chart: TradeLedger["chart"] = [
    { week: "Trade", [sides[0].teamId]: 0, [sides[1].teamId]: 0 },
  ];
  let c0 = 0;
  let c1 = 0;
  weeks.forEach((w, i) => {
    c0 = r2(c0 + sides[0].weeks[i].lineup);
    c1 = r2(c1 + sides[1].weeks[i].lineup);
    chart.push({ week: `W${w}`, [sides[0].teamId]: c0, [sides[1].teamId]: c1 });
  });

  return { trade, weeks, sides, lineupGap, rawGap, leaderTeamId, chart };
}

export function getTradeLedgers(): TradeLedger[] {
  return getTrades()
    .map(buildLedger)
    .sort((a, b) => b.trade.processedAt.localeCompare(a.trade.processedAt));
}

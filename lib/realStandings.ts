import fs from "fs";
import path from "path";

export type WeeklyMatchup = {
  homeTeamId: string;
  awayTeamId: string;
  homeScore: number;
  awayScore: number;
};

export type WeeklyResults = { week: number; matchups: WeeklyMatchup[] };

export type TeamRecord = { wins: number; losses: number; ties: number };

export type AllPlayRecord = TeamRecord & { winPct: number };

export type RealStanding = {
  teamId: string;
  actualRecord: TeamRecord;
  allPlayRecord: AllPlayRecord;
  expectedWins: number;
  scheduleLuck: number;
  pointsFor: number;
  pointsAgainst: number;
  averageScore: number;
  pfRank: number;
  paRank: number;
};

const RESULTS_DIR = path.join(process.cwd(), "data", "results");

export function getAvailableResultWeeks(): number[] {
  if (!fs.existsSync(RESULTS_DIR)) return [];
  return fs
    .readdirSync(RESULTS_DIR)
    .filter((f) => /^week-\d+\.json$/.test(f))
    .map((f) => Number(f.match(/\d+/)![0]))
    .sort((a, b) => a - b);
}

export function getWeeklyResults(week: number): WeeklyResults | undefined {
  const file = path.join(RESULTS_DIR, `week-${week}.json`);
  if (!fs.existsSync(file)) return undefined;
  return JSON.parse(fs.readFileSync(file, "utf8")) as WeeklyResults;
}

function resultsThrough(throughWeek: number): WeeklyResults[] {
  return getAvailableResultWeeks()
    .filter((w) => w <= throughWeek)
    .map((w) => getWeeklyResults(w)!)
    .filter(Boolean);
}

/** All (teamId, score) pairs for one week. */
export function getWeeklyScores(week: number): { teamId: string; score: number }[] {
  const res = getWeeklyResults(week);
  if (!res) return [];
  return res.matchups.flatMap((m) => [
    { teamId: m.homeTeamId, score: m.homeScore },
    { teamId: m.awayTeamId, score: m.awayScore },
  ]);
}

export function calculateActualRecord(teamId: string, throughWeek: number): TeamRecord {
  const rec = { wins: 0, losses: 0, ties: 0 };
  for (const wk of resultsThrough(throughWeek)) {
    for (const m of wk.matchups) {
      let mine: number | undefined, theirs: number | undefined;
      if (m.homeTeamId === teamId) [mine, theirs] = [m.homeScore, m.awayScore];
      else if (m.awayTeamId === teamId) [mine, theirs] = [m.awayScore, m.homeScore];
      else continue;
      if (mine > theirs) rec.wins++;
      else if (mine < theirs) rec.losses++;
      else rec.ties++;
    }
  }
  return rec;
}

export function calculateAllPlayRecord(teamId: string, throughWeek: number): AllPlayRecord {
  let wins = 0, losses = 0, ties = 0;
  for (const wk of resultsThrough(throughWeek)) {
    const scores = wk.matchups.flatMap((m) => [
      { teamId: m.homeTeamId, score: m.homeScore },
      { teamId: m.awayTeamId, score: m.awayScore },
    ]);
    const mine = scores.find((s) => s.teamId === teamId);
    if (!mine) continue;
    for (const other of scores) {
      if (other.teamId === teamId) continue;
      if (mine.score > other.score) wins++;
      else if (mine.score < other.score) losses++;
      else { wins += 0.5; losses += 0.5; ties++; }
    }
  }
  const total = wins + losses;
  return { wins, losses, ties, winPct: total > 0 ? wins / total : 0 };
}

export function calculateExpectedWins(teamId: string, throughWeek: number): number {
  const games = calculateActualRecordGames(teamId, throughWeek);
  return calculateAllPlayRecord(teamId, throughWeek).winPct * games;
}

function calculateActualRecordGames(teamId: string, throughWeek: number): number {
  const r = calculateActualRecord(teamId, throughWeek);
  return r.wins + r.losses + r.ties;
}

export function calculateScheduleLuck(teamId: string, throughWeek: number): number {
  const actual = calculateActualRecord(teamId, throughWeek);
  return actual.wins + actual.ties * 0.5 - calculateExpectedWins(teamId, throughWeek);
}

export function calculatePointsFor(teamId: string, throughWeek: number): number {
  let pf = 0;
  for (const wk of resultsThrough(throughWeek))
    for (const m of wk.matchups) {
      if (m.homeTeamId === teamId) pf += m.homeScore;
      if (m.awayTeamId === teamId) pf += m.awayScore;
    }
  return pf;
}

export function calculatePointsAgainst(teamId: string, throughWeek: number): number {
  let pa = 0;
  for (const wk of resultsThrough(throughWeek))
    for (const m of wk.matchups) {
      if (m.homeTeamId === teamId) pa += m.awayScore;
      if (m.awayTeamId === teamId) pa += m.homeScore;
    }
  return pa;
}

export function calculateRealStandings(teamIds: string[], throughWeek: number): RealStanding[] {
  const rows = teamIds.map((teamId) => {
    const actualRecord = calculateActualRecord(teamId, throughWeek);
    const allPlayRecord = calculateAllPlayRecord(teamId, throughWeek);
    const expectedWins = calculateExpectedWins(teamId, throughWeek);
    const games = actualRecord.wins + actualRecord.losses + actualRecord.ties;
    const pointsFor = calculatePointsFor(teamId, throughWeek);
    return {
      teamId,
      actualRecord,
      allPlayRecord,
      expectedWins,
      scheduleLuck: calculateScheduleLuck(teamId, throughWeek),
      pointsFor,
      pointsAgainst: calculatePointsAgainst(teamId, throughWeek),
      averageScore: games > 0 ? pointsFor / games : 0,
      pfRank: 0,
      paRank: 0,
    };
  });
  const byPf = [...rows].sort((a, b) => b.pointsFor - a.pointsFor);
  const byPa = [...rows].sort((a, b) => a.pointsAgainst - b.pointsAgainst);
  for (const r of rows) {
    r.pfRank = byPf.findIndex((x) => x.teamId === r.teamId) + 1;
    r.paRank = byPa.findIndex((x) => x.teamId === r.teamId) + 1;
  }
  return rows.sort(
    (a, b) =>
      b.expectedWins - a.expectedWins ||
      b.allPlayRecord.winPct - a.allPlayRecord.winPct ||
      b.pointsFor - a.pointsFor ||
      b.actualRecord.wins - a.actualRecord.wins
  );
}

export type SwapWeek = {
  week: number;
  myScore: number;
  opponentId: string;
  opponentScore: number;
  result: "W" | "L" | "T";
  selfNote: boolean;
};

/**
 * Team A takes Team B's schedule. In a week where B's opponent was A itself,
 * the two swap seats, so A faces B's actual score (marked selfNote).
 */
export function calculateScheduleSwap(
  teamAId: string,
  teamBId: string,
  throughWeek: number
): { weeks: SwapWeek[]; record: TeamRecord } {
  const weeks: SwapWeek[] = [];
  const record = { wins: 0, losses: 0, ties: 0 };
  for (const wk of resultsThrough(throughWeek)) {
    const scores = new Map<string, number>();
    let bOpponent: string | undefined;
    for (const m of wk.matchups) {
      scores.set(m.homeTeamId, m.homeScore);
      scores.set(m.awayTeamId, m.awayScore);
      if (m.homeTeamId === teamBId) bOpponent = m.awayTeamId;
      if (m.awayTeamId === teamBId) bOpponent = m.homeTeamId;
    }
    const myScore = scores.get(teamAId);
    if (myScore === undefined || bOpponent === undefined) continue;
    const selfNote = bOpponent === teamAId;
    const opponentId = selfNote ? teamBId : bOpponent;
    const opponentScore = scores.get(opponentId)!;
    let result: "W" | "L" | "T";
    if (myScore > opponentScore) { result = "W"; record.wins++; }
    else if (myScore < opponentScore) { result = "L"; record.losses++; }
    else { result = "T"; record.ties++; }
    weeks.push({ week: wk.week, myScore, opponentId, opponentScore, result, selfNote });
  }
  return { weeks, record };
}

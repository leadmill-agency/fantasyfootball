import fs from "fs";
import path from "path";
import {
  WeeklySnapshotSchema,
  TeamsFileSchema,
  DraftFileSchema,
  DraftGradesFileSchema,
  type WeeklySnapshot,
  type WeeklyTeamSnapshot,
  type Team,
  type TeamGrade,
  type WeekId,
} from "./schemas";

const DATA_DIR = path.join(process.cwd(), "data");

function readJson(rel: string) {
  return JSON.parse(fs.readFileSync(path.join(DATA_DIR, rel), "utf8"));
}

let cache: {
  teams?: Team[];
  weeks?: Map<string, WeeklySnapshot>;
  grades?: TeamGrade[];
  gradedAsOf?: string;
  draftDate?: string;
} = {};

export function getTeams(): Team[] {
  if (!cache.teams) {
    cache.teams = TeamsFileSchema.parse(readJson("teams.json")).teams;
  }
  return cache.teams;
}

export function getTeam(teamId: string): Team | undefined {
  return getTeams().find((t) => t.teamId === teamId);
}

function loadWeeks(): Map<string, WeeklySnapshot> {
  if (!cache.weeks) {
    const dir = path.join(DATA_DIR, "weeks");
    cache.weeks = new Map();
    for (const file of fs.readdirSync(dir).filter((f) => f.endsWith(".json"))) {
      const snap = WeeklySnapshotSchema.parse(
        JSON.parse(fs.readFileSync(path.join(dir, file), "utf8"))
      );
      cache.weeks.set(String(snap.week), snap);
    }
  }
  return cache.weeks;
}

/** Weeks in chronological order: preseason, 1, 2, ... */
export function getAvailableWeeks(): WeekId[] {
  const keys = [...loadWeeks().keys()];
  const nums = keys
    .filter((k) => k !== "preseason")
    .map(Number)
    .sort((a, b) => a - b);
  return keys.includes("preseason") ? ["preseason", ...nums] : nums;
}

export function getLatestWeek(): WeekId {
  const weeks = getAvailableWeeks();
  return weeks[weeks.length - 1];
}

export function getWeekSnapshot(week: WeekId): WeeklySnapshot | undefined {
  return loadWeeks().get(String(week));
}

export function getTeamSnapshot(
  teamId: string,
  week: WeekId
): WeeklyTeamSnapshot | undefined {
  return getWeekSnapshot(week)?.teams.find((t) => t.teamId === teamId);
}

/** Every snapshot for a team, chronological. Powers charts + season story. */
export function getTeamHistory(
  teamId: string
): { week: WeekId; snapshot: WeeklyTeamSnapshot }[] {
  return getAvailableWeeks()
    .map((week) => ({ week, snapshot: getTeamSnapshot(teamId, week) }))
    .filter((x): x is { week: WeekId; snapshot: WeeklyTeamSnapshot } =>
      Boolean(x.snapshot)
    );
}

export function getDraftGrades(): { gradedAsOf: string; teams: TeamGrade[] } {
  if (!cache.grades) {
    const parsed = DraftGradesFileSchema.parse(readJson("draft-grades.json"));
    cache.grades = parsed.teams;
    cache.gradedAsOf = parsed.gradedAsOf;
  }
  return { gradedAsOf: cache.gradedAsOf!, teams: cache.grades! };
}

export function getTeamGrade(teamId: string): TeamGrade | undefined {
  return getDraftGrades().teams.find((t) => t.teamId === teamId);
}

export function getDraft() {
  return DraftFileSchema.parse(readJson("draft.json"));
}

type ScheduleFile = {
  regularSeasonWeeks: number;
  playoffWeeks: number[];
  weeks: Record<string, { away: string; home: string }[]>;
};

let scheduleCache: ScheduleFile | undefined;

export function getSchedule(): ScheduleFile {
  if (!scheduleCache) {
    scheduleCache = JSON.parse(
      fs.readFileSync(path.join(DATA_DIR, "schedule.json"), "utf8")
    ) as ScheduleFile;
  }
  return scheduleCache;
}

export function getTeamSchedule(
  teamId: string
): { week: number; opponentId: string; site: "home" | "away" }[] {
  const schedule = getSchedule();
  const rows: { week: number; opponentId: string; site: "home" | "away" }[] = [];
  for (const [week, games] of Object.entries(schedule.weeks)) {
    for (const g of games) {
      if (g.home === teamId)
        rows.push({ week: Number(week), opponentId: g.away, site: "home" });
      else if (g.away === teamId)
        rows.push({ week: Number(week), opponentId: g.home, site: "away" });
    }
  }
  return rows.sort((a, b) => a.week - b.week);
}

export function parseWeekParam(param: string | undefined): WeekId {
  if (!param) return getLatestWeek();
  if (param === "preseason") return "preseason";
  const n = Number(param);
  if (Number.isInteger(n) && getAvailableWeeks().includes(n)) return n;
  return getLatestWeek();
}

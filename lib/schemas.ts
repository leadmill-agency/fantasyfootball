import { z } from "zod";

export const RosterPlayerSchema = z.object({
  player: z.string(),
  position: z.string(),
  nflTeam: z.string(),
});

export const StarterSchema = RosterPlayerSchema.extend({
  slot: z.string(),
});

export const WeeklyTeamSnapshotSchema = z.object({
  teamId: z.string(),
  powerRank: z.number(),
  previousPowerRank: z.number().optional(),
  powerScore: z.number(),
  titleOdds: z.number(),
  titleOddsAmerican: z.string(),
  playoffOdds: z.number(),
  draftGrade: z.string(),
  tier: z.string().optional(),
  archetype: z.string().optional(),
  ceilingRank: z.number().optional(),
  record: z.object({ wins: z.number(), losses: z.number() }).optional(),
  pointsFor: z.number().optional(),
  headline: z.string(),
  verdict: z.string(),
  analysis: z.string(),
  stockUp: z.string().optional(),
  stockDown: z.string().optional(),
  biggestDevelopment: z.string().optional(),
  nextMatchup: z.string().optional(),
  movementReasons: z
    .array(z.object({ delta: z.number(), reason: z.string() }))
    .optional(),
  roster: z.object({
    starters: z.array(StarterSchema),
    bench: z.array(RosterPlayerSchema),
  }),
});

export const WeeklySnapshotSchema = z.object({
  week: z.union([z.number(), z.literal("preseason")]),
  publishedAt: z.string(),
  deck: z.string(),
  teams: z.array(WeeklyTeamSnapshotSchema),
});

export const TeamSchema = z.object({
  teamId: z.string(),
  teamName: z.string(),
  manager: z.string(),
  draftSlot: z.number(),
});

export const TeamsFileSchema = z.object({
  season: z.number(),
  league: z.string(),
  teams: z.array(TeamSchema.loose()),
});

export const DraftPickSchema = z.object({
  overall: z.number(),
  round: z.number(),
  pickInRound: z.number(),
  player: z.string(),
  nflTeam: z.string(),
  position: z.string(),
  teamId: z.string(),
  teamName: z.string(),
});

export const DraftFileSchema = z.object({
  season: z.number(),
  draftDate: z.string(),
  type: z.string(),
  rounds: z.number(),
  draftOrder: z.array(z.string()),
  picks: z.array(DraftPickSchema),
});

export const GradedPickSchema = z.object({
  round: z.number(),
  pickInRound: z.number(),
  overall: z.number(),
  player: z.string(),
  position: z.string(),
  nflTeam: z.string(),
  adp: z.number().nullable(),
  adpDiff: z.number().nullable(),
  grade: z.string().nullable(),
  comment: z.string().optional(),
});

export const TeamGradeSchema = z.object({
  teamId: z.string(),
  rank: z.number(),
  grade: z.string(),
  score: z.number(),
  components: z.object({
    valueVsAdp: z.number(),
    starters: z.number(),
    ceiling: z.number(),
    construction: z.number(),
    bench: z.number(),
  }),
  constructionNotes: z.array(z.string()),
  verdict: z.string(),
  picks: z.array(GradedPickSchema),
});

export const DraftGradesFileSchema = z.object({
  season: z.number(),
  gradedAsOf: z.string(),
  teams: z.array(TeamGradeSchema),
});

export type WeeklySnapshot = z.infer<typeof WeeklySnapshotSchema>;
export type WeeklyTeamSnapshot = z.infer<typeof WeeklyTeamSnapshotSchema>;
export type Team = z.infer<typeof TeamSchema>;
export type DraftPick = z.infer<typeof DraftPickSchema>;
export type TeamGrade = z.infer<typeof TeamGradeSchema>;
export type GradedPick = z.infer<typeof GradedPickSchema>;
export type WeekId = number | "preseason";

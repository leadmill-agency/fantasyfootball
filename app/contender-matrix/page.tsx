import type { Metadata } from "next";
import {
  getAvailableWeeks,
  getTeams,
  getWeekSnapshot,
  parseWeekParam,
} from "@/lib/data";
import { publishedDate, weekLabel } from "@/lib/format";
import WeekSelector from "@/components/rankings/WeekSelector";
import MatrixPlot, { type MatrixPoint } from "@/components/matrix/MatrixPlot";

export const metadata: Metadata = {
  title: "Contender Matrix",
  description:
    "Who is strong now versus dangerous later. Current strength rank against championship ceiling rank, week over week.",
};

export default async function ContenderMatrixPage({
  searchParams,
}: {
  searchParams: Promise<{ week?: string }>;
}) {
  const week = parseWeekParam((await searchParams).week);
  const snapshot = getWeekSnapshot(week);
  const teams = getTeams();
  const weeks = getAvailableWeeks();
  if (!snapshot) return null;

  const prevIndex = weeks.findIndex((w) => String(w) === String(week)) - 1;
  const prev = prevIndex >= 0 ? getWeekSnapshot(weeks[prevIndex]) : undefined;

  const points: MatrixPoint[] = snapshot.teams
    .filter((t) => t.ceilingRank !== undefined)
    .map((t) => {
      const meta = teams.find((m) => m.teamId === t.teamId);
      const before = prev?.teams.find((p) => p.teamId === t.teamId);
      return {
        teamId: t.teamId,
        teamName: meta?.teamName ?? t.teamId,
        manager: meta?.manager ?? "",
        strengthRank: t.powerRank,
        ceilingRank: t.ceilingRank!,
        strengthDelta: before ? before.powerRank - t.powerRank : undefined,
        ceilingDelta:
          before?.ceilingRank !== undefined
            ? before.ceilingRank - t.ceilingRank!
            : undefined,
        tier: t.tier,
        archetype: t.archetype,
        titleOdds: t.titleOdds,
        draftGrade: t.draftGrade,
      };
    });

  return (
    <div className="pt-10 sm:pt-14 pb-8">
      <div className="eyebrow text-accent">Contender Matrix</div>
      <h1 className="font-display text-5xl sm:text-7xl leading-[0.92] mt-3">
        Strong Now vs Dangerous Later
      </h1>
      <p className="font-condensed font-medium mt-5 text-xl sm:text-2xl text-ink-soft max-w-[640px] leading-snug">
        Every team plotted on two questions: how good is the roster today, and
        how scary is its best December version?
      </p>

      <details className="mt-5 max-w-[640px]">
        <summary className="eyebrow text-accent cursor-pointer">
          How to read this ↓
        </summary>
        <div className="font-data text-sm text-ink-soft mt-3 leading-relaxed space-y-2">
          <p>
            <strong className="text-ink">Horizontal — Current Strength
            Rank (1–12).</strong> The Power Ranking this week. Right is
            stronger. This moves weekly with results and roster quality.
          </p>
          <p>
            <strong className="text-ink">Vertical — Championship Ceiling
            Rank (1–12).</strong> A separate ranking of each roster&apos;s best
            realistic December outcome. Higher is scarier. It moves with
            trades, breakouts, injuries, and role changes — never with one
            loud scoring week.
          </p>
          <p>
            Both are ranks on purpose. Nobody has to pretend a roster is an
            &quot;87.9.&quot;
          </p>
        </div>
      </details>

      <p className="font-data text-xs text-ink-faint mt-4 mb-6">
        {weekLabel(week)} board · Updated {publishedDate(snapshot.publishedAt)}
      </p>

      <WeekSelector weeks={weeks} selected={week} />

      <MatrixPlot points={points} />
    </div>
  );
}

import type { Metadata } from "next";
import { getLatestWeek, getTeams, getWeekSnapshot } from "@/lib/data";
import { publishedDate, weekLabel } from "@/lib/format";
import MatrixPlot, { type MatrixPoint } from "@/components/matrix/MatrixPlot";

export const metadata: Metadata = {
  title: "Contender Matrix",
  description:
    "Who is strong now versus dangerous later. Current strength against championship ceiling, ranks only.",
};

export default function ContenderMatrixPage() {
  const week = getLatestWeek();
  const snapshot = getWeekSnapshot(week);
  const teams = getTeams();
  if (!snapshot) return null;

  const points: MatrixPoint[] = snapshot.teams
    .filter((t) => t.ceilingRank !== undefined)
    .map((t) => {
      const meta = teams.find((m) => m.teamId === t.teamId);
      return {
        teamId: t.teamId,
        teamName: meta?.teamName ?? t.teamId,
        manager: meta?.manager ?? "",
        strengthRank: t.powerRank,
        ceilingRank: t.ceilingRank!,
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
        Current strength against championship ceiling. Ranks, not vibes — and
        deliberately not fake-precision percentages.
      </p>
      <p className="font-data text-xs text-ink-faint mt-4 mb-8">
        {weekLabel(week)} board · Updated {publishedDate(snapshot.publishedAt)}{" "}
        · Ceiling ranks from the preseason analysis; they move with trades,
        breakouts, and injuries — not with one loud scoring week.
      </p>

      <MatrixPlot points={points} />
    </div>
  );
}

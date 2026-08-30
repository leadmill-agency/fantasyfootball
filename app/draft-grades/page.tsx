import type { Metadata } from "next";
import { getDraftGrades, getTeams } from "@/lib/data";
import DraftExplorer from "@/components/draft/DraftExplorer";

export const metadata: Metadata = {
  title: "2026 Draft Grades",
  description:
    "Graded with information available on August 29, 2026. Frozen forever. No hindsight.",
};

export default function DraftGradesPage() {
  const { gradedAsOf, teams: grades } = getDraftGrades();
  const teams = getTeams();

  return (
    <div className="pt-10 sm:pt-14 pb-8">
      <div className="eyebrow text-accent">Draft Grades</div>
      <h1 className="font-display text-5xl sm:text-7xl leading-[0.92] mt-3">
        2026 Draft Grades
      </h1>
      <p className="font-condensed font-medium mt-5 text-xl sm:text-2xl text-ink-soft max-w-[620px] leading-snug">
        Graded using information available on August 29, 2026. These grades are
        frozen. If your C+ team wins the title, the C+ stays.
      </p>
      <p className="font-data text-xs text-ink-faint mt-4 mb-8">
        Pick prices: ESPN Live Draft Results, retrieved {gradedAsOf} — the
        platform this league drafts on. Team grades were computed before the
        ADP-source correction and stay frozen. Unranked players are shown
        without ADP, never invented.
      </p>

      <DraftExplorer
        grades={grades}
        meta={teams.map((t) => ({
          teamId: t.teamId,
          teamName: t.teamName,
          manager: t.manager,
        }))}
      />
    </div>
  );
}

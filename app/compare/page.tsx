import type { Metadata } from "next";
import { Suspense } from "react";
import {
  getLatestWeek,
  getTeam,
  getTeamGrade,
  getTeams,
  getTeamSnapshot,
} from "@/lib/data";
import { comparePositions } from "@/lib/compare";
import { formatRecord } from "@/lib/format";
import CompareSelector from "@/components/compare/CompareSelector";
import ManagerPortrait from "@/components/teams/ManagerPortrait";

export const metadata: Metadata = {
  title: "Compare Teams",
  description: "Two managers enter. The data decides.",
};

export default async function ComparePage({
  searchParams,
}: {
  searchParams: Promise<{ a?: string; b?: string }>;
}) {
  const { a, b } = await searchParams;
  const teams = getTeams();
  const teamA = a ? getTeam(a) : undefined;
  const teamB = b ? getTeam(b) : undefined;

  return (
    <div className="pt-10 sm:pt-14 pb-8">
      <div className="eyebrow text-accent">Compare</div>
      <h1 className="font-display text-5xl sm:text-7xl leading-[0.92] mt-3 mb-8">
        Head to Head
      </h1>

      <Suspense>
        <CompareSelector
          teams={teams.map((t) => ({ teamId: t.teamId, teamName: t.teamName }))}
          a={teamA?.teamId}
          b={teamB?.teamId}
        />
      </Suspense>

      {teamA && teamB ? (
        <Matchup a={teamA.teamId} b={teamB.teamId} />
      ) : (
        <p className="text-ink-soft text-lg border-t border-rule pt-8">
          Pick two teams. The model has no loyalties, only inputs.
        </p>
      )}
    </div>
  );
}

function Matchup({ a, b }: { a: string; b: string }) {
  const week = getLatestWeek();
  const snapA = getTeamSnapshot(a, week);
  const snapB = getTeamSnapshot(b, week);
  const teamA = getTeam(a)!;
  const teamB = getTeam(b)!;
  const gradeA = getTeamGrade(a);
  const gradeB = getTeamGrade(b);
  if (!snapA || !snapB) return null;

  const edges = comparePositions(a, b);
  const edgesA = edges.filter((e) => e.winner === "a").length;
  const edgesB = edges.filter((e) => e.winner === "b").length;

  const rows: { label: string; a: string; b: string; better?: "a" | "b" }[] = [
    {
      label: "Power rank",
      a: `#${snapA.powerRank}`,
      b: `#${snapB.powerRank}`,
      better: snapA.powerRank < snapB.powerRank ? "a" : "b",
    },
    {
      label: "Power score",
      a: String(snapA.powerScore),
      b: String(snapB.powerScore),
      better: snapA.powerScore > snapB.powerScore ? "a" : "b",
    },
    {
      label: "Title odds",
      a: `${snapA.titleOdds}%`,
      b: `${snapB.titleOdds}%`,
      better: snapA.titleOdds > snapB.titleOdds ? "a" : "b",
    },
    {
      label: "Record",
      a: formatRecord(snapA.record),
      b: formatRecord(snapB.record),
    },
    {
      label: "Draft grade",
      a: gradeA?.grade ?? "—",
      b: gradeB?.grade ?? "—",
      better:
        gradeA && gradeB
          ? gradeA.rank < gradeB.rank
            ? "a"
            : "b"
          : undefined,
    },
  ];

  return (
    <div>
      <div className="grid grid-cols-[1fr_auto_1fr] items-end gap-4 border-t-4 border-rule-strong pt-8 mb-8">
        <div className="flex flex-col items-end gap-3">
          <ManagerPortrait
            teamId={teamA.teamId}
            teamName={teamA.teamName}
            manager={teamA.manager}
            variant="portrait"
            size="lg"
            className="w-[88px] h-[88px] sm:w-[140px] sm:h-[140px]"
          />
          <h2 className="font-display text-3xl sm:text-5xl text-right">
            {teamA.teamName}
          </h2>
        </div>
        <span className="eyebrow text-ink-faint pb-2">vs</span>
        <div className="flex flex-col items-start gap-3">
          <ManagerPortrait
            teamId={teamB.teamId}
            teamName={teamB.teamName}
            manager={teamB.manager}
            variant="portrait"
            size="lg"
            className="w-[88px] h-[88px] sm:w-[140px] sm:h-[140px]"
          />
          <h2 className="font-display text-3xl sm:text-5xl">
            {teamB.teamName}
          </h2>
        </div>
      </div>

      <div className="max-w-[640px] mx-auto">
        {rows.map((r) => (
          <div
            key={r.label}
            className="grid grid-cols-[1fr_auto_1fr] items-baseline gap-4 border-b border-rule py-3"
          >
            <span
              className={`font-data text-lg text-right ${
                r.better === "a" ? "font-bold" : "text-ink-soft"
              }`}
            >
              {r.a}
            </span>
            <span className="eyebrow text-ink-faint w-28 text-center">
              {r.label}
            </span>
            <span
              className={`font-data text-lg ${
                r.better === "b" ? "font-bold" : "text-ink-soft"
              }`}
            >
              {r.b}
            </span>
          </div>
        ))}

        <div className="mt-10">
          <h3 className="eyebrow text-ink-soft text-center mb-4">
            Positional edges · from market values
          </h3>
          {edges.map((e) => (
            <div
              key={e.position}
              className="grid grid-cols-[1fr_auto_1fr] items-center gap-4 py-2"
            >
              <span
                className={`text-right font-data text-sm ${
                  e.winner === "a"
                    ? "font-bold text-accent"
                    : "text-ink-faint"
                }`}
              >
                {e.winner === "a" ? teamA.teamName : e.winner === "even" ? "even" : ""}
              </span>
              <span className="eyebrow w-28 text-center">{e.position}</span>
              <span
                className={`font-data text-sm ${
                  e.winner === "b"
                    ? "font-bold text-accent"
                    : "text-ink-faint"
                }`}
              >
                {e.winner === "b" ? teamB.teamName : e.winner === "even" ? "even" : ""}
              </span>
            </div>
          ))}
          <p className="font-data text-xs text-ink-faint text-center mt-6">
            Edges: {teamA.teamName} {edgesA} · {teamB.teamName} {edgesB}.
            Computed from ADP-derived starter values, not vibes.
          </p>
        </div>
      </div>
    </div>
  );
}

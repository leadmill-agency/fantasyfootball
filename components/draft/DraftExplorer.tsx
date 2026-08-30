"use client";

import { useState } from "react";
import Link from "next/link";
import type { TeamGrade } from "@/lib/schemas";
import ManagerPortrait from "@/components/teams/ManagerPortrait";
import { signed } from "@/lib/format";

type TeamMeta = { teamId: string; teamName: string; manager: string };
type Mode = "overview" | "picks";

const COMPONENT_LABELS: [keyof TeamGrade["components"], string][] = [
  ["valueVsAdp", "Value"],
  ["starters", "Starters"],
  ["ceiling", "Ceiling"],
  ["construction", "Construction"],
  ["bench", "Bench"],
];

export default function DraftExplorer({
  grades,
  meta,
}: {
  grades: TeamGrade[];
  meta: TeamMeta[];
}) {
  const [mode, setMode] = useState<Mode>("overview");
  const nameOf = (id: string) =>
    meta.find((m) => m.teamId === id)?.teamName ?? id;

  return (
    <section>
      <div role="group" aria-label="View mode" className="flex mb-4 border-2 border-rule-strong w-fit">
        {(
          [
            ["overview", "Overview"],
            ["picks", "Pick by Pick"],
          ] as const
        ).map(([m, label]) => (
          <button
            key={m}
            onClick={() => setMode(m)}
            aria-pressed={mode === m}
            className={`font-condensed font-bold uppercase tracking-[0.06em] text-sm px-4 py-1.5 transition-colors ${
              mode === m
                ? "bg-rule-strong text-paper"
                : "text-ink-soft hover:text-ink"
            }`}
          >
            {label}
          </button>
        ))}
      </div>

      {mode === "overview" ? (
        <ol>
          {grades.map((g) => (
            <li key={g.teamId} className="border-t-2 border-rule-strong last:border-b-2 py-5">
              <div className="flex flex-wrap items-center gap-x-4 gap-y-1">
                <span className="font-display text-4xl leading-[0.9] w-12">
                  {String(g.rank).padStart(2, "0")}
                </span>
                <ManagerPortrait teamId={g.teamId} teamName={nameOf(g.teamId)} size="sm" />
                <Link
                  href={`/team/${g.teamId}`}
                  className="font-display text-2xl hover:text-accent transition-colors"
                >
                  {nameOf(g.teamId)}
                </Link>
                <span className="font-display text-4xl text-accent ml-auto">
                  {g.grade}
                </span>
              </div>
              <div className="sm:pl-[4.25rem] mt-3">
                <div className="flex flex-wrap gap-x-7 gap-y-2 font-data text-xs text-ink-soft">
                  {COMPONENT_LABELS.map(([key, label]) => (
                    <span key={key}>
                      {label}{" "}
                      <strong className="font-condensed font-bold text-ink text-base">
                        {Math.round(g.components[key])}
                      </strong>
                    </span>
                  ))}
                </div>
                <p className="mt-3 text-[15px] leading-relaxed text-ink max-w-[720px]">
                  {g.verdict}
                </p>
              </div>
            </li>
          ))}
        </ol>
      ) : (
        <div>
          {grades.map((g) => (
            <details key={g.teamId} className="border-t-2 border-rule-strong last:border-b-2 group">
              <summary className="flex items-center gap-4 py-4 cursor-pointer list-none [&::-webkit-details-marker]:hidden">
                <span className="font-display text-3xl leading-[0.9] w-12">
                  {String(g.rank).padStart(2, "0")}
                </span>
                <ManagerPortrait teamId={g.teamId} teamName={nameOf(g.teamId)} size="xs" />
                <span className="font-display text-xl">
                  {nameOf(g.teamId)}
                </span>
                <span className="font-display text-2xl text-accent">
                  {g.grade}
                </span>
                <span className="eyebrow text-ink-faint ml-auto group-open:hidden">
                  Open ↓
                </span>
                <span className="eyebrow text-ink-faint ml-auto hidden group-open:inline">
                  Close ↑
                </span>
              </summary>
              <div className="pb-6 sm:pl-14">
                <ol className="space-y-0">
                  {g.picks.map((p) => (
                    <li
                      key={p.overall}
                      className="border-t border-rule/60 py-2.5"
                    >
                      <div className="flex items-baseline gap-3 font-data text-sm">
                        <span className="text-ink-faint w-12 shrink-0 text-xs">
                          {p.round}.{String(p.pickInRound).padStart(2, "0")}
                        </span>
                        <span className="font-semibold min-w-0">
                          {p.player}
                        </span>
                        <span className="text-ink-faint text-xs">
                          {p.position} · {p.nflTeam}
                        </span>
                        <span className="ml-auto text-xs text-ink-soft whitespace-nowrap">
                          {p.adp === null ? (
                            <span className="text-ink-faint">no ADP</span>
                          ) : (
                            <>
                              ADP {p.adp}{" "}
                              <span
                                className={
                                  (p.adpDiff ?? 0) >= 0
                                    ? "text-positive"
                                    : "text-negative"
                                }
                              >
                                {signed(p.adpDiff ?? 0)}
                              </span>
                            </>
                          )}
                        </span>
                        {p.grade && (
                          <span className="font-semibold w-7 text-right">
                            {p.grade}
                          </span>
                        )}
                      </div>
                      {p.comment && (
                        <p className="text-sm italic text-ink-soft mt-1 sm:ml-[3.75rem]">
                          {p.comment}
                        </p>
                      )}
                    </li>
                  ))}
                </ol>
              </div>
            </details>
          ))}
        </div>
      )}
    </section>
  );
}

"use client";

import { useEffect, useState } from "react";
import Link from "next/link";
import type { WeeklyTeamSnapshot } from "@/lib/schemas";
import Movement from "./Movement";
import { formatRecord, signed } from "@/lib/format";

type TeamMeta = { teamId: string; teamName: string; manager: string };
type Mode = "skim" | "deep";

export default function RankingsExplorer({
  teams,
  meta,
}: {
  teams: WeeklyTeamSnapshot[];
  meta: TeamMeta[];
}) {
  const [mode, setMode] = useState<Mode>("skim");
  const [open, setOpen] = useState<Set<string>>(new Set());

  useEffect(() => {
    try {
      const saved = localStorage.getItem("kk-view-mode");
      if (saved === "deep" || saved === "skim") setMode(saved);
    } catch {}
  }, []);

  const setModePersist = (m: Mode) => {
    setMode(m);
    try {
      localStorage.setItem("kk-view-mode", m);
    } catch {}
  };

  const metaOf = (id: string) => meta.find((m) => m.teamId === id);
  const isOpen = (id: string) => mode === "deep" || open.has(id);
  const toggle = (id: string) =>
    setOpen((prev) => {
      const next = new Set(prev);
      if (next.has(id)) next.delete(id);
      else next.add(id);
      return next;
    });

  return (
    <section>
      <div
        role="group"
        aria-label="View mode"
        className="flex mb-4 border-2 border-rule-strong w-fit"
      >
        {(["skim", "deep"] as const).map((m) => (
          <button
            key={m}
            onClick={() => setModePersist(m)}
            aria-pressed={mode === m}
            className={`font-condensed font-bold uppercase tracking-[0.06em] text-sm px-4 py-1.5 transition-colors ${
              mode === m
                ? "bg-rule-strong text-paper"
                : "text-ink-soft hover:text-ink"
            }`}
          >
            {m === "skim" ? "Skim" : "Deep Dive"}
          </button>
        ))}
      </div>

      <ol>
        {teams.map((t) => {
          const m = metaOf(t.teamId);
          const expanded = isOpen(t.teamId);
          return (
            <li key={t.teamId} className="border-t-2 border-rule-strong last:border-b-2">
              <div className="grid grid-cols-[4rem_minmax(0,1fr)] sm:grid-cols-[6rem_minmax(0,1fr)_7.5rem] gap-x-3 sm:gap-x-5 py-5">
                <div className="row-span-2 sm:row-span-1">
                  <span className="font-display text-5xl sm:text-[4.25rem] leading-[0.9] block">
                    {String(t.powerRank).padStart(2, "0")}
                  </span>
                  <div className="mt-1.5 pl-0.5">
                    <Movement current={t.powerRank} previous={t.previousPowerRank} />
                  </div>
                </div>

                <div className="min-w-0">
                  <div className="flex flex-wrap items-baseline gap-x-3 gap-y-0.5">
                    <Link
                      href={`/team/${t.teamId}`}
                      className="font-display text-2xl sm:text-3xl leading-none hover:text-accent transition-colors"
                    >
                      {m?.teamName ?? t.teamId}
                    </Link>
                    <span className="font-condensed font-medium text-sm text-ink-faint uppercase tracking-[0.04em]">
                      {m?.manager}
                    </span>
                    {t.tier && (
                      <span className="font-condensed font-bold text-xs text-accent uppercase tracking-[0.08em]">
                        {t.tier}
                      </span>
                    )}
                  </div>
                  <div className="font-data text-[13px] text-ink-soft mt-2 flex flex-wrap gap-x-4">
                    <span>{formatRecord(t.record)}</span>
                    {t.pointsFor !== undefined && <span>{t.pointsFor} PF</span>}
                    <span>
                      PWR <strong className="text-ink">{t.powerScore}</strong>
                    </span>
                    <span className="sm:hidden">
                      TITLE <strong className="text-ink">{t.titleOdds}%</strong>
                    </span>
                    <span>
                      DRAFT <strong className="text-ink">{t.draftGrade}</strong>
                    </span>
                  </div>
                  <p className="verdict mt-2.5 text-ink">{t.verdict}</p>
                  {!expanded && (
                    <button
                      onClick={() => toggle(t.teamId)}
                      aria-expanded={false}
                      className="font-condensed font-bold uppercase tracking-[0.06em] text-sm text-accent mt-3 hover:underline underline-offset-4"
                    >
                      Read the column ↓
                    </button>
                  )}
                </div>

                <div className="hidden sm:block text-right border-l border-rule pl-4">
                  <div className="eyebrow text-ink-faint">Title odds</div>
                  <div className="font-display text-3xl mt-1">{t.titleOdds}%</div>
                  <div className="font-data text-xs text-ink-faint mt-0.5">
                    {t.titleOddsAmerican}
                  </div>
                </div>
              </div>

              <div
                className={`grid transition-[grid-template-rows] duration-200 ease-out ${
                  expanded ? "grid-rows-[1fr]" : "grid-rows-[0fr]"
                }`}
              >
                <div className="overflow-hidden">
                  <Expansion t={t} onCollapse={() => toggle(t.teamId)} deep={mode === "deep"} />
                </div>
              </div>
            </li>
          );
        })}
      </ol>
    </section>
  );
}

function Expansion({
  t,
  onCollapse,
  deep,
}: {
  t: WeeklyTeamSnapshot;
  onCollapse: () => void;
  deep: boolean;
}) {
  return (
    <div className="pb-8 sm:pl-[6rem] sm:pr-4 max-w-[820px]">
      <h3 className="font-display text-xl sm:text-2xl text-accent mb-3">
        {t.headline}
      </h3>
      <div className="prose-editorial">
        {t.analysis.split("\n\n").map((p, i) => (
          <p key={i}>{p}</p>
        ))}
      </div>

      {t.movementReasons && t.movementReasons.length > 0 && (
        <div className="mt-6 border-t border-rule pt-4">
          <div className="eyebrow text-ink-soft mb-2">Why they moved</div>
          <ul className="font-data text-sm space-y-1">
            {t.movementReasons.map((r, i) => (
              <li key={i} className="flex gap-3">
                <span
                  className={
                    r.delta >= 0 ? "text-positive w-12" : "text-negative w-12"
                  }
                >
                  {signed(r.delta)}
                </span>
                <span>{r.reason}</span>
              </li>
            ))}
          </ul>
        </div>
      )}

      <div className="mt-6 flex flex-wrap gap-x-8 gap-y-3 border-t border-rule pt-4">
        <Metric label="Power score" value={String(t.powerScore)} />
        <Metric label="Title odds" value={`${t.titleOdds}%`} />
        <Metric label="Playoff odds" value={`${t.playoffOdds}%`} />
        <Metric label="Draft grade" value={t.draftGrade} />
        {t.ceilingRank && <Metric label="Ceiling rank" value={`#${t.ceilingRank}`} />}
        {t.archetype && <Metric label="Archetype" value={t.archetype} />}
        {t.stockUp && <Metric label="Stock up" value={t.stockUp} />}
        {t.stockDown && <Metric label="Stock down" value={t.stockDown} />}
        {t.nextMatchup && <Metric label="Next" value={t.nextMatchup} />}
      </div>

      <div className="mt-5 flex gap-6">
        <Link
          href={`/team/${t.teamId}`}
          className="font-condensed font-bold uppercase tracking-[0.06em] text-sm text-accent hover:underline underline-offset-4"
        >
          View team page →
        </Link>
        {!deep && (
          <button
            onClick={onCollapse}
            className="font-condensed font-bold uppercase tracking-[0.06em] text-sm text-ink-faint hover:text-ink"
          >
            Collapse ↑
          </button>
        )}
      </div>
    </div>
  );
}

function Metric({ label, value }: { label: string; value: string }) {
  return (
    <div>
      <div className="eyebrow text-ink-faint">{label}</div>
      <div className="font-condensed font-bold text-lg mt-1">{value}</div>
    </div>
  );
}

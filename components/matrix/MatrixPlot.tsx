"use client";

import { useState } from "react";
import Link from "next/link";
import ManagerPortrait from "@/components/teams/ManagerPortrait";
import { signed } from "@/lib/format";

export type MatrixPoint = {
  teamId: string;
  teamName: string;
  manager: string;
  strengthRank: number;
  ceilingRank: number;
  strengthDelta?: number; // + = improved since last week
  ceilingDelta?: number;
  tier?: string;
  archetype?: string;
  titleOdds: number;
  draftGrade: string;
};

export default function MatrixPlot({ points }: { points: MatrixPoint[] }) {
  const [selected, setSelected] = useState<string | null>(null);
  const sel = points.find((p) => p.teamId === selected);

  // Best strength = right edge; best ceiling = top edge.
  const xPct = (r: number) => ((12 - r) / 11) * 100;
  const yPct = (r: number) => ((r - 1) / 11) * 100;

  return (
    <div>
      <div className="flex gap-2 max-w-[900px]">
        {/* y-axis */}
        <div className="flex flex-col justify-between items-center py-1 w-8 shrink-0">
          <span className="font-data text-[11px] font-semibold text-ink">#1</span>
          <span
            className="font-condensed font-bold uppercase tracking-[0.1em] text-[11px] text-ink-soft"
            style={{ writingMode: "vertical-rl", transform: "rotate(180deg)" }}
          >
            Championship ceiling rank
          </span>
          <span className="font-data text-[11px] font-semibold text-ink-faint">#12</span>
        </div>

        <div className="flex-1 min-w-0">
          <div className="relative border-2 border-rule-strong bg-surface aspect-square sm:aspect-[4/3] w-full">
            <div className="absolute inset-y-0 left-1/2 w-px bg-rule" />
            <div className="absolute inset-x-0 top-1/2 h-px bg-rule" />

            <QuadrantLabel className="top-2 right-2 text-right">
              True Contenders
            </QuadrantLabel>
            <QuadrantLabel className="top-2 left-2">
              Dangerous If It Hits
            </QuadrantLabel>
            <QuadrantLabel className="bottom-2 right-2 text-right">
              Regular-Season Merchants
            </QuadrantLabel>
            <QuadrantLabel className="bottom-2 left-2">
              The Long Season
            </QuadrantLabel>

            {points.map((p) => {
              const moved =
                (p.strengthDelta ?? 0) !== 0 || (p.ceilingDelta ?? 0) !== 0;
              return (
                <button
                  key={p.teamId}
                  onClick={() =>
                    setSelected(selected === p.teamId ? null : p.teamId)
                  }
                  aria-pressed={selected === p.teamId}
                  aria-label={`${p.teamName}: current strength rank ${p.strengthRank}, championship ceiling rank ${p.ceilingRank}`}
                  className={`absolute -translate-x-1/2 -translate-y-1/2 transition-transform ${
                    selected === p.teamId
                      ? "z-20 scale-125"
                      : "z-10 hover:scale-110"
                  }`}
                  style={{
                    left: `${(xPct(p.strengthRank) * 0.86 + 7).toFixed(1)}%`,
                    top: `${(yPct(p.ceilingRank) * 0.82 + 9).toFixed(1)}%`,
                  }}
                >
                  <ManagerPortrait
                    teamId={p.teamId}
                    teamName={p.teamName}
                    manager={p.manager}
                    size="sm"
                    className={selected === p.teamId ? "border-accent" : ""}
                  />
                  {moved && (
                    <span className="absolute -top-1.5 -right-1.5 w-3 h-3 bg-accent border border-paper rounded-full" />
                  )}
                </button>
              );
            })}
          </div>

          {/* x-axis */}
          <div className="flex justify-between items-baseline mt-1.5">
            <span className="font-data text-[11px] font-semibold text-ink-faint">
              #12
            </span>
            <span className="font-condensed font-bold uppercase tracking-[0.1em] text-[11px] text-ink-soft">
              Current strength rank
            </span>
            <span className="font-data text-[11px] font-semibold text-ink">#1</span>
          </div>
        </div>
      </div>

      {sel ? (
        <div className="mt-6 border-2 border-rule-strong bg-surface p-5 max-w-[900px] flex items-center gap-5 flex-wrap">
          <ManagerPortrait
            teamId={sel.teamId}
            teamName={sel.teamName}
            manager={sel.manager}
            variant="portrait"
            size="lg"
          />
          <div className="min-w-0">
            <div className="font-display text-2xl">{sel.teamName}</div>
            <div className="font-condensed font-medium text-sm text-ink-soft uppercase tracking-[0.04em]">
              {sel.manager}
              {sel.archetype ? ` · ${sel.archetype}` : ""}
            </div>
            <div className="font-data text-sm text-ink-soft mt-2 flex flex-wrap gap-x-5 gap-y-1">
              <span>
                Strength <strong className="text-ink">#{sel.strengthRank}</strong>
                <Delta d={sel.strengthDelta} />
              </span>
              <span>
                Ceiling <strong className="text-ink">#{sel.ceilingRank}</strong>
                <Delta d={sel.ceilingDelta} />
              </span>
              <span>
                Title odds <strong className="text-ink">{sel.titleOdds}%</strong>
              </span>
              <span>
                Draft <strong className="text-ink">{sel.draftGrade}</strong>
              </span>
            </div>
            <Link
              href={`/team/${sel.teamId}`}
              className="font-condensed font-bold uppercase tracking-[0.06em] text-sm text-accent mt-2 inline-block hover:underline underline-offset-4"
            >
              Team page →
            </Link>
          </div>
        </div>
      ) : (
        <p className="font-data text-xs text-ink-faint mt-6">
          Tap a face for details. A red dot means that team moved on either
          axis since the previous week.
        </p>
      )}
    </div>
  );
}

function Delta({ d }: { d?: number }) {
  if (!d) return null;
  return (
    <span
      className={`ml-1 text-xs font-semibold ${
        d > 0 ? "text-positive" : "text-negative"
      }`}
    >
      {d > 0 ? `↑${d}` : `↓${-d}`}
    </span>
  );
}

function QuadrantLabel({
  children,
  className,
}: {
  children: React.ReactNode;
  className: string;
}) {
  return (
    <span
      className={`absolute font-condensed font-bold uppercase tracking-[0.08em] text-[11px] text-ink-faint pointer-events-none ${className}`}
    >
      {children}
    </span>
  );
}

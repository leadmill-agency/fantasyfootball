import type { Metadata } from "next";
import Link from "next/link";
import {
  getAvailableWeeks,
  getTeams,
  getWeekSnapshot,
  parseWeekParam,
} from "@/lib/data";
import { publishedDate, signed, weekShort } from "@/lib/format";
import WeekSelector from "@/components/rankings/WeekSelector";
import OddsChart from "@/components/odds/OddsChart";

export const metadata: Metadata = {
  title: "Championship Odds",
  description: "Who actually wins this thing? The championship market, updated weekly.",
};

export default async function OddsPage({
  searchParams,
}: {
  searchParams: Promise<{ week?: string }>;
}) {
  const week = parseWeekParam((await searchParams).week);
  const snapshot = getWeekSnapshot(week);
  const teams = getTeams();
  const weeks = getAvailableWeeks();
  if (!snapshot) return null;

  const ranked = [...snapshot.teams].sort((a, b) => b.titleOdds - a.titleOdds);
  const favorite = ranked[0];
  const longshot = ranked[ranked.length - 1];
  const nameOf = (id: string) =>
    teams.find((t) => t.teamId === id)?.teamName ?? id;

  const prevIndex = weeks.findIndex((w) => String(w) === String(week)) - 1;
  const prev = prevIndex >= 0 ? getWeekSnapshot(weeks[prevIndex]) : undefined;
  const deltaOf = (teamId: string) => {
    const before = prev?.teams.find((t) => t.teamId === teamId)?.titleOdds;
    const now = snapshot.teams.find((t) => t.teamId === teamId)?.titleOdds;
    return before !== undefined && now !== undefined ? now - before : undefined;
  };

  const series = weeks.map((w) => {
    const snap = getWeekSnapshot(w)!;
    const point: { week: string; [teamId: string]: string | number } = {
      week: weekShort(w),
    };
    for (const t of snap.teams) point[t.teamId] = t.titleOdds;
    return point;
  });

  return (
    <div className="pt-10 sm:pt-14 pb-8">
      <div className="eyebrow text-accent">Title Odds</div>
      <h1 className="font-display text-5xl sm:text-7xl leading-[0.92] mt-3">
        The Championship Market
      </h1>
      <p className="font-condensed font-medium mt-5 text-xl sm:text-2xl text-ink-soft max-w-[620px] leading-snug">
        Who actually wins this thing?
      </p>
      <p className="font-data text-xs text-ink-faint mt-4 mb-6">
        Updated {publishedDate(snapshot.publishedAt)} · Probabilities sum to
        100% · Not a sportsbook
      </p>

      <WeekSelector weeks={weeks} selected={week} />

      <div className="grid grid-cols-1 sm:grid-cols-2 border-y-2 border-rule-strong divide-y-2 sm:divide-y-0 sm:divide-x-2 divide-rule-strong mb-4">
        <div className="py-5 sm:pr-8">
          <div className="eyebrow text-ink-faint">Favorite</div>
          <div className="font-display text-3xl mt-2">
            {nameOf(favorite.teamId)}
          </div>
          <div className="font-data text-sm text-ink-soft mt-0.5">
            {favorite.titleOdds}% · {favorite.titleOddsAmerican}
          </div>
        </div>
        <div className="py-5 sm:pl-8">
          <div className="eyebrow text-ink-faint">Longest shot</div>
          <div className="font-display text-3xl mt-2">
            {nameOf(longshot.teamId)}
          </div>
          <div className="font-data text-sm text-ink-soft mt-0.5">
            {longshot.titleOdds}% · {longshot.titleOddsAmerican}
          </div>
        </div>
      </div>

      <OddsChart
        data={series}
        teams={teams.map((t) => ({ teamId: t.teamId, teamName: t.teamName }))}
      />

      <ol>
        {ranked.map((t, i) => {
          const delta = deltaOf(t.teamId);
          return (
            <li
              key={t.teamId}
              className="grid grid-cols-[3rem_minmax(0,1fr)_auto] items-baseline gap-3 border-t-2 border-rule-strong last:border-b-2 py-4"
            >
              <span className="font-display text-3xl leading-none">
                {String(i + 1).padStart(2, "0")}
              </span>
              <span className="min-w-0">
                <Link
                  href={`/team/${t.teamId}`}
                  className="font-display text-xl hover:text-accent transition-colors"
                >
                  {nameOf(t.teamId)}
                </Link>
                {delta !== undefined && delta !== 0 && (
                  <span
                    className={`font-data text-xs ml-3 ${
                      delta > 0 ? "text-positive" : "text-negative"
                    }`}
                  >
                    {signed(delta)}% this week
                  </span>
                )}
              </span>
              <span className="text-right">
                <span className="font-display text-2xl">
                  {t.titleOdds}%
                </span>
                <span className="font-data text-xs text-ink-faint ml-3 hidden sm:inline">
                  {t.titleOddsAmerican}
                </span>
              </span>
            </li>
          );
        })}
      </ol>
    </div>
  );
}

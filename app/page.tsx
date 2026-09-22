import type { Metadata } from "next";
import Link from "next/link";
import {
  getAvailableWeeks,
  getTeams,
  getWeekSnapshot,
  parseWeekParam,
} from "@/lib/data";
import { publishedDate, weekLabel } from "@/lib/format";
import { getWeeklyScores } from "@/lib/realStandings";
import WeekSelector from "@/components/rankings/WeekSelector";
import RankingsExplorer from "@/components/rankings/RankingsExplorer";

export async function generateMetadata({
  searchParams,
}: {
  searchParams: Promise<{ week?: string }>;
}): Promise<Metadata> {
  const week = parseWeekParam((await searchParams).week);
  return {
    title: `${weekLabel(week)} Power Rankings`,
    description:
      "Where you rank, whether you moved, and why. Updated every week.",
  };
}

export default async function PowerRankingsPage({
  searchParams,
}: {
  searchParams: Promise<{ week?: string }>;
}) {
  const week = parseWeekParam((await searchParams).week);
  const snapshot = getWeekSnapshot(week);
  const teams = getTeams();

  if (!snapshot) {
    return (
      <div className="py-24 text-center">
        <p className="font-display text-xl">No rankings for this week yet.</p>
        <Link href="/" className="eyebrow text-accent mt-4 inline-block">
          Back to latest
        </Link>
      </div>
    );
  }

  const nameOf = (teamId: string) =>
    teams.find((t) => t.teamId === teamId)?.teamName ?? teamId;

  const facts: { label: string; team: string; value: string }[] = [];
  if (week !== "preseason") {
    const scores = getWeeklyScores(week);
    if (scores.length > 0) {
      const high = scores.reduce((a, b) => (b.score > a.score ? b : a));
      facts.push({
        label: "Week high",
        team: nameOf(high.teamId),
        value: high.score.toFixed(2),
      });
    }
    const movers = snapshot.teams
      .filter((t) => t.previousPowerRank !== undefined)
      .map((t) => ({ t, d: t.previousPowerRank! - t.powerRank }));
    if (movers.length > 0) {
      const up = movers.reduce((a, b) => (b.d > a.d ? b : a));
      const down = movers.reduce((a, b) => (b.d < a.d ? b : a));
      if (up.d > 0)
        facts.push({
          label: "Biggest riser",
          team: nameOf(up.t.teamId),
          value: `↑${up.d}`,
        });
      if (down.d < 0)
        facts.push({
          label: "Biggest faller",
          team: nameOf(down.t.teamId),
          value: `↓${-down.d}`,
        });
    }
  }
  const favorite = snapshot.teams.find((t) => t.powerRank === 1);
  if (favorite)
    facts.push({
      label: "Title favorite",
      team: nameOf(favorite.teamId),
      value: `${favorite.titleOdds}%`,
    });
  if (week === "preseason") {
    const longest = snapshot.teams.reduce((a, b) =>
      b.titleOdds < a.titleOdds ? b : a
    );
    facts.push({
      label: "Longest shot",
      team: nameOf(longest.teamId),
      value: `${longest.titleOdds}%`,
    });
    const ceiling = snapshot.teams.find((t) => t.ceilingRank === 1);
    if (ceiling)
      facts.push({
        label: "Ceiling No. 1",
        team: nameOf(ceiling.teamId),
        value: `#${ceiling.powerRank}`,
      });
  }

  return (
    <div className="pt-10 sm:pt-14 pb-8">
      <div className="min-[900px]:grid min-[900px]:grid-cols-[minmax(0,1fr)_300px] xl:grid-cols-[minmax(0,1fr)_340px] min-[900px]:gap-10 xl:gap-12 min-[900px]:items-end mb-6">
        <div>
          <div className="eyebrow text-accent">Power Rankings</div>
          <h1 className="font-display text-5xl sm:text-7xl leading-[0.92] mt-3 max-w-[900px]">
            {week === "preseason" ? (
              <>The Preseason Board</>
            ) : (
              <>{weekLabel(week)} Power Rankings</>
            )}
          </h1>
          {snapshot.deck && (
            <p className="font-condensed font-medium mt-5 text-xl sm:text-2xl text-ink-soft max-w-[680px] leading-snug">
              {snapshot.deck}
            </p>
          )}
          <p className="font-data text-xs text-ink-faint mt-4">
            Updated {publishedDate(snapshot.publishedAt)}
          </p>
        </div>

        {facts.length > 0 && (
          <aside className="hidden min-[900px]:block border-2 border-rule-strong bg-surface">
            <div className="eyebrow bg-ink text-paper px-4 py-2.5">
              {week === "preseason" ? "The board in numbers" : "The week in numbers"}
            </div>
            {facts.map((f) => (
              <div
                key={f.label}
                className="flex items-baseline justify-between gap-4 px-4 py-3 border-t-2 border-rule first:border-t-0"
              >
                <div className="min-w-0">
                  <div className="eyebrow text-ink-faint text-[10px]">
                    {f.label}
                  </div>
                  <div className="font-condensed font-bold uppercase tracking-[0.04em] text-sm truncate">
                    {f.team}
                  </div>
                </div>
                <div className="font-display text-2xl shrink-0">{f.value}</div>
              </div>
            ))}
          </aside>
        )}
      </div>

      <WeekSelector weeks={getAvailableWeeks()} selected={week} />

      <RankingsExplorer
        teams={snapshot.teams}
        meta={teams.map((t) => ({
          teamId: t.teamId,
          teamName: t.teamName,
          manager: t.manager,
        }))}
      />

      {snapshot.corrections && (
        <aside className="mt-10 border-2 border-rule-strong bg-surface px-5 py-4 max-w-[760px]">
          <div className="eyebrow text-accent mb-2">Corrections Dept.</div>
          <p className="text-[14px] leading-relaxed">{snapshot.corrections}</p>
        </aside>
      )}

      <div className="mt-10">
        <Link
          href="/compare"
          className="eyebrow text-accent hover:underline underline-offset-4"
        >
          Compare two teams →
        </Link>
      </div>
    </div>
  );
}

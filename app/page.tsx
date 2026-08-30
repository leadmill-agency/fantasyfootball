import type { Metadata } from "next";
import Link from "next/link";
import {
  getAvailableWeeks,
  getTeams,
  getWeekSnapshot,
  parseWeekParam,
} from "@/lib/data";
import { publishedDate, weekLabel } from "@/lib/format";
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

  return (
    <div className="pt-10 sm:pt-14 pb-8">
      <div className="eyebrow text-accent">Power Rankings</div>
      <h1 className="font-display text-5xl sm:text-7xl leading-[0.92] mt-3 max-w-[900px]">
        {week === "preseason" ? (
          <>The Preseason Board</>
        ) : (
          <>{weekLabel(week)} Power Rankings</>
        )}
      </h1>
      {snapshot.deck && (
        <p className="font-condensed font-medium mt-5 text-xl sm:text-2xl text-ink-soft max-w-[620px] leading-snug">
          {snapshot.deck}
        </p>
      )}
      <p className="font-data text-xs text-ink-faint mt-4 mb-6">
        Updated {publishedDate(snapshot.publishedAt)}
      </p>

      <WeekSelector weeks={getAvailableWeeks()} selected={week} />

      <RankingsExplorer
        teams={snapshot.teams}
        meta={teams.map((t) => ({
          teamId: t.teamId,
          teamName: t.teamName,
          manager: t.manager,
        }))}
      />

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

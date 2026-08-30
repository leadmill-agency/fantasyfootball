import type { Metadata } from "next";
import Link from "next/link";
import { notFound } from "next/navigation";
import {
  getLatestWeek,
  getTeam,
  getTeamGrade,
  getTeamHistory,
  getTeams,
  getTeamSchedule,
  getTeamSnapshot,
} from "@/lib/data";
import { formatRecord, weekLabel } from "@/lib/format";
import Movement from "@/components/rankings/Movement";

export function generateStaticParams() {
  return getTeams().map((t) => ({ slug: t.teamId }));
}

export async function generateMetadata({
  params,
}: {
  params: Promise<{ slug: string }>;
}): Promise<Metadata> {
  const team = getTeam((await params).slug);
  return team
    ? { title: team.teamName, description: `${team.teamName}, managed by ${team.manager}. Rankings, odds, and the season story.` }
    : { title: "Team not found" };
}

export default async function TeamPage({
  params,
}: {
  params: Promise<{ slug: string }>;
}) {
  const { slug } = await params;
  const team = getTeam(slug);
  if (!team) notFound();

  const latest = getLatestWeek();
  const snap = getTeamSnapshot(slug, latest);
  const grade = getTeamGrade(slug);
  const history = getTeamHistory(slug);
  if (!snap) notFound();

  return (
    <div className="pt-10 sm:pt-14 pb-8">
      <div className="grid sm:grid-cols-[minmax(0,1fr)_auto] gap-6 items-end border-b-4 border-rule-strong pb-8">
        <div>
          <div className="eyebrow text-accent">Team Page</div>
          <h1 className="font-display text-5xl sm:text-7xl leading-[0.92] mt-3">
            {team.teamName}
          </h1>
          <p className="font-data text-sm text-ink-soft mt-3">
            Managed by {team.manager} · Drafted from slot {team.draftSlot}
          </p>
          {(team.championships || team.runnerUp) && (
            <p className="font-condensed font-bold uppercase tracking-[0.08em] text-sm mt-2">
              {team.championships && (
                <span className="text-accent">
                  League champion {team.championships.join(", ")}
                </span>
              )}
              {team.championships && team.runnerUp && (
                <span className="text-ink-faint"> · </span>
              )}
              {team.runnerUp && (
                <span className="text-ink-soft">
                  Runner-up {team.runnerUp.join(", ")}
                </span>
              )}
            </p>
          )}
        </div>
        <div className="flex sm:flex-col gap-6 sm:gap-3 sm:text-right">
          <div>
            <div className="eyebrow text-ink-faint">Power rank</div>
            <div className="font-display text-4xl leading-none mt-1">
              #{snap.powerRank}{" "}
              <Movement current={snap.powerRank} previous={snap.previousPowerRank} size="lg" />
            </div>
          </div>
          <div>
            <div className="eyebrow text-ink-faint">Title odds</div>
            <div className="font-display text-2xl">{snap.titleOdds}%</div>
          </div>
          <div>
            <div className="eyebrow text-ink-faint">Draft grade</div>
            <div className="font-display text-2xl text-accent">
              {snap.draftGrade}
            </div>
          </div>
        </div>
      </div>

      <div className="flex flex-wrap gap-x-10 gap-y-4 border-b border-rule py-5">
        <Stat label="Record" value={formatRecord(snap.record)} />
        {snap.pointsFor !== undefined && (
          <Stat label="Points for" value={String(snap.pointsFor)} />
        )}
        <Stat label="Power score" value={String(snap.powerScore)} />
        <Stat label="Playoff odds" value={`${snap.playoffOdds}%`} />
        {grade && <Stat label="Draft score" value={String(grade.score)} />}
      </div>

      <div className="grid lg:grid-cols-[minmax(0,1fr)_320px] gap-12 mt-10">
        <div>
          <h2 className="eyebrow text-ink-soft border-b border-rule pb-2 mb-6">
            Season Story
          </h2>
          {[...history].reverse().map(({ week, snapshot }) => (
            <article key={String(week)} className="mb-12">
              <div className="eyebrow text-accent">{weekLabel(week)}</div>
              <h3 className="font-display text-3xl mt-1 mb-4">
                {snapshot.headline}
              </h3>
              <div className="prose-editorial text-[16px] max-w-[680px]">
                {snapshot.analysis.split("\n\n").map((p, i) => (
                  <p key={i}>{p}</p>
                ))}
              </div>
            </article>
          ))}

          {grade && (
            <div className="border-t border-rule pt-8 mt-4">
              <h2 className="eyebrow text-ink-soft mb-4">
                Draft Verdict · Frozen {`August 29, 2026`}
              </h2>
              <p className="text-[16px] leading-relaxed max-w-[680px]">
                {grade.verdict}
              </p>
              <Link
                href="/draft-grades"
                className="eyebrow text-accent mt-4 inline-block hover:underline underline-offset-4"
              >
                Full draft grades →
              </Link>
            </div>
          )}
        </div>

        <aside>
          <h2 className="eyebrow text-ink-soft border-b border-rule pb-2 mb-4">
            Current Roster
          </h2>
          <div className="eyebrow text-ink-faint mb-2">Starters</div>
          <ul className="mb-6">
            {snap.roster.starters.map((p, i) => (
              <li
                key={i}
                className="flex items-baseline gap-3 py-1.5 border-b border-rule/50 font-data text-sm"
              >
                <span className="text-ink-faint text-xs w-10 shrink-0">
                  {p.slot}
                </span>
                <span className="font-medium">{p.player}</span>
                <span className="text-ink-faint text-xs ml-auto">
                  {p.nflTeam}
                </span>
              </li>
            ))}
          </ul>
          <div className="eyebrow text-ink-faint mb-2">Bench</div>
          <ul>
            {snap.roster.bench.map((p, i) => (
              <li
                key={i}
                className="flex items-baseline gap-3 py-1.5 border-b border-rule/50 font-data text-sm"
              >
                <span className="text-ink-faint text-xs w-10 shrink-0">
                  {p.position}
                </span>
                <span>{p.player}</span>
                <span className="text-ink-faint text-xs ml-auto">
                  {p.nflTeam}
                </span>
              </li>
            ))}
          </ul>
          <Link
            href={`/compare?a=${slug}`}
            className="eyebrow text-accent mt-6 inline-block hover:underline underline-offset-4"
          >
            Compare this team →
          </Link>

          <h2 className="eyebrow text-ink-soft border-b border-rule pb-2 mb-4 mt-10">
            2026 Schedule
          </h2>
          <ul>
            {getTeamSchedule(slug).map((g) => {
              const opp = getTeam(g.opponentId);
              return (
                <li
                  key={g.week}
                  className="flex items-baseline gap-3 py-1.5 border-b border-rule/50 font-data text-sm"
                >
                  <span className="text-ink-faint text-xs w-10 shrink-0">
                    W{g.week}
                  </span>
                  <span className="text-ink-faint text-xs w-5 shrink-0">
                    {g.site === "home" ? "vs" : "at"}
                  </span>
                  <Link
                    href={`/team/${g.opponentId}`}
                    className="hover:text-accent transition-colors"
                  >
                    {opp?.teamName ?? g.opponentId}
                  </Link>
                </li>
              );
            })}
          </ul>
        </aside>
      </div>
    </div>
  );
}

function Stat({ label, value }: { label: string; value: string }) {
  return (
    <div>
      <div className="eyebrow text-ink-faint">{label}</div>
      <div className="font-condensed font-bold text-xl mt-1">{value}</div>
    </div>
  );
}

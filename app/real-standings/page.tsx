import type { Metadata } from "next";
import { getTeams } from "@/lib/data";
import {
  calculateRealStandings,
  getAvailableResultWeeks,
} from "@/lib/realStandings";
import ManagerPortrait from "@/components/teams/ManagerPortrait";
import Link from "next/link";
import { signed } from "@/lib/format";

export const metadata: Metadata = {
  title: "Real Standings",
  description:
    "Your record is what happened. This is what you deserved. All-play records, expected wins, and schedule luck.",
};

export default async function RealStandingsPage({
  searchParams,
}: {
  searchParams: Promise<{ week?: string }>;
}) {
  const weeks = getAvailableResultWeeks();
  const requested = Number((await searchParams).week);
  const through =
    weeks.length === 0
      ? 0
      : weeks.includes(requested)
        ? requested
        : weeks[weeks.length - 1];

  return (
    <div className="pt-10 sm:pt-14 pb-8">
      <div className="eyebrow text-accent">Real Standings</div>
      <h1 className="font-display text-5xl sm:text-7xl leading-[0.92] mt-3 max-w-[900px]">
        Your record is what happened. This is what you deserved.
      </h1>
      <p className="font-condensed font-medium mt-5 text-xl sm:text-2xl text-ink-soft max-w-[640px] leading-snug">
        Every score compared against all eleven other teams, every week. The
        schedule doesn&apos;t get a vote here.
      </p>

      <details className="mt-5 max-w-[640px]">
        <summary className="eyebrow text-accent cursor-pointer">
          How it works ↓
        </summary>
        <p className="font-data text-sm text-ink-soft mt-3 leading-relaxed">
          Each week, every team&apos;s score is compared with all 11 others.
          All-play win percentage is how often you would have beaten the rest
          of the league. Expected wins converts that into a normal record.
          Schedule Luck is actual wins minus expected wins — positive means
          the schedule has been kind, negative means it owes you money.
        </p>
      </details>

      {weeks.length === 0 ? (
        <div className="mt-10 border-2 border-rule-strong bg-surface px-6 py-12 text-center max-w-[760px]">
          <p className="font-display text-2xl">
            Real Standings unlock after Week 1.
          </p>
          <p className="font-data text-sm text-ink-soft mt-3 max-w-[480px] mx-auto">
            No games have been played. Twelve managers are currently tied for
            deserving nothing.
          </p>
          <Link
            href="/"
            className="eyebrow text-accent mt-6 inline-block hover:underline underline-offset-4"
          >
            Preseason board →
          </Link>
        </div>
      ) : (
        <Standings through={through} weeks={weeks} />
      )}
    </div>
  );
}

function Standings({ through, weeks }: { through: number; weeks: number[] }) {
  const teams = getTeams();
  const nameOf = (id: string) =>
    teams.find((t) => t.teamId === id)?.teamName ?? id;
  const managerOf = (id: string) => teams.find((t) => t.teamId === id)?.manager;
  const rows = calculateRealStandings(
    teams.map((t) => t.teamId),
    through
  );

  const bestAllPlay = [...rows].sort(
    (a, b) => b.allPlayRecord.winPct - a.allPlayRecord.winPct
  )[0];
  const luckiest = [...rows].sort((a, b) => b.scheduleLuck - a.scheduleLuck)[0];
  const unluckiest = [...rows].sort((a, b) => a.scheduleLuck - b.scheduleLuck)[0];

  const fmtAp = (r: (typeof rows)[0]) =>
    `${r.allPlayRecord.wins}–${r.allPlayRecord.losses}`;

  return (
    <div className="mt-8">
      <div className="flex gap-5 overflow-x-auto border-y-2 border-rule-strong py-2.5 mb-6 [scrollbar-width:none]">
        {weeks.map((w) => (
          <Link
            key={w}
            href={`/real-standings?week=${w}`}
            className={`font-condensed font-bold uppercase tracking-[0.06em] text-[15px] whitespace-nowrap px-1 ${
              w === through ? "text-accent" : "text-ink-soft hover:text-ink"
            }`}
          >
            W{w}
          </Link>
        ))}
      </div>

      <div className="grid grid-cols-1 sm:grid-cols-3 border-y-2 border-rule-strong divide-y-2 sm:divide-y-0 sm:divide-x-2 divide-rule-strong mb-8">
        {[
          { label: "Best all-play", row: bestAllPlay, value: `${(bestAllPlay.allPlayRecord.winPct * 100).toFixed(1)}%` },
          { label: "Luckiest", row: luckiest, value: `${signed(luckiest.scheduleLuck)} wins` },
          { label: "Unluckiest", row: unluckiest, value: `${signed(unluckiest.scheduleLuck)} wins` },
        ].map(({ label, row, value }) => (
          <div key={label} className="py-4 sm:px-5 first:pl-0 flex items-center gap-3">
            <ManagerPortrait teamId={row.teamId} teamName={nameOf(row.teamId)} size="sm" />
            <div>
              <div className="eyebrow text-ink-faint">{label}</div>
              <div className="font-display text-lg mt-0.5">{nameOf(row.teamId)}</div>
              <div className="font-data text-sm text-ink-soft">{value}</div>
            </div>
          </div>
        ))}
      </div>

      <ol>
        {rows.map((r, i) => (
          <li
            key={r.teamId}
            className="border-t-2 border-rule-strong last:border-b-2 py-4"
          >
            <div className="grid grid-cols-[2.5rem_44px_minmax(0,1fr)] sm:grid-cols-[2.5rem_44px_minmax(0,1fr)_repeat(5,4.5rem)] items-center gap-3">
              <span className="font-display text-3xl leading-none">
                {String(i + 1).padStart(2, "0")}
              </span>
              <ManagerPortrait
                teamId={r.teamId}
                teamName={nameOf(r.teamId)}
                manager={managerOf(r.teamId)}
                size="sm"
              />
              <Link
                href={`/team/${r.teamId}`}
                className="font-display text-xl hover:text-accent transition-colors min-w-0"
              >
                {nameOf(r.teamId)}
              </Link>
              <Cell label="Actual" value={`${r.actualRecord.wins}–${r.actualRecord.losses}${r.actualRecord.ties ? `–${r.actualRecord.ties}` : ""}`} />
              <Cell label="Real" value={fmtAp(r)} />
              <Cell label="xW" value={r.expectedWins.toFixed(2)} />
              <Cell
                label="Luck"
                value={signed(r.scheduleLuck, 2)}
                tone={r.scheduleLuck > 0.05 ? "pos" : r.scheduleLuck < -0.05 ? "neg" : undefined}
              />
              <Cell label="PF" value={r.pointsFor.toFixed(1)} />
            </div>
            <div className="sm:hidden font-data text-[13px] text-ink-soft mt-2 pl-[calc(2.5rem+44px+1.5rem)] flex flex-wrap gap-x-4">
              <span>ACT <strong className="text-ink">{r.actualRecord.wins}–{r.actualRecord.losses}</strong></span>
              <span>REAL <strong className="text-ink">{fmtAp(r)}</strong></span>
              <span>xW <strong className="text-ink">{r.expectedWins.toFixed(2)}</strong></span>
              <span className={r.scheduleLuck > 0.05 ? "text-positive" : r.scheduleLuck < -0.05 ? "text-negative" : ""}>LUCK <strong>{signed(r.scheduleLuck, 2)}</strong></span>
            </div>
          </li>
        ))}
      </ol>

      <p className="font-data text-xs text-ink-faint mt-6">
        Ranked by expected wins. Real = all-play record vs all 11 teams each
        week. Luck = actual wins minus expected wins.
      </p>
    </div>
  );
}

function Cell({
  label,
  value,
  tone,
}: {
  label: string;
  value: string;
  tone?: "pos" | "neg";
}) {
  return (
    <div className="hidden sm:block text-right">
      <div className="eyebrow text-ink-faint">{label}</div>
      <div
        className={`font-data font-semibold text-sm mt-0.5 ${
          tone === "pos" ? "text-positive" : tone === "neg" ? "text-negative" : ""
        }`}
      >
        {value}
      </div>
    </div>
  );
}

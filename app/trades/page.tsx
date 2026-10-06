import type { Metadata } from "next";
import Link from "next/link";
import { getTeams } from "@/lib/data";
import { getTradeLedgers, type SideLedger, type TradeLedger } from "@/lib/trades";
import ManagerPortrait from "@/components/teams/ManagerPortrait";
import TradeChart from "@/components/trades/TradeChart";

export const metadata: Metadata = {
  title: "Trade Tracker",
  description:
    "Every trade in the league, scored week by week. Who actually won, measured in points, not group-chat volume.",
};

const fmt = (n: number) => n.toFixed(2);
const signedFmt = (n: number) => (n > 0 ? `+${fmt(n)}` : fmt(n));

export default function TradesPage() {
  const ledgers = getTradeLedgers();
  const teams = getTeams();
  const meta = (teamId: string) => teams.find((t) => t.teamId === teamId);
  const latestWeek = ledgers.length
    ? Math.max(...ledgers.map((l) => l.weeks[l.weeks.length - 1] ?? 0))
    : 0;

  return (
    <div className="pt-10 sm:pt-14 pb-8">
      <div className="eyebrow text-accent">Trade Tracker</div>
      <h1 className="font-display text-5xl sm:text-7xl leading-[0.92] mt-3 max-w-[900px]">
        Who Won the Trade
      </h1>
      <p className="font-condensed font-medium mt-5 text-xl sm:text-2xl text-ink-soft max-w-[680px] leading-snug">
        Every deal in the league, scored week by week from the day it
        processed. The group chat has opinions. This page has a ledger.
      </p>

      <details className="mt-5 max-w-[680px]">
        <summary className="eyebrow text-accent cursor-pointer">
          How it&apos;s scored ↓
        </summary>
        <div className="font-data text-sm text-ink-soft mt-3 leading-relaxed space-y-2">
          <p>
            <strong className="text-ink">Lineup points</strong> are what a
            received player scored while in his new team&apos;s starting
            lineup. That&apos;s the headline number, because it&apos;s what
            actually changed the week.
          </p>
          <p>
            <strong className="text-ink">Raw points</strong> count everything
            he scored on the roster, started or benched. It answers a
            different question: who got the better players.
          </p>
          <p>
            Byes and injuries count as zero. Counting stops if a player is
            dropped or traded again. Nothing before the trade is counted.
          </p>
        </div>
      </details>

      <p className="font-data text-xs text-ink-faint mt-4 mb-8">
        {ledgers.length} trade{ledgers.length === 1 ? "" : "s"} · Scored
        through Week {latestWeek}
      </p>

      {ledgers.length === 0 ? (
        <div className="border border-rule bg-surface px-6 py-10 text-center">
          <p className="font-display text-lg">No trades yet.</p>
        </div>
      ) : (
        <div className="space-y-10">
          {ledgers.map((l) => (
            <TradeCard
              key={l.trade.id}
              ledger={l}
              names={[
                meta(l.sides[0].teamId)?.teamName ?? l.sides[0].teamId,
                meta(l.sides[1].teamId)?.teamName ?? l.sides[1].teamId,
              ]}
              managers={[
                meta(l.sides[0].teamId)?.manager ?? "",
                meta(l.sides[1].teamId)?.manager ?? "",
              ]}
            />
          ))}
        </div>
      )}
    </div>
  );
}

function TradeCard({
  ledger,
  names,
  managers,
}: {
  ledger: TradeLedger;
  names: [string, string];
  managers: [string, string];
}) {
  const { trade, sides, lineupGap, rawGap, leaderTeamId, weeks } = ledger;
  const leaderIdx = leaderTeamId === sides[0].teamId ? 0 : leaderTeamId === sides[1].teamId ? 1 : -1;
  const votes =
    trade.vetoes === null || trade.upholds === null
      ? "Vote not recorded"
      : `${trade.vetoes} veto${trade.vetoes === 1 ? "" : "es"} · ${trade.upholds} uphold${trade.upholds === 1 ? "" : "s"}`;

  return (
    <article className="border-2 border-rule-strong bg-surface">
      <header className="px-5 sm:px-6 pt-5 pb-4 border-b-2 border-rule-strong">
        <div className="eyebrow text-ink-faint">
          Processed Week {trade.processedWeek} · {trade.processedAt} · {votes}
        </div>
        <h2 className="font-display text-3xl sm:text-5xl leading-[0.95] mt-2">
          {names[0]} <span className="text-accent">↔</span> {names[1]}
        </h2>
        <p className="font-condensed font-medium text-lg text-ink-soft mt-2 max-w-[720px] leading-snug">
          {trade.summary}
        </p>
      </header>

      {/* Verdict strip */}
      <div className="px-5 sm:px-6 py-4 border-b-2 border-rule flex flex-wrap items-baseline gap-x-6 gap-y-2">
        <div>
          <div className="eyebrow text-ink-faint">Lineup points, through Week {weeks[weeks.length - 1]}</div>
          <div className="font-display text-3xl sm:text-4xl mt-1">
            {leaderIdx === -1 ? (
              <>Dead even</>
            ) : (
              <>
                {names[leaderIdx]}{" "}
                <span className="text-accent">
                  {signedFmt(Math.abs(lineupGap))}
                </span>
              </>
            )}
          </div>
        </div>
        <div className="font-data text-sm text-ink-soft">
          Raw points:{" "}
          <strong className="text-ink">
            {names[0]} {fmt(sides[0].rawTotal)}
          </strong>{" "}
          vs{" "}
          <strong className="text-ink">
            {names[1]} {fmt(sides[1].rawTotal)}
          </strong>{" "}
          ({signedFmt(rawGap)} {names[0]})
        </div>
      </div>

      {/* Two sides */}
      <div className="grid sm:grid-cols-2">
        {sides.map((s, i) => (
          <SidePanel
            key={s.teamId}
            side={s}
            name={names[i]}
            manager={managers[i]}
            leading={leaderIdx === i}
            className={i === 0 ? "sm:border-r-2 border-b-2 sm:border-b-0 border-rule" : ""}
          />
        ))}
      </div>

      {/* Ledger + chart */}
      <div className="grid lg:grid-cols-[1fr_1fr] border-t-2 border-rule">
        <div className="px-5 sm:px-6 py-4 overflow-x-auto">
          <div className="eyebrow text-ink-faint mb-2">Week by week · lineup (raw)</div>
          <table className="w-full font-data text-sm">
            <thead>
              <tr className="text-ink-faint text-xs uppercase tracking-[0.06em]">
                <th className="text-left py-1 font-semibold">Week</th>
                <th className="text-right py-1 font-semibold">{names[0]}</th>
                <th className="text-right py-1 font-semibold">{names[1]}</th>
                <th className="text-right py-1 font-semibold">Running</th>
              </tr>
            </thead>
            <tbody>
              {weeks.map((w, i) => {
                const a = sides[0].weeks[i];
                const b = sides[1].weeks[i];
                const run = sides[0].weeks
                  .slice(0, i + 1)
                  .reduce((acc, x, j) => acc + x.lineup - sides[1].weeks[j].lineup, 0);
                return (
                  <tr key={w} className="border-t border-rule/60">
                    <td className="py-1.5 font-semibold">W{w}</td>
                    <td className="py-1.5 text-right tabular-nums">
                      {fmt(a.lineup)} <span className="text-ink-faint">({fmt(a.raw)})</span>
                    </td>
                    <td className="py-1.5 text-right tabular-nums">
                      {fmt(b.lineup)} <span className="text-ink-faint">({fmt(b.raw)})</span>
                    </td>
                    <td className={`py-1.5 text-right tabular-nums font-semibold ${run > 0 ? "text-positive" : run < 0 ? "text-negative" : ""}`}>
                      {signedFmt(Math.round(run * 100) / 100)}
                    </td>
                  </tr>
                );
              })}
            </tbody>
          </table>
          <p className="font-data text-xs text-ink-faint mt-2">
            Running = {names[0]} minus {names[1]}, lineup points.
          </p>
        </div>
        <div className="px-5 sm:px-6 py-4 border-t-2 lg:border-t-0 lg:border-l-2 border-rule">
          <div className="eyebrow text-ink-faint mb-2">Cumulative lineup points</div>
          <TradeChart
            data={ledger.chart}
            sides={[
              { teamId: sides[0].teamId, teamName: names[0] },
              { teamId: sides[1].teamId, teamName: names[1] },
            ]}
          />
          <div className="flex gap-5 mt-1 font-condensed font-bold uppercase tracking-[0.06em] text-xs">
            <span className="flex items-center gap-1.5"><span className="inline-block w-3 h-[3px] bg-accent" />{names[0]}</span>
            <span className="flex items-center gap-1.5"><span className="inline-block w-3 h-[3px] bg-ink" />{names[1]}</span>
          </div>
        </div>
      </div>
    </article>
  );
}

function SidePanel({
  side,
  name,
  manager,
  leading,
  className,
}: {
  side: SideLedger;
  name: string;
  manager: string;
  leading: boolean;
  className?: string;
}) {
  return (
    <div className={`px-5 sm:px-6 py-5 ${className ?? ""}`}>
      <div className="flex items-center gap-4">
        <ManagerPortrait teamId={side.teamId} teamName={name} manager={manager} size="md" />
        <div className="min-w-0">
          <div className="flex items-center gap-2 flex-wrap">
            <Link href={`/team/${side.teamId}`} className="font-display text-2xl hover:text-accent transition-colors">
              {name}
            </Link>
            {leading && (
              <span className="eyebrow bg-accent text-paper px-1.5 py-0.5">Ahead</span>
            )}
          </div>
          <div className="font-condensed font-medium text-sm text-ink-soft uppercase tracking-[0.04em]">
            {manager} · {side.recordSince.wins}–{side.recordSince.losses} since the trade
          </div>
        </div>
      </div>

      <div className="mt-4 flex items-baseline gap-5">
        <div>
          <div className="eyebrow text-ink-faint">Lineup</div>
          <div className="font-display text-3xl">{fmt(side.lineupTotal)}</div>
        </div>
        <div>
          <div className="eyebrow text-ink-faint">Raw</div>
          <div className="font-display text-xl text-ink-soft">{fmt(side.rawTotal)}</div>
        </div>
      </div>

      <div className="eyebrow text-ink-faint mt-4 mb-1">Received</div>
      <ul className="font-data text-sm">
        {side.received.map((p) => {
          const lineup = Object.values(p.weeks).reduce((a, l) => a + (l.started ? l.points : 0), 0);
          const raw = Object.values(p.weeks).reduce((a, l) => a + l.points, 0);
          return (
            <li key={p.player} className="flex items-baseline gap-3 py-1.5 border-b border-rule/50">
              <span className="text-ink-faint text-xs w-8 shrink-0">{p.position}</span>
              <span className="font-medium">{p.player}</span>
              <span className="text-ink-faint text-xs">{p.nflTeam}</span>
              <span className="ml-auto tabular-nums">
                {fmt(lineup)}{" "}
                <span className="text-ink-faint">({fmt(raw)})</span>
              </span>
            </li>
          );
        })}
      </ul>
    </div>
  );
}

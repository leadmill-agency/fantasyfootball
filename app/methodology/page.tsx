import type { Metadata } from "next";
import Link from "next/link";

export const metadata: Metadata = {
  title: "Methodology",
  description:
    "How the power scores, title odds, and draft grades are made. No invented numbers, ever.",
};

export default function MethodologyPage() {
  return (
    <div className="pt-10 sm:pt-14 pb-8 max-w-[760px]">
      <div className="eyebrow text-accent">Methodology</div>
      <h1 className="font-display text-5xl sm:text-7xl leading-[0.92] mt-3">
        How the Numbers Work
      </h1>
      <p className="font-condensed font-medium mt-5 text-xl sm:text-2xl text-ink-soft leading-snug">
        Every number on this site has a source. Here they all are.
      </p>

      <Section id="power-score" title="Power Score">
        <p>
          The 0–100 rating behind the Power Rankings, answering one question:{" "}
          <em>who has the strongest team right now?</em> It is not the
          standings. A lucky 5–1 team can sit below an unlucky 3–3 team.
        </p>
        <p>
          In-season, the score weighs current roster strength (35%), season
          performance (25%), recent performance over roughly three weeks (15%),
          roster trajectory — trades, waivers, injuries, role changes (15%) —
          and record/playoff position (10%). The preseason board is the
          post-draft analysis of roster strength, ceiling, and construction,
          before any games existed to score.
        </p>
        <p>
          The rankings are authored, not just computed. When the columnist
          disagrees with a mechanical ordering, the column says so and says
          why.
        </p>
      </Section>

      <Section id="title-odds" title="Title Odds">
        <p>
          A different question: <em>who actually wins this thing?</em> Twelve
          probabilities that always sum to exactly 100%. Because eight of
          twelve teams make the playoffs and every playoff round is a one-week,
          single-elimination matchup, the market stays compressed — no
          preseason roster earns some absurd 30% share. The American-style
          odds are a conversion for entertainment. This is not a sportsbook.
        </p>
      </Section>

      <Section id="draft-grades" title="Draft Grades">
        <p>
          A frozen artifact, graded with information available on August 29,
          2026, and never revised. The components: value vs ADP (30%),
          starting lineup (25%), championship ceiling (20%), roster
          construction (15%), and bench optionality (10%).
        </p>
        <p>
          ADP comes from a real recorded source: Fantasy Football Calculator's
          12-team half-PPR data, 3,302 live drafts sampled August 24–29, 2026.
          Players outside that source are shown without ADP — an unknown stays
          unknown.
        </p>
        <p>
          The grades and the power board are allowed to disagree, and they do.
          A C+ draft can be the fourth-best team. An A- draft can rank
          seventh. The columns explain the gaps.
        </p>
      </Section>

      <Section id="data-integrity" title="Data Integrity">
        <p>
          Nothing is invented: no fabricated ADP, statistics, scores,
          injuries, or transactions. Historical snapshots are immutable — once
          a week publishes, it stays exactly as it was believed at the time,
          wrong takes included. That is the point.
        </p>
      </Section>

      <div className="mt-10 flex gap-6">
        <Link
          href="/"
          className="font-condensed font-bold uppercase tracking-[0.06em] text-sm text-accent hover:underline underline-offset-4"
        >
          Back to Power Rankings →
        </Link>
      </div>
    </div>
  );
}

function Section({
  id,
  title,
  children,
}: {
  id: string;
  title: string;
  children: React.ReactNode;
}) {
  return (
    <section id={id} className="mt-12 border-t-2 border-rule-strong pt-6 scroll-mt-24">
      <h2 className="font-display text-2xl sm:text-3xl mb-4">{title}</h2>
      <div className="prose-editorial space-y-4 [&_p]:text-[15px]">{children}</div>
    </section>
  );
}

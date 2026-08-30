"use client";

import Link from "next/link";

export default function Error({ reset }: { error: Error; reset: () => void }) {
  return (
    <div className="py-24 text-center">
      <p className="font-display text-4xl">Something broke.</p>
      <p className="text-ink-soft mt-2">
        The model takes no responsibility. It only does rankings.
      </p>
      <div className="mt-6 flex gap-6 justify-center">
        <button
          onClick={reset}
          className="eyebrow text-accent hover:underline underline-offset-4"
        >
          Try again
        </button>
        <Link
          href="/"
          className="eyebrow text-ink-soft hover:text-ink"
        >
          Back to Power Rankings
        </Link>
      </div>
    </div>
  );
}

"use client";

import { useRouter, usePathname } from "next/navigation";
import { useEffect, useRef } from "react";

export default function WeekSelector({
  weeks,
  selected,
}: {
  weeks: (number | "preseason")[];
  selected: number | "preseason";
}) {
  const router = useRouter();
  const pathname = usePathname();
  const scroller = useRef<HTMLDivElement>(null);

  useEffect(() => {
    scroller.current
      ?.querySelector('[aria-current="true"]')
      ?.scrollIntoView({ block: "nearest", inline: "center" });
  }, [selected]);

  return (
    <div
      ref={scroller}
      className="flex gap-5 sm:gap-6 overflow-x-auto border-y-2 border-rule-strong py-2.5 mb-8 [scrollbar-width:none]"
      role="tablist"
      aria-label="Select week"
    >
      {weeks.map((w) => {
        const active = String(w) === String(selected);
        const label = w === "preseason" ? "Preseason" : `W${w}`;
        return (
          <button
            key={String(w)}
            role="tab"
            aria-selected={active}
            aria-current={active}
            onClick={() => router.push(`${pathname}?week=${w}`, { scroll: false })}
            className={`font-condensed font-bold uppercase tracking-[0.06em] text-[15px] whitespace-nowrap px-1 transition-colors ${
              active
                ? "text-accent"
                : "text-ink-soft hover:text-ink"
            }`}
          >
            {label}
          </button>
        );
      })}
    </div>
  );
}

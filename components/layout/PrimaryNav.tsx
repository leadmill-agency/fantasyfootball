"use client";

import Link from "next/link";
import { usePathname } from "next/navigation";

const ITEMS = [
  { href: "/", label: "Power Rankings", short: "Power" },
  { href: "/odds", label: "Title Odds", short: "Odds" },
  { href: "/draft-grades", label: "Draft Grades", short: "Draft" },
];

export default function PrimaryNav() {
  const pathname = usePathname();
  return (
    <nav aria-label="Primary" className="flex gap-5 sm:gap-7 mt-2">
      {ITEMS.map((item) => {
        const active =
          item.href === "/"
            ? pathname === "/" || pathname.startsWith("/team")
            : pathname.startsWith(item.href);
        return (
          <Link
            key={item.href}
            href={item.href}
            aria-current={active ? "page" : undefined}
            className={`font-condensed font-bold uppercase tracking-[0.06em] text-[15px] pb-2 border-b-[3px] transition-colors ${
              active
                ? "border-accent text-ink"
                : "border-transparent text-ink-soft hover:text-ink"
            }`}
          >
            <span className="hidden sm:inline">{item.label}</span>
            <span className="sm:hidden">{item.short}</span>
          </Link>
        );
      })}
    </nav>
  );
}

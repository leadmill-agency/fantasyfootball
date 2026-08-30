import Link from "next/link";
import { getLatestWeek } from "@/lib/data";
import { weekLabel } from "@/lib/format";
import PrimaryNav from "./PrimaryNav";

export default function SiteHeader() {
  const latest = getLatestWeek();
  return (
    <header className="w-full bg-paper sticky top-0 z-40 border-b-4 border-rule-strong">
      <div className="max-w-[1280px] mx-auto px-4 sm:px-6 lg:px-8">
        <div className="flex items-center justify-between pt-3 sm:pt-4">
          <Link
            href="/"
            className="font-display text-2xl sm:text-3xl leading-none hover:text-accent transition-colors"
          >
            Kingwood{" "}
            <span className="bg-accent text-paper px-1.5 inline-block">
              Killaz
            </span>
          </Link>
          <div className="eyebrow text-ink-soft text-right leading-tight">
            {weekLabel(latest)}
            <span className="block text-ink-faint">2026 season</span>
          </div>
        </div>
        <PrimaryNav />
      </div>
    </header>
  );
}

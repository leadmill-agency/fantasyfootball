"use client";

import { useRouter, useSearchParams } from "next/navigation";

export default function CompareSelector({
  teams,
  a,
  b,
}: {
  teams: { teamId: string; teamName: string }[];
  a?: string;
  b?: string;
}) {
  const router = useRouter();
  const params = useSearchParams();

  const update = (key: "a" | "b", value: string) => {
    const next = new URLSearchParams(params.toString());
    if (value) next.set(key, value);
    else next.delete(key);
    router.push(`/compare?${next.toString()}`, { scroll: false });
  };

  const select = (key: "a" | "b", current?: string, exclude?: string) => (
    <label className="flex-1 min-w-0">
      <span className="eyebrow text-ink-faint block mb-1.5">
        {key === "a" ? "Team 1" : "Team 2"}
      </span>
      <select
        value={current ?? ""}
        onChange={(e) => update(key, e.target.value)}
        className="w-full font-data text-sm bg-surface border border-rule px-3 py-2.5 focus:border-accent focus:outline-none"
      >
        <option value="">Select team…</option>
        {teams
          .filter((t) => t.teamId !== exclude)
          .map((t) => (
            <option key={t.teamId} value={t.teamId}>
              {t.teamName}
            </option>
          ))}
      </select>
    </label>
  );

  return (
    <div className="flex flex-col sm:flex-row gap-4 sm:items-end mb-10">
      {select("a", a, b)}
      <span className="eyebrow text-ink-faint text-center hidden sm:block pb-3">
        vs
      </span>
      {select("b", b, a)}
    </div>
  );
}

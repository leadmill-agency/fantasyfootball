import type { WeekId } from "./schemas";

export function weekLabel(week: WeekId): string {
  return week === "preseason" ? "Preseason" : `Week ${week}`;
}

export function weekShort(week: WeekId): string {
  return week === "preseason" ? "PRE" : `W${week}`;
}

export function formatRecord(r?: { wins: number; losses: number }): string {
  return r ? `${r.wins}–${r.losses}` : "0–0";
}

export function movement(current: number, previous?: number) {
  if (previous === undefined) return { dir: "none" as const, amount: 0 };
  const delta = previous - current;
  if (delta > 0) return { dir: "up" as const, amount: delta };
  if (delta < 0) return { dir: "down" as const, amount: -delta };
  return { dir: "flat" as const, amount: 0 };
}

export function signed(n: number, digits = 1): string {
  const v = n.toFixed(digits);
  return n > 0 ? `+${v}` : v;
}

export function publishedDate(iso: string): string {
  return new Date(`${iso}T12:00:00`).toLocaleDateString("en-US", {
    weekday: "long",
    month: "long",
    day: "numeric",
  });
}

import { movement } from "@/lib/format";

export default function Movement({
  current,
  previous,
  size = "md",
}: {
  current: number;
  previous?: number;
  size?: "md" | "lg";
}) {
  const m = movement(current, previous);
  const cls = size === "lg" ? "text-base" : "text-sm";
  if (m.dir === "up")
    return (
      <span className={`font-data font-semibold text-positive ${cls}`}>
        ↑{m.amount}
        <span className="sr-only"> up {m.amount} from last week</span>
      </span>
    );
  if (m.dir === "down")
    return (
      <span className={`font-data font-semibold text-negative ${cls}`}>
        ↓{m.amount}
        <span className="sr-only"> down {m.amount} from last week</span>
      </span>
    );
  return (
    <span className={`font-data text-ink-faint ${cls}`} aria-label="no movement">
      —
    </span>
  );
}

"use client";

import { useState } from "react";
import {
  LineChart,
  Line,
  XAxis,
  YAxis,
  Tooltip,
  ResponsiveContainer,
} from "recharts";

type SeriesPoint = { week: string; [teamId: string]: string | number };

export default function OddsChart({
  data,
  teams,
}: {
  data: SeriesPoint[];
  teams: { teamId: string; teamName: string }[];
}) {
  const [selected, setSelected] = useState<string | null>(null);

  if (data.length < 2) {
    return (
      <div className="border border-rule bg-surface px-6 py-10 text-center my-8">
        <p className="font-display text-lg">
          The odds history chart unlocks after Week 1.
        </p>
        <p className="font-data text-xs text-ink-faint mt-2">
          One data point is a dot, not a story.
        </p>
      </div>
    );
  }

  return (
    <div className="my-8">
      <div className="flex gap-2 flex-wrap mb-4">
        <Chip
          label="All"
          active={selected === null}
          onClick={() => setSelected(null)}
        />
        {teams.map((t) => (
          <Chip
            key={t.teamId}
            label={t.teamName}
            active={selected === t.teamId}
            onClick={() =>
              setSelected(selected === t.teamId ? null : t.teamId)
            }
          />
        ))}
      </div>
      <div className="h-[360px]">
        <ResponsiveContainer width="100%" height="100%">
          <LineChart data={data} margin={{ top: 8, right: 8, bottom: 0, left: -16 }}>
            <XAxis
              dataKey="week"
              tick={{ fontSize: 11, fontFamily: "var(--font-inter)" }}
              stroke="#8a8371"
            />
            <YAxis
              tick={{ fontSize: 11, fontFamily: "var(--font-inter)" }}
              stroke="#8a8371"
              tickFormatter={(v) => `${v}%`}
            />
            <Tooltip
              formatter={(value, name) => [
                `${value}%`,
                teams.find((t) => t.teamId === name)?.teamName ?? name,
              ]}
              contentStyle={{
                fontFamily: "var(--font-inter)",
                fontSize: 12,
                background: "#fdfcf8",
                border: "1px solid #d9d2c2",
              }}
            />
            {teams.map((t) => {
              const emphasized = selected === null || selected === t.teamId;
              return (
                <Line
                  key={t.teamId}
                  dataKey={t.teamId}
                  type="monotone"
                  dot={false}
                  stroke={selected === t.teamId ? "#8c1f13" : "#171310"}
                  strokeWidth={selected === t.teamId ? 2.5 : 1.25}
                  strokeOpacity={emphasized ? (selected ? 1 : 0.55) : 0.12}
                />
              );
            })}
          </LineChart>
        </ResponsiveContainer>
      </div>
    </div>
  );
}

function Chip({
  label,
  active,
  onClick,
}: {
  label: string;
  active: boolean;
  onClick: () => void;
}) {
  return (
    <button
      onClick={onClick}
      aria-pressed={active}
      className={`font-data text-xs px-2.5 py-1 border transition-colors ${
        active
          ? "border-accent text-accent"
          : "border-rule text-ink-soft hover:border-ink-soft"
      }`}
    >
      {label}
    </button>
  );
}

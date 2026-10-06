"use client";

import {
  LineChart,
  Line,
  XAxis,
  YAxis,
  Tooltip,
  ResponsiveContainer,
} from "recharts";

type Row = { week: string; [teamId: string]: string | number };

export default function TradeChart({
  data,
  sides,
}: {
  data: Row[];
  sides: { teamId: string; teamName: string }[];
}) {
  const colors = ["#e0250e", "#0d0d0c"];
  return (
    <div className="h-[220px] sm:h-[260px]">
      <ResponsiveContainer width="100%" height="100%">
        <LineChart data={data} margin={{ top: 8, right: 12, bottom: 0, left: -18 }}>
          <XAxis
            dataKey="week"
            tick={{ fontSize: 11, fontFamily: "var(--font-inter)", fill: "#85837b" }}
            axisLine={{ stroke: "#cfcdc4" }}
            tickLine={false}
          />
          <YAxis
            tick={{ fontSize: 11, fontFamily: "var(--font-inter)", fill: "#85837b" }}
            axisLine={false}
            tickLine={false}
            width={48}
          />
          <Tooltip
            contentStyle={{
              border: "2px solid #0d0d0c",
              borderRadius: 0,
              background: "#ffffff",
              fontFamily: "var(--font-inter)",
              fontSize: 12,
            }}
            formatter={(value, name) => [
              `${Number(value).toFixed(2)} pts`,
              sides.find((s) => s.teamId === name)?.teamName ?? String(name),
            ]}
          />
          {sides.map((s, i) => (
            <Line
              key={s.teamId}
              type="monotone"
              dataKey={s.teamId}
              stroke={colors[i]}
              strokeWidth={3}
              dot={{ r: 4, strokeWidth: 0, fill: colors[i] }}
              isAnimationActive={false}
            />
          ))}
        </LineChart>
      </ResponsiveContainer>
    </div>
  );
}

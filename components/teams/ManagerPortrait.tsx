import Image from "next/image";

const SIZES = { xs: 32, sm: 44, md: 56, lg: 96, hero: 200 } as const;

export default function ManagerPortrait({
  teamId,
  teamName,
  manager,
  variant = "headshot",
  size = "md",
  priority = false,
  className = "",
}: {
  teamId: string;
  teamName: string;
  manager?: string;
  variant?: "headshot" | "portrait";
  size?: keyof typeof SIZES;
  priority?: boolean;
  className?: string;
}) {
  const px = SIZES[size];
  const src = `/managers/${teamId}/${variant}.webp`;
  const initials = teamName
    .split(/\s+/)
    .map((w) => w[0])
    .join("")
    .slice(0, 3)
    .toUpperCase();

  return (
    <span
      className={`relative inline-block shrink-0 overflow-hidden border-2 border-rule-strong bg-surface ${className}`}
      style={className.includes("w-") ? undefined : { width: px, height: px }}
    >
      <Image
        src={src}
        alt={manager ? `${manager} — ${teamName}` : teamName}
        width={px}
        height={px}
        priority={priority}
        className="object-cover w-full h-full"
      />
      <span
        aria-hidden
        className="absolute inset-0 -z-10 flex items-center justify-center font-condensed font-bold text-ink-faint"
      >
        {initials}
      </span>
    </span>
  );
}

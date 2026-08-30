import Link from "next/link";

export default function NotFound() {
  return (
    <div className="py-24 text-center">
      <p className="font-display text-4xl">Team not found.</p>
      <p className="text-ink-soft mt-2">
        Either the slug is wrong or someone got relegated.
      </p>
      <Link
        href="/"
        className="eyebrow text-accent mt-6 inline-block hover:underline underline-offset-4"
      >
        Back to Power Rankings
      </Link>
    </div>
  );
}

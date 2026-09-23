#!/usr/bin/env python3
"""Pre-ship checks for a weekly package. Usage: python3 scripts/check-week.py N

1. Banned-phrase lint over scripts/editorial-week-N.json (voice PRD §16-17).
2. Every team's movementReasons sum to its power-score change vs last week.
3. Title odds sum to 100.0; playoff odds sum to ~800.
4. Prints cumulative record + PF per team from data/results/ — compare these
   against the ESPN standings screenshot before shipping.
Exits non-zero on any failure.
"""
import json, os, re, sys

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
week = int(sys.argv[1])

BANNED = [
    "fantasy gods", "roller coaster", "firing on all cylinders", "league mates beware",
    "don't sleep on", "quietly", "poised for", "force to be reckoned", "championship pedigree",
    "set and forget", "must start", "stud", "smash spot", "only time will tell",
    "anything can happen", "leverage", "here's the thing", "make no mistake",
    "at the end of the day", "when all is said and done", "one thing is clear",
    "one thing is for sure", "it remains to be seen", "time will tell",
    "what makes this interesting", "what stands out", "worth noting",
    "important to remember", "no denying", "in many ways", "the reality is",
    "the bottom line is", "with that being said", "moving forward", "looking ahead",
    "isn't just a", "not only",
]

failures = []

ed = json.load(open(f"{ROOT}/scripts/editorial-week-{week}.json"))
texts = [("deck", ed["deck"])] + [
    (f"{tid}.{k}", v[k]) for tid, v in ed["teams"].items() for k in ("headline", "verdict", "analysis")
]
for where, text in texts:
    for phrase in BANNED:
        if re.search(rf"\b{re.escape(phrase)}\b", text, re.IGNORECASE):
            failures.append(f"lint: '{phrase}' in {where}")

snap = json.load(open(f"{ROOT}/data/weeks/week-{week}.json"))
prev_file = f"{ROOT}/data/weeks/week-{week - 1}.json" if week > 1 else f"{ROOT}/data/weeks/preseason.json"
prev = {t["teamId"]: t["powerScore"] for t in json.load(open(prev_file))["teams"]}
for t in snap["teams"]:
    want = round(t["powerScore"] - prev[t["teamId"]], 1)
    got = round(sum(m["delta"] for m in t["movementReasons"]), 1)
    if want != got:
        failures.append(f"movement: {t['teamId']} reasons sum {got}, score moved {want}")

odds = round(sum(t["titleOdds"] for t in snap["teams"]), 1)
if odds != 100.0:
    failures.append(f"odds: title odds sum to {odds}")
playoff = round(sum(t["playoffOdds"] for t in snap["teams"]), 1)
if abs(playoff - 800) > 0.5:
    failures.append(f"odds: playoff odds sum to {playoff}")

rec, pf = {}, {}
for wk in range(1, week + 1):
    for m in json.load(open(f"{ROOT}/data/results/week-{wk}.json"))["matchups"]:
        for tid, mine, theirs in ((m["homeTeamId"], m["homeScore"], m["awayScore"]),
                                  (m["awayTeamId"], m["awayScore"], m["homeScore"])):
            w, l = rec.get(tid, (0, 0))
            rec[tid] = (w + (mine > theirs), l + (mine < theirs))
            pf[tid] = round(pf.get(tid, 0) + mine, 2)

print(f"Cumulative through Week {week} (match these to ESPN standings):")
for tid in sorted(pf, key=pf.get, reverse=True):
    print(f"  {tid:<28} {rec[tid][0]}-{rec[tid][1]}  PF {pf[tid]}")

if failures:
    print("\nFAILED:")
    for f in failures:
        print("  " + f)
    sys.exit(1)
print("\nAll checks passed.")

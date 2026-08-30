#!/usr/bin/env python3
"""Swap per-pick ADP display data in draft-grades.json to the ESPN source.

Rewrites ONLY adp / adpDiff / grade on each pick row (letter thresholds
identical to compute-preseason.py). Team-level grade, score, components,
constructionNotes, verdict, and pick comments are preserved untouched —
the team grades are a frozen artifact computed against the FFC market.
"""
import json, os

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
espn = json.load(open(f"{ROOT}/data/adp-espn.json"))
grades = json.load(open(f"{ROOT}/data/draft-grades.json"))

by_overall = {p["overallPick"]: p for p in espn["players"]}

def pick_grade(diff):
    if diff is None: return None
    if diff >= 24: return "A"
    if diff >= 10: return "B+"
    if diff >= -6: return "B"
    if diff >= -18: return "C+"
    if diff >= -36: return "C"
    return "D"

for team in grades["teams"]:
    for p in team["picks"]:
        src = by_overall[p["overall"]]
        p["adp"] = src["adp"]
        p["adpDiff"] = None if src["adp"] is None else round(p["overall"] - src["adp"], 1)
        p["grade"] = pick_grade(p["adpDiff"])

grades["displayAdpSource"] = espn["source"]
json.dump(grades, open(f"{ROOT}/data/draft-grades.json", "w"), indent=2)
print("applied ESPN ADP to", sum(len(t["picks"]) for t in grades["teams"]), "pick rows")

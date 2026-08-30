#!/usr/bin/env python3
"""Sync grade verdicts + per-pick comments from scripts/editorial.json into
data/draft-grades.json. Team grades/scores/components are never touched."""
import json, os

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
ed = json.load(open(f"{ROOT}/scripts/editorial.json"))["grades"]
grades = json.load(open(f"{ROOT}/data/draft-grades.json"))

for team in grades["teams"]:
    e = ed[team["teamId"]]
    team["verdict"] = e["verdict"]
    comments = {int(k): v for k, v in e.get("pickComments", {}).items()}
    for p in team["picks"]:
        p.pop("comment", None)
        if p["overall"] in comments:
            p["comment"] = comments[p["overall"]]

json.dump(grades, open(f"{ROOT}/data/draft-grades.json", "w"), indent=2)
print("grade editorial synced")

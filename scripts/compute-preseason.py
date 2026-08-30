#!/usr/bin/env python3
"""Compute preseason draft grades + power scores + title odds for Kingwood Killaz.

All inputs are traceable: data/draft.json (actual picks) and data/adp.json
(Fantasy Football Calculator 12-team half-PPR ADP, 3,302 drafts, 2026-08-24..29).

Player value proxy: v(adp) = 100 * exp(-0.028 * (adp - 1)).
Players absent from the ADP source get a floor value of 1.0 (never invented).

Grade components (product PRD section 14):
  30% Value vs ADP   - sum of (overall pick - adp) across picks, normalized
  25% Starting Lineup - value of best legal starting lineup
  20% Championship Ceiling - value of top-4 skill players
  15% Roster Construction - balance/timing penalties (early K/DST, thin slots)
  10% Bench Optionality - value of bench after starters

Preseason power score = 70% starters + 30% bench value, scaled to 0-100.
Title odds = softmax over power scores, temperature tuned for compression
(playoff field of 8 with single-week elimination keeps odds tight), sums to 100.0.
"""
import json, math, os
from collections import defaultdict

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
draft = json.load(open(f"{ROOT}/data/draft.json"))
adp = json.load(open(f"{ROOT}/data/adp.json"))

adp_by_overall = {p["overallPick"]: p for p in adp["players"]}

def player_value(a):
    if a is None:
        return 1.0
    return 100 * math.exp(-0.028 * (a - 1))

teams = defaultdict(list)
for pick in draft["picks"]:
    src = adp_by_overall[pick["overall"]]
    teams[pick["teamId"]].append({
        **pick,
        "adp": src.get("adp"),
        "adpFormatted": src.get("adpFormatted"),
        "value": round(player_value(src.get("adp")), 2),
    })

STARTER_SLOTS = [("QB", ["QB"]), ("RB", ["RB"]), ("RB", ["RB"]), ("WR", ["WR"]),
                 ("WR", ["WR"]), ("TE", ["TE"]), ("FLEX", ["RB", "WR", "TE"]),
                 ("D/ST", ["D/ST"]), ("K", ["K"])]

def best_lineup(players):
    pool = sorted(players, key=lambda p: -p["value"])
    used, lineup = set(), []
    for slot, allowed in STARTER_SLOTS:
        for p in pool:
            if id(p) in used or p["position"] not in allowed:
                continue
            used.add(id(p))
            lineup.append({"slot": slot, **{k: p[k] for k in ("player", "position", "nflTeam", "value", "adp", "overall")}})
            break
    bench = [p for p in pool if id(p) not in used]
    return lineup, bench

results = {}
for tid, players in teams.items():
    lineup, bench = best_lineup(players)
    starters_raw = sum(p["value"] for p in lineup)
    bench_raw = sum(p["value"] for p in bench)
    value_vs_adp = sum((p["overall"] - p["adp"]) for p in players if p["adp"] is not None)
    skill = sorted([p for p in players if p["position"] in ("QB", "RB", "WR", "TE")], key=lambda p: -p["value"])
    ceiling_raw = sum(p["value"] for p in skill[:4])

    penalties, notes = 0, []
    for p in players:
        if p["position"] in ("K", "D/ST") and p["round"] <= 10:
            penalties += (11 - p["round"]) * 4
            notes.append(f'{p["player"]} ({p["position"]}) drafted round {p["round"]}')
    for entry in lineup:
        if entry["slot"] in ("QB", "RB", "WR", "TE") and (entry["adp"] is None or entry["adp"] > 110):
            penalties += 6
            notes.append(f'thin starting slot: {entry["slot"]} ({entry["player"]}, ADP {entry["adp"]})')
    pos_counts = defaultdict(int)
    for p in players:
        pos_counts[p["position"]] += 1
    for pos in ("RB", "WR"):
        if pos_counts[pos] >= 7:
            penalties += 4
            notes.append(f'{pos_counts[pos]} {pos}s drafted (hoarding)')
    construction_raw = max(0, 100 - penalties)

    results[tid] = {
        "teamId": tid,
        "players": players,
        "lineup": lineup,
        "bench": bench,
        "raw": {"valueVsAdp": round(value_vs_adp, 1), "starters": round(starters_raw, 1),
                "ceiling": round(ceiling_raw, 1), "construction": construction_raw,
                "bench": round(bench_raw, 1)},
        "constructionNotes": notes,
    }

def normalize(vals, lo=55, hi=98):
    mn, mx = min(vals.values()), max(vals.values())
    if mx == mn:
        return {k: (lo + hi) / 2 for k in vals}
    return {k: lo + (v - mn) / (mx - mn) * (hi - lo) for k, v in vals.items()}

norm = {}
for comp in ("valueVsAdp", "starters", "ceiling", "bench"):
    norm[comp] = normalize({t: r["raw"][comp] for t, r in results.items()})
norm["construction"] = {t: r["raw"]["construction"] for t, r in results.items()}

WEIGHTS = {"valueVsAdp": 0.30, "starters": 0.25, "ceiling": 0.20, "construction": 0.15, "bench": 0.10}
overall_scores = {t: sum(norm[c][t] * w for c, w in WEIGHTS.items()) for t in results}

ranked = sorted(overall_scores, key=lambda t: -overall_scores[t])
GRADES = ["A", "A-", "B+", "B+", "B", "B", "B-", "B-", "C+", "C+", "C", "C-"]
grade_of = {t: GRADES[i] for i, t in enumerate(ranked)}

power_raw = {t: 0.7 * norm["starters"][t] + 0.3 * norm["bench"][t] for t in results}
power = normalize(power_raw, 62, 91)
power_ranked = sorted(power, key=lambda t: -power[t])

TEMP = 24.0
exps = {t: math.exp(power[t] / TEMP) for t in results}
total = sum(exps.values())
odds = {t: 100 * e / total for t, e in exps.items()}
odds_rounded = {t: round(v, 1) for t, v in odds.items()}
drift = round(100.0 - sum(odds_rounded.values()), 1)
odds_rounded[max(odds_rounded, key=odds_rounded.get)] = round(
    odds_rounded[max(odds_rounded, key=odds_rounded.get)] + drift, 1)

po_norm = normalize(power_raw, -1.2, 1.2)
playoff = {t: 66.7 + po_norm[t] * 10 for t in results}
po_scale = 800 / sum(playoff.values())
playoff = {t: round(v * po_scale, 1) for t, v in playoff.items()}

def american(prob):
    p = prob / 100
    return f"+{round((1 - p) / p * 100 / 5) * 5}"

grades_out = {"season": 2026, "gradedAs Of": None}
grades_out = {
    "season": 2026,
    "gradedAsOf": "2026-08-29",
    "methodology": {
        "weights": WEIGHTS,
        "playerValueCurve": "v(adp) = 100 * exp(-0.028 * (adp - 1)); floor 1.0 when ADP unknown",
        "adpSource": adp["source"],
    },
    "teams": [],
}
for i, tid in enumerate(ranked):
    r = results[tid]
    pick_rows = []
    for p in sorted(r["players"], key=lambda x: x["overall"]):
        diff = None if p["adp"] is None else round(p["overall"] - p["adp"], 1)
        if diff is None:
            pg = None
        elif diff >= 24: pg = "A"
        elif diff >= 10: pg = "B+"
        elif diff >= -6: pg = "B"
        elif diff >= -18: pg = "C+"
        elif diff >= -36: pg = "C"
        else: pg = "D"
        pick_rows.append({"round": p["round"], "pickInRound": p["pickInRound"], "overall": p["overall"],
                          "player": p["player"], "position": p["position"], "nflTeam": p["nflTeam"],
                          "adp": p["adp"], "adpDiff": diff, "grade": pg})
    grades_out["teams"].append({
        "teamId": tid, "rank": i + 1, "grade": grade_of[tid],
        "score": round(overall_scores[tid], 1),
        "components": {c: round(norm[c][tid], 1) for c in WEIGHTS},
        "constructionNotes": r["constructionNotes"],
        "verdict": "",
        "picks": pick_rows,
    })

pre_out = {
    "week": "preseason",
    "publishedAt": "2026-08-29",
    "deck": "",
    "teams": [],
}
for i, tid in enumerate(power_ranked):
    r = results[tid]
    pre_out["teams"].append({
        "teamId": tid,
        "powerRank": i + 1,
        "powerScore": round(power[tid], 1),
        "titleOdds": odds_rounded[tid],
        "titleOddsAmerican": american(odds_rounded[tid]),
        "playoffOdds": playoff[tid],
        "draftGrade": grade_of[tid],
        "headline": "",
        "verdict": "",
        "analysis": "",
        "roster": {
            "starters": [{"slot": e["slot"], "player": e["player"], "position": e["position"], "nflTeam": e["nflTeam"]} for e in r["lineup"]],
            "bench": [{"player": p["player"], "position": p["position"], "nflTeam": p["nflTeam"]} for p in r["bench"]],
        },
    })

json.dump(grades_out, open(f"{ROOT}/data/draft-grades.json", "w"), indent=2)
json.dump(pre_out, open(f"{ROOT}/data/weeks/preseason.json", "w"), indent=2)

print("POWER RANKS / ODDS:")
for t in pre_out["teams"]:
    print(f'  #{t["powerRank"]:>2} {t["teamId"]:<28} score {t["powerScore"]:>5}  odds {t["titleOdds"]:>4}%  ({t["titleOddsAmerican"]})  grade {t["draftGrade"]}')
print("sum odds:", round(sum(t["titleOdds"] for t in pre_out["teams"]), 1))
print("\nDRAFT GRADE ORDER:")
for g in grades_out["teams"]:
    c = g["components"]
    print(f'  {g["rank"]:>2} {g["teamId"]:<28} {g["grade"]:<3} score {g["score"]}  val {c["valueVsAdp"]}  st {c["starters"]}  ceil {c["ceiling"]}  con {c["construction"]}  bench {c["bench"]}')

#!/usr/bin/env python3
"""Build data/weeks/preseason.json.

Sources (all verified, none invented):
- Power ranking, tiers, archetypes, ceiling ranks: the canonical post-draft
  analysis in kingwood_killaz_draft_board_rankings_reference.md (analyst
  judgment, NOT the ADP curve — draft grades remain pure ADP math, and the
  two boards intentionally disagree; see voice PRD section 51).
- Starting lineups: verified ESPN roster screenshots transcribed in the same
  reference doc. MBK/HNFNR kickers were unreadable in screenshots but each
  roster drafted exactly one K, so they follow by elimination.
- Bench: drafted roster minus starters (data/draft.json).
- Title odds: softmax over power scores, T=24 (compressed market), sum 100.0.
- Editorial: scripts/editorial.json.
"""
import json, math, os

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
draft = json.load(open(f"{ROOT}/data/draft.json"))
grades = json.load(open(f"{ROOT}/data/draft-grades.json"))
editorial = json.load(open(f"{ROOT}/scripts/editorial.json"))

grade_of = {t["teamId"]: t["grade"] for t in grades["teams"]}
drafted = {}
for p in draft["picks"]:
    drafted.setdefault(p["teamId"], []).append(p)

# rank, teamId, powerScore, tier, archetype, ceilingRank(optional)
BOARD = [
    (1, "team-noor", 88.6, "Favorite", "The Complete Team", 3),
    (2, "bizzy", 87.2, "Favorite", "The RB Machine", 2),
    (3, "team-mbk", 86.5, "Favorite", "The Floor Monster", 6),
    (4, "bazan", 80.1, "Contender", "The Nuclear Core", 4),
    (5, "rambam", 79.4, "Contender", "The Venture Portfolio", 1),
    (6, "mustafas-magnificent-team", 78.6, "Contender", "The Deep Bench", None),
    (7, "hnfnr-aint-busy", 77.9, "Playoff-caliber", "The Stars Up Top", None),
    (8, "i-eat-ass", 76.4, "High-variance playoff team", "The Volatility Bet", None),
    (9, "chief-sheikh", 75.1, "Stars-and-scrubs contender", "The WR Superteam", None),
    (10, "gang-green", 71.8, "High-variance sleeper", "The Moonshot", 5),
    (11, "ivaafay", 70.2, "Fringe contender", "The Bijan Build", None),
    (12, "deddybaba", 66.5, "Fragile", "The No-RB Experiment", None),
]

SLOTS = ["QB", "RB", "RB", "WR", "WR", "TE", "FLEX", "D/ST", "K"]
STARTERS = {  # exact draft.json player names, in slot order above
    "team-noor": ["Brock Purdy", "Breece Hall", "Kyren Williams", "Ja'Marr Chase", "Jaylen Waddle", "George Kittle", "Bucky Irving", "Patriots D/ST", "Tyler Loop"],
    "bizzy": ["Drake Maye", "Jonathan Taylor", "Kenneth Walker III", "Nico Collins", "Carnell Tate", "Colston Loveland", "TreVeyon Henderson", "Rams D/ST", "Cam Little"],
    "team-mbk": ["Dak Prescott", "Jahmyr Gibbs", "Josh Jacobs", "Drake London", "Tee Higgins", "Sam LaPorta", "David Montgomery", "Seahawks D/ST", "Harrison Mevis"],
    "bazan": ["Lamar Jackson", "James Cook III", "D'Andre Swift", "A.J. Brown", "Malik Nabers", "Juwan Johnson", "Michael Pittman Jr.", "Jaguars D/ST", "Chase McLaughlin"],
    "rambam": ["Jayden Daniels", "Chase Brown", "Travis Etienne Jr.", "CeeDee Lamb", "Emeka Egbuka", "Tyler Warren", "Rome Odunze", "Lions D/ST", "Cameron Dicker"],
    "mustafas-magnificent-team": ["Patrick Mahomes", "Omarion Hampton", "Saquon Barkley", "DeVonta Smith", "Ladd McConkey", "Isaiah Likely", "DJ Moore", "Ravens D/ST", "Jason Myers"],
    "hnfnr-aint-busy": ["Joe Burrow", "Derrick Henry", "Rhamondre Stevenson", "Jaxon Smith-Njigba", "Zay Flowers", "Brock Bowers", "Tony Pollard", "Eagles D/ST", "Evan McPherson"],
    "i-eat-ass": ["Jalen Hurts", "Christian McCaffrey", "Jeremiyah Love", "Chris Olave", "Jameson Williams", "Dallas Goedert", "Quinshon Judkins", "Steelers D/ST", "Eddy Pineiro"],
    "chief-sheikh": ["Justin Herbert", "Cam Skattebo", "Jaylen Warren", "Amon-Ra St. Brown", "Justin Jefferson", "Trey McBride", "Parker Washington", "Texans D/ST", "Brandon Aubrey"],
    "gang-green": ["Trevor Lawrence", "De'Von Achane", "Ashton Jeanty", "Garrett Wilson", "Tetairoa McMillan", "Harold Fannin Jr.", "Luther Burden III", "Jets D/ST", "Harrison Butker"],
    "ivaafay": ["Caleb Williams", "Bijan Robinson", "Javonte Williams", "George Pickens", "Davante Adams", "Kyle Pitts Sr.", "Jadarian Price", "Chargers D/ST", "Jake Bates"],
    "deddybaba": ["Josh Allen", "Bhayshul Tuten", "RJ Harvey", "Puka Nacua", "Rashee Rice", "Tucker Kraft", "Terry McLaurin", "Broncos D/ST", "Ka'imi Fairbairn"],
}

TEMP = 24.0
scores = {tid: s for _, tid, s, _, _, _ in BOARD}
exps = {t: math.exp(s / TEMP) for t, s in scores.items()}
total = sum(exps.values())
odds = {t: round(100 * e / total, 1) for t, e in exps.items()}
drift = round(100.0 - sum(odds.values()), 1)
fav = max(odds, key=odds.get)
odds[fav] = round(odds[fav] + drift, 1)

lo, hi = min(scores.values()), max(scores.values())
playoff = {t: 66.7 + (-1.2 + (s - lo) / (hi - lo) * 2.4) * 10 for t, s in scores.items()}
scale = 800 / sum(playoff.values())
playoff = {t: round(v * scale, 1) for t, v in playoff.items()}

def american(prob):
    p = prob / 100
    return f"+{round((1 - p) / p * 100 / 5) * 5}"

out = {"week": "preseason", "publishedAt": "2026-08-29", "deck": editorial["deck"], "teams": []}
for rank, tid, score, tier, archetype, ceiling in BOARD:
    players = drafted[tid]
    by_name = {p["player"]: p for p in players}
    starters, used = [], set()
    for slot, name in zip(SLOTS, STARTERS[tid]):
        p = by_name[name]  # KeyError = transcription mismatch, fail loudly
        starters.append({"slot": slot, "player": p["player"], "position": p["position"], "nflTeam": p["nflTeam"]})
        used.add(name)
    bench = [{"player": p["player"], "position": p["position"], "nflTeam": p["nflTeam"]}
             for p in sorted(players, key=lambda x: x["overall"]) if p["player"] not in used]
    assert len(bench) == 7, (tid, len(bench))

    e = editorial["preseason"][tid]
    out["teams"].append({
        "teamId": tid,
        "powerRank": rank,
        "powerScore": score,
        "titleOdds": odds[tid],
        "titleOddsAmerican": american(odds[tid]),
        "playoffOdds": playoff[tid],
        "draftGrade": grade_of[tid],
        "tier": tier,
        "archetype": archetype,
        **({"ceilingRank": ceiling} if ceiling else {}),
        "headline": e["headline"],
        "verdict": e["verdict"],
        "analysis": e["analysis"],
        "roster": {"starters": starters, "bench": bench},
    })

json.dump(out, open(f"{ROOT}/data/weeks/preseason.json", "w"), indent=2)
print("odds sum:", round(sum(t["titleOdds"] for t in out["teams"]), 1))
for t in out["teams"]:
    print(f'#{t["powerRank"]:>2} {t["teamId"]:<28} {t["powerScore"]:>5}  {t["titleOdds"]:>4}%  {t["draftGrade"]:<2} {t["tier"]}')

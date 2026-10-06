#!/usr/bin/env python3
"""Build data/weeks/week-4.json — the fourth in-season power snapshot.

Board: first week on the "Version B" results formula Rameel chose 2026-09-29:
results = 20% win% + 40% all-play% + 40% scoring vs league average (scaled from
the league low to the league high); blend = 0.7 x results + 0.3 x structure.
Power scores keep the blend's order on the familiar 65-89 scale.
Rosters: Week 4 lineups as played, transcribed from ESPN box scores
(final, 2026-10-06). IVaafay's capture dropped its offensive rows twice, so that
roster is omitted (rosterNote) until re-captured. HNFNR was re-shot and added.
"""
import json, math, os

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
grades = {t["teamId"]: t["grade"] for t in json.load(open(f"{ROOT}/data/draft-grades.json"))["teams"]}
teams_meta = {t["teamId"]: t for t in json.load(open(f"{ROOT}/data/teams.json"))["teams"]}
editorial = json.load(open(f"{ROOT}/scripts/editorial-week-4.json"))
schedule = json.load(open(f"{ROOT}/data/schedule.json"))

PRE_RANK = {"hnfnr-aint-busy": 1, "team-noor": 2, "team-mbk": 3, "chief-sheikh": 4,
            "bazan": 5, "gang-green": 6, "i-eat-ass": 7, "ivaafay": 8, "bizzy": 9,
            "mustafas-magnificent-team": 10, "rambam": 11, "deddybaba": 12}

# rank, teamId, powerScore, tier, ceilingRank
BOARD = [
    (1, "hnfnr-aint-busy", 89.0, "Favorite", 2),
    (2, "team-noor", 86.2, "Favorite", 1),
    (3, "team-mbk", 83.4, "Contender", 4),
    (4, "bizzy", 81.0, "Contender", 3),
    (5, "gang-green", 77.8, "Contender", 6),
    (6, "ivaafay", 76.6, "Playoff-caliber", 7),
    (7, "chief-sheikh", 74.8, "Playoff-caliber", 8),
    (8, "bazan", 73.2, "Playoff-caliber", 9),
    (9, "rambam", 71.8, "Playoff-caliber", 5),
    (10, "i-eat-ass", 71.0, "Fringe contender", 10),
    (11, "deddybaba", 66.4, "Fringe contender", 11),
    (12, "mustafas-magnificent-team", 65.2, "Fragile", 12),
]

ARCHETYPE = {"team-noor": "The Complete Team", "bizzy": "The RB Machine", "team-mbk": "The Floor Monster",
             "bazan": "The Nuclear Core", "rambam": "The Venture Portfolio",
             "mustafas-magnificent-team": "The Deep Bench", "hnfnr-aint-busy": "The Stars Up Top",
             "i-eat-ass": "The Volatility Bet", "chief-sheikh": "The WR Superteam",
             "gang-green": "The Moonshot", "ivaafay": "The Bijan Build", "deddybaba": "The No-RB Experiment"}

MOVEMENT = {
  "hnfnr-aint-busy": [(0.8, "4-0, 36-8 all-play, most points in the league"), (0.4, "Burrow's 428 yards"), (-0.6, "New formula compresses the top")],
  "team-noor": [(1.0, "Josh Allen acquired"), (-0.9, "Lost to the 0-3 team at 5-6 all-play"), (-0.7, "Chase in the concussion protocol")],
  "team-mbk": [(0.6, "30-14 all-play, second-best in the league"), (-0.8, "Loss at 6-5 all-play — unluckiest team"), (0.0, "Robinson's 25.2 on the bench")],
  "bizzy": [(4.6, "165.24 — the season's best score, 11-0 all-play"), (3.2, "Lamb, Collins and Walker all over 27"), (1.6, "Points now above the league average")],
  "gang-green": [(1.8, "3-1, second in the standings"), (1.4, "McMillan's 38.2 and Hubbard's 25.4"), (0.2, "Bryce Young producing against his old team")],
  "ivaafay": [(2.4, "128.72 at 10-1 all-play"), (1.6, "Back to 2-2 and the league scoring average"), (0.6, "Watson covering for Caleb")],
  "chief-sheikh": [(-3.4, "72.82 — the week's lowest score, 0-11 all-play"), (-1.6, "Jefferson on IR to about Week 8"), (-0.8, "Points now below the league average")],
  "bazan": [(-2.6, "Loss at 2-9 all-play"), (-1.8, "Lamar's sprained ankle"), (-1.2, "Monangai's 27.5 benched; Coker and Mitchell out")],
  "rambam": [(2.8, "First win, 7-4 all-play"), (1.4, "Taylor, Wilson and Stroud all over 22"), (0.8, "Daniels expected back this week"), (-0.8, "Etienne to IR")],
  "i-eat-ass": [(-1.6, "Third straight loss, 1-3"), (-0.8, "520.3 points allowed, most in the league"), (-0.4, "Hurts' 93 passing yards")],
  "deddybaba": [(0.8, "IHOP Bowl win, Puka back"), (-0.9, "Josh Allen traded away"), (-0.5, "Rice's hamstring")],
  "mustafas-magnificent-team": [(-2.4, "74.6 at 1-10 all-play, last in the standings"), (-1.8, "Barkley's hamstring, Weeks 6-8"), (-1.0, "McConkey, Moore and Kelce combined for 4.7")],
}

STOCK = {
  "hnfnr-aint-busy": ("Joe Burrow", "Eagles D/ST"),
  "team-noor": ("Kyren Williams", "Ja'Marr Chase"),
  "team-mbk": ("Tee Higgins", "David Montgomery"),
  "bizzy": ("CeeDee Lamb", "Tyler Shough"),
  "gang-green": ("Tetairoa McMillan", "Garrett Wilson"),
  "ivaafay": ("Deshaun Watson", "Caleb Williams"),
  "chief-sheikh": ("Jaylen Warren", "Justin Jefferson"),
  "bazan": ("Kyle Monangai", "Lamar Jackson"),
  "rambam": ("Emanuel Wilson", "Travis Etienne Jr."),
  "i-eat-ass": ("Quinshon Judkins", "Jalen Hurts"),
  "deddybaba": ("Puka Nacua", "Rashee Rice"),
  "mustafas-magnificent-team": ("Will Reichard", "Saquon Barkley"),
}

DEVELOPMENT = {
  "hnfnr-aint-busy": "4-0 after a 54-point win over Kashir; Burrow threw for 428.",
  "team-noor": "Traded for Josh Allen, survived the veto by one vote, lost to the commissioner.",
  "team-mbk": "Lost at 6-5 all-play; now the unluckiest team in the league.",
  "bizzy": "165.24 — the season's best score — with Lamb, Collins and Walker. First weekly hundo.",
  "gang-green": "McMillan's 38.2 and Hubbard's 25.4 lifted GG to 3-1, second in the standings.",
  "ivaafay": "Beat MBK with Watson at QB, then dropped Penix for Joe Mixon.",
  "chief-sheikh": "72.82, the week's lowest score; Jefferson to IR.",
  "bazan": "Benched Monangai's 27.5; Lamar sprained an ankle and left in a boot.",
  "rambam": "First win — Taylor 22.2, Wilson 25.5 — in the week Lamb scored 32.8 for Bizzy.",
  "i-eat-ass": "Third straight loss; 520.3 points allowed, most in the league.",
  "deddybaba": "Traded Josh Allen for Purdy and Bucky, then won the IHOP Bowl with Purdy.",
  "mustafas-magnificent-team": "74.6 and last in the standings; Barkley out Weeks 6-8.",
}

S = ["QB", "RB", "RB", "WR", "WR", "TE", "FLEX", "D/ST", "K"]
def P(name, pos, nfl): return {"player": name, "position": pos, "nflTeam": nfl}
ROSTERS = {
 "rambam": {
   "starters": [P("C.J. Stroud","QB","HOU"),P("Emanuel Wilson","RB","SEA"),P("Jonathan Taylor","RB","IND"),P("Matthew Golden","WR","GB"),P("Kalif Raymond","WR","CHI"),P("Tyler Warren","TE","IND"),P("TreVeyon Henderson","RB","NE"),P("Packers D/ST","D/ST","GB"),P("Spencer Shrader","K","IND")],
   "bench": [P("Emeka Egbuka","WR","TB"),P("Rome Odunze","WR","CHI"),P("Jayden Daniels","QB","WSH"),P("Xavier Worthy","WR","KC"),P("Kaelon Black","RB","SF"),P("Chris Rodriguez Jr.","RB","JAX"),P("Travis Etienne Jr. (IR)","RB","NO"),P("Jonathon Brooks (IR)","RB","CAR")]},
 "hnfnr-aint-busy": {
   "starters": [P("Joe Burrow","QB","CIN"),P("Derrick Henry","RB","BAL"),P("Tony Pollard","RB","TEN"),P("Jaxon Smith-Njigba","WR","SEA"),P("Zay Flowers","WR","BAL"),P("Brock Bowers","TE","LV"),P("Michael Wilson","WR","ARI"),P("Eagles D/ST","D/ST","PHI"),P("Cameron Dicker","K","LAC")],
   "bench": [P("Rhamondre Stevenson","RB","NE"),P("Brian Thomas Jr.","WR","JAX"),P("Jacory Croskey-Merritt","RB","WSH"),P("Tyler Allgeier","RB","ARI"),P("Dalton Kincaid","TE","BUF"),P("Dalton Schultz","TE","HOU"),P("Denzel Boston","WR","CLE"),P("Jayden Reed (IR)","WR","GB")]},
 "team-noor": {
   "starters": [P("Josh Allen","QB","BUF"),P("Kyren Williams","RB","LAR"),P("Aaron Jones Sr.","RB","MIN"),P("Ja'Marr Chase","WR","CIN"),P("Christian Watson","WR","GB"),P("George Kittle","TE","SF"),P("Jaylen Waddle","WR","DEN"),P("Raiders D/ST","D/ST","LV"),P("Tyler Loop","K","BAL")],
   "bench": [P("Breece Hall","RB","NYJ"),P("J.K. Dobbins","RB","DEN"),P("Mark Andrews","TE","BAL"),P("Jared Goff","QB","DET"),P("Tre Tucker","WR","LV"),P("Patriots D/ST","D/ST","NE"),P("Demarcus Robinson (IR)","WR","SF")]},
 "i-eat-ass": {
   "starters": [P("Jalen Hurts","QB","PHI"),P("Christian McCaffrey","RB","SF"),P("Jeremiyah Love","RB","ARI"),P("Chris Olave","WR","NO"),P("Jakobi Meyers","WR","JAX"),P("T.J. Hockenson","TE","MIN"),P("Quinshon Judkins","RB","CLE"),P("Steelers D/ST","D/ST","PIT"),P("Eddy Pineiro","K","SF")],
   "bench": [P("Jameson Williams","WR","DET"),P("Dallas Goedert","TE","PHI"),P("Woody Marks","RB","HOU"),P("Devaughn Vele","WR","NO"),P("Carnell Tate","WR","TEN"),P("Keenan Allen","WR","IND"),P("Zach Ertz","TE","PHI")]},
 "bizzy": {
   "starters": [P("Tyler Shough","QB","NO"),P("Kenneth Walker III","RB","KC"),P("Chase Brown","RB","CIN"),P("Nico Collins","WR","HOU"),P("CeeDee Lamb","WR","DAL"),P("Colston Loveland","TE","CHI"),P("Deebo Samuel Sr.","WR","SF"),P("Ravens D/ST","D/ST","BAL"),P("Cam Little","K","JAX")],
   "bench": [P("Drake Maye","QB","NE"),P("Rachaad White","RB","WSH"),P("Malik Washington","WR","MIA"),P("Emmett Johnson","RB","KC"),P("Samaje Perine","RB","CIN"),P("Najee Harris","RB","NYG"),P("Rams D/ST","D/ST","LAR"),P("Alec Pierce (IR)","WR","IND")]},
 "bazan": {
   "starters": [P("Lamar Jackson","QB","BAL"),P("James Cook III","RB","BUF"),P("D'Andre Swift","RB","CHI"),P("Malik Nabers","WR","NYG"),P("Dontayvion Wicks","WR","PHI"),P("Juwan Johnson","TE","NO"),P("George Holani","RB","SEA"),P("Browns D/ST","D/ST","CLE"),P("Chase McLaughlin","K","TB")],
   "bench": [P("Michael Pittman Jr.","WR","PIT"),P("Kyle Monangai","RB","CHI"),P("Bo Nix","QB","DEN"),P("Jalen Coker","WR","CAR"),P("Ray Davis","RB","BUF"),P("Adonai Mitchell","WR","NYJ"),P("Commanders D/ST","D/ST","WSH"),P("A.J. Brown (IR)","WR","NE")]},
 "gang-green": {
   "starters": [P("Bryce Young","QB","CAR"),P("Ashton Jeanty","RB","LV"),P("Chuba Hubbard","RB","CAR"),P("Garrett Wilson","WR","NYJ"),P("Tetairoa McMillan","WR","CAR"),P("Harold Fannin Jr.","TE","CLE"),P("Kenyon Sadiq","TE","NYJ"),P("Jets D/ST","D/ST","NYJ"),P("Harrison Butker","K","KC")],
   "bench": [P("Luther Burden III","WR","CHI"),P("Stefon Diggs","WR","WSH"),P("Mike Washington Jr.","RB","LV"),P("Keaton Mitchell","RB","LAC"),P("Trevor Lawrence","QB","JAX"),P("Jaylen Wright","RB","MIA"),P("MarShawn Lloyd","RB","GB"),P("Jordyn Tyson (IR)","WR","NO")]},
 "deddybaba": {
   "starters": [P("Brock Purdy","QB","SF"),P("Bhayshul Tuten","RB","JAX"),P("Bucky Irving","RB","TB"),P("Puka Nacua","WR","LAR"),P("Josh Downs","WR","IND"),P("Tucker Kraft","TE","GB"),P("Rashee Rice","WR","KC"),P("Bills D/ST","D/ST","BUF"),P("Ka'imi Fairbairn","K","HOU")],
   "bench": [P("Terry McLaurin","WR","WSH"),P("RJ Harvey","RB","DEN"),P("Kenny Gainwell","RB","TB"),P("Tyjae Spears","RB","TEN"),P("Ollie Gordon II","RB","MIA"),P("Tre' Harris","WR","LAC"),P("Broncos D/ST","D/ST","DEN"),P("Christian Kirk (IR)","WR","SF")]},
 "mustafas-magnificent-team": {
   "starters": [P("Patrick Mahomes","QB","KC"),P("Omarion Hampton","RB","LAC"),P("Saquon Barkley","RB","PHI"),P("Ladd McConkey","WR","LAC"),P("DJ Moore","WR","BUF"),P("Travis Kelce","TE","KC"),P("Isaiah Likely","TE","NYG"),P("Vikings D/ST","D/ST","MIN"),P("Will Reichard","K","MIN")],
   "bench": [P("DeVonta Smith","WR","PHI"),P("Marvin Harrison Jr.","WR","ARI"),P("Kyler Murray","QB","MIN"),P("Tyreek Hill","WR","FA"),P("Mack Hollins","WR","NE"),P("Justice Hill","RB","BAL"),P("Jason Myers","K","SEA"),P("Zach Charbonnet (IR)","RB","SEA")]},
 "chief-sheikh": {
   "starters": [P("Sam Darnold","QB","SEA"),P("Cam Skattebo","RB","NYG"),P("Jaylen Warren","RB","PIT"),P("Amon-Ra St. Brown","WR","DET"),P("Parker Washington","WR","JAX"),P("Trey McBride","TE","ARI"),P("Braelon Allen","RB","NYJ"),P("Chiefs D/ST","D/ST","KC"),P("Brandon Aubrey","K","DAL")],
   "bench": [P("Blake Corum","RB","LAR"),P("Tank Bigsby","RB","PHI"),P("Jordan Love","QB","GB"),P("Jake Ferguson","TE","DAL"),P("Kendre Miller","RB","NO"),P("Isaiah Davis","RB","NYJ"),P("Texans D/ST","D/ST","HOU"),P("Justin Jefferson (IR)","WR","MIN")]},
 "team-mbk": {
   "starters": [P("Dak Prescott","QB","DAL"),P("Jahmyr Gibbs","RB","DET"),P("David Montgomery","RB","HOU"),P("Drake London","WR","ATL"),P("Tee Higgins","WR","CIN"),P("Sam LaPorta","TE","DET"),P("Tyler Higbee","TE","LAR"),P("Seahawks D/ST","D/ST","SEA"),P("Evan McPherson","K","CIN")],
   "bench": [P("Mike Evans","WR","SF"),P("Rico Dowdle","RB","PIT"),P("Wan'Dale Robinson","WR","TEN"),P("Brian Robinson Jr.","RB","ATL"),P("Matthew Stafford","QB","LAR"),P("KC Concepcion","WR","CLE"),P("Chris Godwin Jr.","WR","TB"),P("Josh Jacobs (IR)","RB","GB")]},
}
for tid, r in ROSTERS.items():
    slots = [{"slot": s, **p} for s, p in zip(S, r["starters"])]
    ROSTERS[tid] = {"starters": slots, "bench": r["bench"]}
ROSTER_NOTE = {
  "ivaafay": "The Week 4 lineup didn't survive the ESPN screenshot (twice). Known: Watson 12.92, Bijan Robinson 27.2, Bates 18.0, Bears D/ST 9.0; the rest is pending re-capture.",
}

# cumulative records + PF from all results through week 4
rec = {t: {"wins": 0, "losses": 0} for t in PRE_RANK}
pf = {t: 0.0 for t in PRE_RANK}
for wk in (1, 2, 3, 4):
    results = json.load(open(f"{ROOT}/data/results/week-{wk}.json"))
    for m in results["matchups"]:
        hw = m["homeScore"] > m["awayScore"]
        rec[m["homeTeamId"]]["wins" if hw else "losses"] += 1
        rec[m["awayTeamId"]]["losses" if hw else "wins"] += 1
        pf[m["homeTeamId"]] = round(pf[m["homeTeamId"]] + m["homeScore"], 2)
        pf[m["awayTeamId"]] = round(pf[m["awayTeamId"]] + m["awayScore"], 2)

# odds + playoff odds from new power scores
TEMP = 24.0
scores = {tid: s for _, tid, s, _, _ in BOARD}
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

def american(p):
    return f"+{round((1 - p/100) / (p/100) * 100 / 5) * 5}"

# next matchup from week 5 schedule
nxt = {}
for m in schedule["weeks"]["5"]:
    nxt[m["away"]] = f'at {teams_meta[m["home"]]["teamName"]}'
    nxt[m["home"]] = f'vs {teams_meta[m["away"]]["teamName"]}'

out = {"week": 4, "publishedAt": "2026-10-06", "deck": editorial["deck"], "teams": []}
for rank, tid, score, tier, ceiling in BOARD:
    e = editorial["teams"][tid]
    up, down = STOCK[tid]
    row = {
        "teamId": tid, "powerRank": rank, "previousPowerRank": PRE_RANK[tid],
        "powerScore": score, "titleOdds": odds[tid], "titleOddsAmerican": american(odds[tid]),
        "playoffOdds": playoff[tid], "draftGrade": grades[tid], "tier": tier,
        "archetype": ARCHETYPE[tid], "ceilingRank": ceiling,
        "record": rec[tid], "pointsFor": pf[tid],
        "stockUp": up, "stockDown": down, "biggestDevelopment": DEVELOPMENT[tid],
        "nextMatchup": nxt[tid],
        "movementReasons": [{"delta": d, "reason": r} for d, r in MOVEMENT[tid]],
        "headline": e["headline"], "verdict": e["verdict"], "analysis": e["analysis"],
    }
    if tid in ROSTERS:
        row["roster"] = ROSTERS[tid]
    else:
        row["rosterNote"] = ROSTER_NOTE[tid]
    out["teams"].append(row)

json.dump(out, open(f"{ROOT}/data/weeks/week-4.json", "w"), indent=2)
print("odds sum:", round(sum(t["titleOdds"] for t in out["teams"]), 1))
print("playoff sum:", round(sum(t["playoffOdds"] for t in out["teams"]), 1))
for t in out["teams"]:
    mv = PRE_RANK[t["teamId"]] - t["powerRank"]
    delta_sum = round(sum(m["delta"] for m in t["movementReasons"]), 1)
    print(f'#{t["powerRank"]:>2} {t["teamId"]:<28} {"↑" + str(mv) if mv > 0 else "↓" + str(-mv) if mv < 0 else "—":>3}  {t["powerScore"]:>5}  {t["titleOdds"]:>4}%  {t["record"]["wins"]}-{t["record"]["losses"]}  PF {t["pointsFor"]:>6}  Δreasons {delta_sum}')

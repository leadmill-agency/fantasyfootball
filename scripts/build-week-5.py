#!/usr/bin/env python3
"""Build data/weeks/week-5.json — the fifth in-season power snapshot.

Board: Version B formula (results = 20% win% + 40% all-play% + 40% scoring vs
league average; blend 70/30 with structure) plus two commissioner overrides on
2026-10-13: Gang Green to 3rd (4-1, second in the standings; the formula alone
had 5th) and RN over I Eat Ass at 11/12 (RN won with seven injured starters).
Rosters: Week 5 lineups as played, from the ESPN box scores (final, 2026-10-13).
"""
import json, math, os

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
grades = {t["teamId"]: t["grade"] for t in json.load(open(f"{ROOT}/data/draft-grades.json"))["teams"]}
teams_meta = {t["teamId"]: t for t in json.load(open(f"{ROOT}/data/teams.json"))["teams"]}
editorial = json.load(open(f"{ROOT}/scripts/editorial-week-5.json"))
schedule = json.load(open(f"{ROOT}/data/schedule.json"))

PRE_RANK = {"hnfnr-aint-busy": 1, "team-noor": 2, "team-mbk": 3, "bizzy": 4, "gang-green": 5,
            "ivaafay": 6, "chief-sheikh": 7, "bazan": 8, "rambam": 9, "i-eat-ass": 10,
            "deddybaba": 11, "mustafas-magnificent-team": 12}

# rank, teamId, powerScore, tier, ceilingRank
BOARD = [
    (1, "hnfnr-aint-busy", 89.4, "Favorite", 2),
    (2, "team-noor", 86.0, "Favorite", 1),
    (3, "gang-green", 82.6, "Contender", 7),
    (4, "team-mbk", 82.2, "Contender", 3),
    (5, "chief-sheikh", 81.6, "Contender", 5),
    (6, "rambam", 77.6, "Playoff-caliber", 4),
    (7, "ivaafay", 76.2, "Playoff-caliber", 9),
    (8, "bizzy", 75.0, "Playoff-caliber", 6),
    (9, "deddybaba", 73.4, "Playoff-caliber", 8),
    (10, "bazan", 69.6, "Fringe contender", 10),
    (11, "mustafas-magnificent-team", 66.2, "Fringe contender", 12),
    (12, "i-eat-ass", 65.4, "Fragile", 11),
]

ARCHETYPE = {"team-noor": "The Complete Team", "bizzy": "The RB Machine", "team-mbk": "The Floor Monster",
             "bazan": "The Nuclear Core", "rambam": "The Venture Portfolio",
             "mustafas-magnificent-team": "The Deep Bench", "hnfnr-aint-busy": "The Stars Up Top",
             "i-eat-ass": "The Volatility Bet", "chief-sheikh": "The WR Superteam",
             "gang-green": "The Moonshot", "ivaafay": "The Bijan Build", "deddybaba": "The No-RB Experiment"}

MOVEMENT = {
  "hnfnr-aint-busy": [(1.0, "5-0, 43-12 all-play"), (0.4, "Bowers, Henry and Smith-Njigba all over 19"), (-1.0, "Burrow on bye in Week 6 with no backup")],
  "team-noor": [(1.2, "139.0 — second-best score of the week; most points in the league"), (-1.4, "Third straight loss; unluckiest team in the league")],
  "gang-green": [(2.6, "4-1, second in the standings"), (1.4, "Won with Young, McMillan and Hubbard on bye"), (0.8, "Lloyd and Lawrence covered the byes")],
  "team-mbk": [(0.8, "Gibbs' 35.2"), (-1.4, "Second straight loss at 6-5 all-play"), (-0.6, "Stafford benched a fifth straight week")],
  "chief-sheikh": [(3.2, "148.36 — the weekly high, 11-0 all-play"), (2.2, "Jefferson back from IR"), (1.4, "Warren's 33.8, Washington's 27.4")],
  "rambam": [(2.4, "Second straight win, 8-3 all-play"), (2.6, "Daniels back with 32.26"), (0.8, "Shrader and Warren producing")],
  "ivaafay": [(0.6, "28-27 all-play, still above water"), (-1.0, "Loss to the No. 1 team at 5-6 all-play")],
  "bizzy": [(-3.0, "80.16 at 1-10 all-play"), (-2.2, "Lamb's quad, Deebo's hamstring"), (-1.6, "Points fell below the league average"), (0.8, "Maye's four touchdowns")],
  "deddybaba": [(3.4, "147.56 at 10-1 all-play"), (2.4, "Bucky 30.5, Puka 29.2 — the trade is paying"), (1.2, "3-2, fourth in the standings")],
  "bazan": [(-1.8, "Loss at 2-9 all-play"), (-1.0, "Lamar still out; Rodgers starting"), (-0.8, "26 roster moves; Cowboys D/ST at −2.0")],
  "mustafas-magnificent-team": [(1.8, "Won with seven injured players and two on bye"), (-0.8, "15-40 all-play, fewest points in the league")],
  "i-eat-ass": [(-2.4, "75.3 — the week's lowest score, 0-11 all-play"), (-1.8, "Four straight losses, 1-4"), (-1.4, "643.96 points allowed, most in the league")],
}

STOCK = {
  "hnfnr-aint-busy": ("Brock Bowers", "Michael Wilson"),
  "team-noor": ("Christian Watson", "Jaylen Waddle"),
  "gang-green": ("MarShawn Lloyd", "Harold Fannin Jr."),
  "team-mbk": ("Jahmyr Gibbs", "Tee Higgins"),
  "chief-sheikh": ("Jaylen Warren", "Brandon Aubrey"),
  "rambam": ("Jayden Daniels", "Jonathan Taylor"),
  "ivaafay": ("George Pickens", "Bears D/ST"),
  "bizzy": ("Drake Maye", "CeeDee Lamb"),
  "deddybaba": ("Bucky Irving", "Josh Downs"),
  "bazan": ("Malik Nabers", "Cowboys D/ST"),
  "mustafas-magnificent-team": ("Isaiah Likely", "Omarion Hampton"),
  "i-eat-ass": ("Mike Evans", "Jeremiyah Love"),
}

DEVELOPMENT = {
  "hnfnr-aint-busy": "5-0 and 43-12 all-play; Burrow is on bye next week with no backup QB.",
  "team-noor": "Scored 139.0 and lost; Dobbins' 14.4 on the bench would have won it.",
  "gang-green": "Won with three Panthers on bye; Lloyd, the Ivan castoff, scored 16.2.",
  "team-mbk": "Traded Evans and Montgomery for Judkins; Stafford's 27.32 benched again.",
  "chief-sheikh": "148.36, the weekly hundo, with Jefferson back from IR.",
  "rambam": "Daniels returned with 32.26; Roman Wilson's 0.0 started over Egbuka's 14.2.",
  "ivaafay": "Lost to the unbeaten team; the Bears D/ST scored −2.0.",
  "bizzy": "Maye threw four TDs for 39.46; the other eight starters combined for 40.7.",
  "deddybaba": "147.56 — 0.80 short of the weekly hundo. Bucky 30.5, Puka 29.2.",
  "bazan": "26 roster moves; started Rodgers and the Cowboys D/ST (−2.0).",
  "mustafas-magnificent-team": "Won with seven injured starters and two on bye; Brissett 24.78 off waivers.",
  "i-eat-ass": "75.3, the week's lowest; Evans scored 22.8 in his debut from the trade.",
}

S = ["QB", "RB", "RB", "WR", "WR", "TE", "FLEX", "D/ST", "K"]
def P(name, pos, nfl): return {"player": name, "position": pos, "nflTeam": nfl}
ROSTERS = {
 "rambam": {
   "starters": [P("Jayden Daniels","QB","WSH"),P("Emanuel Wilson","RB","SEA"),P("Jonathan Taylor","RB","IND"),P("Matthew Golden","WR","GB"),P("Roman Wilson","WR","PIT"),P("Tyler Warren","TE","IND"),P("TreVeyon Henderson","RB","NE"),P("Bengals D/ST","D/ST","CIN"),P("Spencer Shrader","K","IND")],
   "bench": [P("Emeka Egbuka","WR","TB"),P("Rome Odunze","WR","CHI"),P("Xavier Worthy","WR","KC"),P("Kaelon Black","RB","SF"),P("Kalif Raymond","WR","CHI"),P("C.J. Stroud","QB","HOU"),P("Jonathon Brooks (IR)","RB","CAR"),P("Travis Etienne Jr. (IR)","RB","NO")]},
 "i-eat-ass": {
   "starters": [P("Jalen Hurts","QB","PHI"),P("Christian McCaffrey","RB","SF"),P("Jeremiyah Love","RB","ARI"),P("Chris Olave","WR","NO"),P("Carnell Tate","WR","TEN"),P("Dallas Goedert","TE","PHI"),P("Mike Evans","WR","SF"),P("Steelers D/ST","D/ST","PIT"),P("Eddy Pineiro","K","SF")],
   "bench": [P("Jameson Williams","WR","DET"),P("Woody Marks","RB","HOU"),P("Devaughn Vele","WR","NO"),P("T.J. Hockenson","TE","MIN"),P("Kirk Cousins","QB","LV"),P("David Montgomery","RB","HOU"),P("Jakobi Meyers","WR","JAX")]},
 "bizzy": {
   "starters": [P("Drake Maye","QB","NE"),P("Chase Brown","RB","CIN"),P("Will Shipley","RB","PHI"),P("Nico Collins","WR","HOU"),P("CeeDee Lamb","WR","DAL"),P("Colston Loveland","TE","CHI"),P("Deebo Samuel Sr.","WR","SF"),P("Jaguars D/ST","D/ST","JAX"),P("Cam Little","K","JAX")],
   "bench": [P("Kenneth Walker III","RB","KC"),P("Rachaad White","RB","WSH"),P("Rams D/ST","D/ST","LAR"),P("Tyler Shough","QB","NO"),P("Malik Washington","WR","MIA"),P("Emmett Johnson","RB","KC"),P("Samaje Perine","RB","CIN"),P("Alec Pierce (IR)","WR","IND")]},
 "gang-green": {
   "starters": [P("Trevor Lawrence","QB","JAX"),P("Ashton Jeanty","RB","LV"),P("Keaton Mitchell","RB","LAC"),P("Garrett Wilson","WR","NYJ"),P("Luther Burden III","WR","CHI"),P("Harold Fannin Jr.","TE","CLE"),P("MarShawn Lloyd","RB","GB"),P("Jets D/ST","D/ST","NYJ"),P("Chase McLaughlin","K","TB")],
   "bench": [P("Tetairoa McMillan","WR","CAR"),P("Chuba Hubbard","RB","CAR"),P("Stefon Diggs","WR","WSH"),P("Mike Washington Jr.","RB","LV"),P("Kenyon Sadiq","TE","NYJ"),P("Bryce Young","QB","CAR"),P("Jaylen Wright","RB","MIA"),P("Jordyn Tyson (IR)","WR","NO")]},
 "mustafas-magnificent-team": {
   "starters": [P("Jacoby Brissett","QB","ARI"),P("Omarion Hampton","RB","LAC"),P("Chris Rodriguez Jr.","RB","JAX"),P("Romeo Doubs","WR","NE"),P("Courtland Sutton","WR","DEN"),P("Isaiah Likely","TE","NYG"),P("Rashid Shaheed","WR","SEA"),P("Vikings D/ST","D/ST","MIN"),P("Will Reichard","K","MIN")],
   "bench": [P("Saquon Barkley","RB","PHI"),P("DeVonta Smith","WR","PHI"),P("Ladd McConkey","WR","LAC"),P("DJ Moore","WR","BUF"),P("Marvin Harrison Jr.","WR","HOU"),P("Patrick Mahomes","QB","KC"),P("Travis Kelce","TE","KC"),P("Zach Charbonnet (IR)","RB","SEA")]},
 "bazan": {
   "starters": [P("Aaron Rodgers","QB","PIT"),P("James Cook III","RB","BUF"),P("D'Andre Swift","RB","CHI"),P("Malik Nabers","WR","NYG"),P("Isaac TeSlaa","WR","DET"),P("Juwan Johnson","TE","NO"),P("Antonio Williams","WR","WSH"),P("Cowboys D/ST","D/ST","DAL"),P("Chad Ryland","K","ARI")],
   "bench": [P("Lamar Jackson","QB","BAL"),P("Kyle Monangai","RB","CHI"),P("Jalen Coker","WR","CAR"),P("Ray Davis","RB","BUF"),P("Adonai Mitchell","WR","NYJ"),P("Dameon Pierce","RB","PHI"),P("Ravens D/ST","D/ST","BAL"),P("A.J. Brown (IR)","WR","NE")]},
 "chief-sheikh": {
   "starters": [P("Kyler Murray","QB","MIN"),P("Cam Skattebo","RB","NYG"),P("Jaylen Warren","RB","PIT"),P("Amon-Ra St. Brown","WR","DET"),P("Parker Washington","WR","JAX"),P("Trey McBride","TE","ARI"),P("Justin Jefferson","WR","MIN"),P("Texans D/ST","D/ST","HOU"),P("Brandon Aubrey","K","DAL")],
   "bench": [P("Blake Corum","RB","LAR"),P("Braelon Allen","RB","NYJ"),P("Jordan Love","QB","GB"),P("Jake Ferguson","TE","DAL"),P("Chiefs D/ST","D/ST","KC"),P("Jaleel McLaughlin","RB","CLE"),P("Najee Harris","RB","NYG")]},
 "team-noor": {
   "starters": [P("Josh Allen","QB","BUF"),P("Kyren Williams","RB","LAR"),P("Aaron Jones Sr.","RB","MIN"),P("Ja'Marr Chase","WR","CIN"),P("Christian Watson","WR","GB"),P("George Kittle","TE","SF"),P("Jaylen Waddle","WR","DEN"),P("Patriots D/ST","D/ST","NE"),P("Tyler Loop","K","BAL")],
   "bench": [P("Breece Hall","RB","NYJ"),P("J.K. Dobbins","RB","DEN"),P("Mark Andrews","TE","BAL"),P("Jared Goff","QB","DET"),P("Tre Tucker","WR","LV"),P("Raiders D/ST","D/ST","LV"),P("Keon Coleman","WR","BUF"),P("Demarcus Robinson (IR)","WR","SF")]},
 "team-mbk": {
   "starters": [P("Dak Prescott","QB","DAL"),P("Jahmyr Gibbs","RB","DET"),P("Quinshon Judkins","RB","CLE"),P("Drake London","WR","ATL"),P("Tee Higgins","WR","CIN"),P("Sam LaPorta","TE","DET"),P("Mike Gesicki","TE","CIN"),P("Falcons D/ST","D/ST","ATL"),P("Evan McPherson","K","CIN")],
   "bench": [P("Rico Dowdle","RB","PIT"),P("Seahawks D/ST","D/ST","SEA"),P("Wan'Dale Robinson","WR","TEN"),P("Brian Robinson Jr.","RB","ATL"),P("Matthew Stafford","QB","LAR"),P("KC Concepcion","WR","CLE"),P("Tank Dell (IR)","WR","HOU"),P("Josh Jacobs (IR)","RB","GB")]},
 "deddybaba": {
   "starters": [P("Brock Purdy","QB","SF"),P("Bhayshul Tuten","RB","JAX"),P("Bucky Irving","RB","TB"),P("Puka Nacua","WR","LAR"),P("Josh Downs","WR","IND"),P("Tucker Kraft","TE","GB"),P("Ollie Gordon II","RB","MIA"),P("Broncos D/ST","D/ST","DEN"),P("Ka'imi Fairbairn","K","HOU")],
   "bench": [P("Rashee Rice","WR","KC"),P("Terry McLaurin","WR","WSH"),P("RJ Harvey","RB","DEN"),P("Kenny Gainwell","RB","TB"),P("Tyjae Spears","RB","TEN"),P("Tre' Harris","WR","LAC"),P("Roschon Johnson","RB","CHI"),P("Christian Kirk (IR)","WR","SF")]},
 "ivaafay": {
   "starters": [P("Deshaun Watson","QB","CLE"),P("Bijan Robinson","RB","ATL"),P("Javonte Williams","RB","DAL"),P("George Pickens","WR","DAL"),P("Davante Adams","WR","LAR"),P("Kyle Pitts Sr.","TE","ATL"),P("DK Metcalf","WR","PIT"),P("Bears D/ST","D/ST","CHI"),P("Jake Bates","K","DET")],
   "bench": [P("Caleb Williams","QB","CHI"),P("Jordan Addison","WR","MIN"),P("Alvin Kamara","RB","NO"),P("Khalil Shakir","WR","BUF"),P("Kaleb Johnson","RB","GB"),P("Brenton Strange","TE","JAX"),P("Jadarian Price (IR)","RB","SEA"),P("Jordan Mason (IR)","RB","MIN")]},
 "hnfnr-aint-busy": {
   "starters": [P("Joe Burrow","QB","CIN"),P("Derrick Henry","RB","BAL"),P("Tony Pollard","RB","TEN"),P("Jaxon Smith-Njigba","WR","SEA"),P("Michael Wilson","WR","ARI"),P("Brock Bowers","TE","LV"),P("Zay Flowers","WR","BAL"),P("Browns D/ST","D/ST","CLE"),P("Cameron Dicker","K","LAC")],
   "bench": [P("Rhamondre Stevenson","RB","NE"),P("Brian Thomas Jr.","WR","JAX"),P("Jacory Croskey-Merritt","RB","WSH"),P("Tyler Allgeier","RB","ARI"),P("Dalton Kincaid","TE","BUF"),P("Dalton Schultz","TE","HOU"),P("Denzel Boston","WR","CLE"),P("Jonah Coleman (IR)","RB","DEN")]},
}
for tid, r in ROSTERS.items():
    slots = [{"slot": s, **p} for s, p in zip(S, r["starters"])]
    ROSTERS[tid] = {"starters": slots, "bench": r["bench"]}

# cumulative records + PF from all results through week 5
rec = {t: {"wins": 0, "losses": 0} for t in PRE_RANK}
pf = {t: 0.0 for t in PRE_RANK}
for wk in (1, 2, 3, 4, 5):
    results = json.load(open(f"{ROOT}/data/results/week-{wk}.json"))
    for m in results["matchups"]:
        hw = m["homeScore"] > m["awayScore"]
        rec[m["homeTeamId"]]["wins" if hw else "losses"] += 1
        rec[m["awayTeamId"]]["losses" if hw else "wins"] += 1
        pf[m["homeTeamId"]] = round(pf[m["homeTeamId"]] + m["homeScore"], 2)
        pf[m["awayTeamId"]] = round(pf[m["awayTeamId"]] + m["awayScore"], 2)

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

nxt = {}
for m in schedule["weeks"]["6"]:
    nxt[m["away"]] = f'at {teams_meta[m["home"]]["teamName"]}'
    nxt[m["home"]] = f'vs {teams_meta[m["away"]]["teamName"]}'

out = {"week": 5, "publishedAt": "2026-10-13", "deck": editorial["deck"], "teams": []}
for rank, tid, score, tier, ceiling in BOARD:
    e = editorial["teams"][tid]
    up, down = STOCK[tid]
    out["teams"].append({
        "teamId": tid, "powerRank": rank, "previousPowerRank": PRE_RANK[tid],
        "powerScore": score, "titleOdds": odds[tid], "titleOddsAmerican": american(odds[tid]),
        "playoffOdds": playoff[tid], "draftGrade": grades[tid], "tier": tier,
        "archetype": ARCHETYPE[tid], "ceilingRank": ceiling,
        "record": rec[tid], "pointsFor": pf[tid],
        "stockUp": up, "stockDown": down, "biggestDevelopment": DEVELOPMENT[tid],
        "nextMatchup": nxt[tid],
        "movementReasons": [{"delta": d, "reason": r} for d, r in MOVEMENT[tid]],
        "headline": e["headline"], "verdict": e["verdict"], "analysis": e["analysis"],
        "roster": ROSTERS[tid],
    })

json.dump(out, open(f"{ROOT}/data/weeks/week-5.json", "w"), indent=2)
print("odds sum:", round(sum(t["titleOdds"] for t in out["teams"]), 1))
for t in out["teams"]:
    mv = PRE_RANK[t["teamId"]] - t["powerRank"]
    delta_sum = round(sum(m["delta"] for m in t["movementReasons"]), 1)
    print(f'#{t["powerRank"]:>2} {t["teamId"]:<28} {"↑" + str(mv) if mv > 0 else "↓" + str(-mv) if mv < 0 else "—":>3}  {t["powerScore"]:>5}  {t["titleOdds"]:>4}%  {t["record"]["wins"]}-{t["record"]["losses"]}  PF {t["pointsFor"]:>6}  Δreasons {delta_sum}')

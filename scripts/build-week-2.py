#!/usr/bin/env python3
"""Build data/weeks/week-2.json — the second in-season power snapshot.

Board: authored on the ~75% Week 1 prior / 25% Week 2 blend, plus structural
news (Jayden Daniels dislocated elbow — out weeks, back before December, so
ceiling holds; Caleb Williams hamstring week-to-week; Nabers shoulder scare
resolved). Ceiling ranks UNCHANGED from Week 1 — no December-relevant
roster-structure changes this week.
Rosters: transcribed from ESPN box scores (final, 2026-09-22); IR players
listed at the end of the bench. Records/PF cumulative from data/results/.
"""
import json, math, os

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
grades = {t["teamId"]: t["grade"] for t in json.load(open(f"{ROOT}/data/draft-grades.json"))["teams"]}
teams_meta = {t["teamId"]: t for t in json.load(open(f"{ROOT}/data/teams.json"))["teams"]}
editorial = json.load(open(f"{ROOT}/scripts/editorial-week-2.json"))
schedule = json.load(open(f"{ROOT}/data/schedule.json"))

PRE_RANK = {"bizzy": 1, "hnfnr-aint-busy": 2, "team-noor": 3, "bazan": 4,
            "team-mbk": 5, "i-eat-ass": 6, "chief-sheikh": 7,
            "mustafas-magnificent-team": 8, "rambam": 9, "gang-green": 10,
            "ivaafay": 11, "deddybaba": 12}

# rank, teamId, powerScore, tier, ceilingRank (ceilings unchanged from W1)
BOARD = [
    (1, "hnfnr-aint-busy", 86.8, "Favorite", 10),
    (2, "team-noor", 85.5, "Favorite", 3),
    (3, "bizzy", 83.4, "Favorite", 2),
    (4, "chief-sheikh", 81.0, "Contender", 8),
    (5, "team-mbk", 80.4, "Contender", 7),
    (6, "i-eat-ass", 78.0, "Contender", 6),
    (7, "bazan", 77.2, "Contender", 4),
    (8, "gang-green", 74.6, "Playoff-caliber", 5),
    (9, "mustafas-magnificent-team", 73.9, "Playoff-caliber", 9),
    (10, "deddybaba", 70.8, "Playoff-caliber", 12),
    (11, "rambam", 70.2, "Fringe contender", 1),
    (12, "ivaafay", 66.5, "Fragile", 11),
]

ARCHETYPE = {"team-noor": "The Complete Team", "bizzy": "The RB Machine", "team-mbk": "The Floor Monster",
             "bazan": "The Nuclear Core", "rambam": "The Venture Portfolio",
             "mustafas-magnificent-team": "The Deep Bench", "hnfnr-aint-busy": "The Stars Up Top",
             "i-eat-ass": "The Volatility Bet", "chief-sheikh": "The WR Superteam",
             "gang-green": "The Moonshot", "ivaafay": "The Bijan Build", "deddybaba": "The No-RB Experiment"}

MOVEMENT = {
  "hnfnr-aint-busy": [(1.4, "2-0 with the league scoring lead"), (0.9, "Schultz-Kincaid tight end platoon both hit"), (-0.7, "Reed and the kicker combined for 1.9")],
  "team-noor": [(2.0, "Week-high 133.88"), (0.6, "Purdy over Dart paid at 28.48"), (-1.1, "League-worst 243.68 points against")],
  "bizzy": [(-1.8, "Maye's interception spiral"), (-1.2, "93.62, a 40-point loss"), (-1.0, "Collins sidelined"), (0.4, "Henderson's 13.6 return")],
  "chief-sheikh": [(1.7, "2-0 at 10-1 all-play — no luck disclaimer this time"), (1.2, "St. Brown's 30.7"), (0.9, "Love-over-Herbert call paid"), (-0.2, "Chiefs D/ST gave 1.0")],
  "team-mbk": [(1.1, "Dak's 29.76 and the win"), (0.7, "9-2 all-play quality"), (-0.8, "Jacobs saga drags on"), (-0.4, "Montgomery's 3.4")],
  "i-eat-ass": [(-1.3, "86.86 at 1-10 all-play"), (-0.5, "Goedert hobbled to 0.9"), (0.9, "McCaffrey and Olave steady")],
  "bazan": [(-1.6, "Lamar at 14.8 and publicly shopped"), (-1.5, "24 points of defense left on the bench"), (-1.2, "Nabers scare on top of Brown's IR")],
  "gang-green": [(1.2, "First win, with Hubbard promoted in time"), (0.8, "Butker and Wilson delivered"), (-0.2, "Achane usage still light")],
  "mustafas-magnificent-team": [(0.6, "Mahomes' 28.98"), (-0.8, "Barkley's 2.5"), (-0.7, "Kelce's 20.6 benched, Moore's −0.1 started")],
  "deddybaba": [(2.6, "Allen's 40.82 — the season's best game, again"), (1.8, "First win, by 15.82"), (1.4, "Ferguson and Bateman signs of life")],
  "rambam": [(-2.4, "Daniels' dislocated elbow, out weeks"), (-1.6, "0-2 despite 6-5 all-play"), (0.6, "Lamb's 31.3")],
  "ivaafay": [(-1.4, "0-11 all-play week"), (-1.2, "Caleb Williams week-to-week"), (-0.8, "Bijan at 9.6"), (0.4, "Adams' 35.5 Monday night")],
}

STOCK = {
  "hnfnr-aint-busy": ("Dalton Schultz", "Jayden Reed"),
  "team-noor": ("Brock Purdy", "Jaxson Dart"),
  "bizzy": ("TreVeyon Henderson", "Drake Maye"),
  "chief-sheikh": ("Jordan Love", "Chiefs D/ST"),
  "team-mbk": ("Dak Prescott", "David Montgomery"),
  "i-eat-ass": ("Quinshon Judkins", "Dallas Goedert"),
  "bazan": ("Chase McLaughlin", "Lamar Jackson"),
  "gang-green": ("Chuba Hubbard", "De'Von Achane"),
  "mustafas-magnificent-team": ("Patrick Mahomes", "Saquon Barkley"),
  "deddybaba": ("Terrance Ferguson", "Puka Nacua"),
  "rambam": ("CeeDee Lamb", "Jayden Daniels"),
  "ivaafay": ("Davante Adams", "Caleb Williams"),
}

DEVELOPMENT = {
  "hnfnr-aint-busy": "2-0 with the scoring lead, and Bowers still hasn't played.",
  "team-noor": "Reversed the Dart call; Purdy's 28.48 delivered the week high.",
  "bizzy": "Maye and Loveland were offered to the group chat by 3:04 PM Sunday.",
  "chief-sheikh": "Benched Herbert for Love and won by 19.7 — 2-0 without the luck disclaimer.",
  "team-mbk": "Won with Stafford's 26.98 on the bench, then started selling him Tuesday.",
  "i-eat-ass": "86.86 one week after 132 — the first dud of the Ivan era.",
  "bazan": "Benched the Panthers defense that scored 24; started the Bucs at 4.",
  "gang-green": "Promoted Hubbard one week after his 22.2 sat — and won.",
  "mustafas-magnificent-team": "Benched Kelce's 20.6, started Moore's −0.1, lost by 19.72.",
  "deddybaba": "Allen followed 35.66 with 40.82 — the two best games of the season, same jersey.",
  "rambam": "Daniels dislocated his elbow Sunday; X-rays clean, timeline in weeks.",
  "ivaafay": "Adams hung 35.5 Monday night; the other eight starters combined for 48.32.",
}

S = ["QB", "RB", "RB", "WR", "WR", "TE", "FLEX", "D/ST", "K"]
def P(name, pos, nfl): return {"player": name, "position": pos, "nflTeam": nfl}
ROSTERS = {
 "rambam": {
   "starters": [P("Jayden Daniels","QB","WSH"),P("Chase Brown","RB","CIN"),P("Travis Etienne Jr.","RB","NO"),P("CeeDee Lamb","WR","DAL"),P("Emeka Egbuka","WR","TB"),P("Tyler Warren","TE","IND"),P("Matthew Golden","WR","GB"),P("49ers D/ST","D/ST","SF"),P("Tyler Bass","K","BUF")],
   "bench": [P("Rome Odunze","WR","CHI"),P("Jonathon Brooks","RB","CAR"),P("Xavier Worthy","WR","KC"),P("Kaelon Black","RB","SF"),P("Emmett Johnson","RB","KC"),P("Devin Singletary","RB","NYG"),P("Kalif Raymond","WR","CHI"),P("Tank Dell (IR)","WR","HOU")]},
 "mustafas-magnificent-team": {
   "starters": [P("Patrick Mahomes","QB","KC"),P("Omarion Hampton","RB","LAC"),P("Saquon Barkley","RB","PHI"),P("DeVonta Smith","WR","PHI"),P("DJ Moore","WR","BUF"),P("Isaiah Likely","TE","NYG"),P("Ladd McConkey","WR","LAC"),P("Ravens D/ST","D/ST","BAL"),P("Jason Myers","K","SEA")],
   "bench": [P("Marvin Harrison Jr.","WR","ARI"),P("Chris Godwin Jr.","WR","TB"),P("Justice Hill","RB","BAL"),P("Travis Kelce","TE","KC"),P("Kyler Murray","QB","MIN"),P("George Holani","RB","SEA"),P("Pat Bryant","WR","DEN"),P("Zach Charbonnet (IR)","RB","SEA")]},
 "bizzy": {
   "starters": [P("Drake Maye","QB","NE"),P("Jonathan Taylor","RB","IND"),P("Kenneth Walker III","RB","KC"),P("Carnell Tate","WR","TEN"),P("Deebo Samuel Sr.","WR","SF"),P("Colston Loveland","TE","CHI"),P("TreVeyon Henderson","RB","NE"),P("Packers D/ST","D/ST","GB"),P("Cam Little","K","JAX")],
   "bench": [P("Nico Collins","WR","HOU"),P("Rachaad White","RB","WSH"),P("Alec Pierce","WR","IND"),P("Rams D/ST","D/ST","LAR"),P("Hunter Henry","TE","NE"),P("Emari Demercado","RB","DAL"),P("Tyler Shough","QB","NO"),P("Jordyn Tyson (IR)","WR","NO")]},
 "deddybaba": {
   "starters": [P("Josh Allen","QB","BUF"),P("Bhayshul Tuten","RB","JAX"),P("Kenny Gainwell","RB","TB"),P("Rashee Rice","WR","KC"),P("Terry McLaurin","WR","WSH"),P("Tucker Kraft","TE","GB"),P("Terrance Ferguson","TE","LAR"),P("Broncos D/ST","D/ST","DEN"),P("Ka'imi Fairbairn","K","HOU")],
   "bench": [P("Puka Nacua","WR","LAR"),P("RJ Harvey","RB","DEN"),P("Josh Downs","WR","IND"),P("Tyjae Spears","RB","TEN"),P("Malik Willis","QB","MIA"),P("Demond Claiborne","RB","MIN"),P("Rashod Bateman","WR","BAL")]},
 "team-noor": {
   "starters": [P("Brock Purdy","QB","SF"),P("Breece Hall","RB","NYJ"),P("Kyren Williams","RB","LAR"),P("Ja'Marr Chase","WR","CIN"),P("Christian Watson","WR","GB"),P("Mark Andrews","TE","BAL"),P("Bucky Irving","RB","TB"),P("Patriots D/ST","D/ST","NE"),P("Tyler Loop","K","BAL")],
   "bench": [P("Jaylen Waddle","WR","DEN"),P("Aaron Jones Sr.","RB","MIN"),P("George Kittle","TE","SF"),P("J.K. Dobbins","RB","DEN"),P("Jakobi Meyers","WR","JAX"),P("Jaxson Dart","QB","NYG"),P("Demarcus Robinson","WR","SF")]},
 "hnfnr-aint-busy": {
   "starters": [P("Joe Burrow","QB","CIN"),P("Derrick Henry","RB","BAL"),P("Rhamondre Stevenson","RB","NE"),P("Jaxon Smith-Njigba","WR","SEA"),P("Jayden Reed","WR","GB"),P("Dalton Schultz","TE","HOU"),P("Tony Pollard","RB","TEN"),P("Eagles D/ST","D/ST","PHI"),P("Cameron Dicker","K","LAC")],
   "bench": [P("Brock Bowers","TE","LV"),P("Brian Thomas Jr.","WR","JAX"),P("Jacory Croskey-Merritt","RB","WSH"),P("Michael Wilson","WR","ARI"),P("Tyler Allgeier","RB","ARI"),P("Dalton Kincaid","TE","BUF"),P("Tyrone Tracy Jr.","RB","NYG"),P("Zay Flowers (IR)","WR","BAL")]},
 "bazan": {
   "starters": [P("Lamar Jackson","QB","BAL"),P("James Cook III","RB","BUF"),P("D'Andre Swift","RB","CHI"),P("Malik Nabers","WR","NYG"),P("Jalen Coker","WR","CAR"),P("Juwan Johnson","TE","NO"),P("Courtland Sutton","WR","DEN"),P("Buccaneers D/ST","D/ST","TB"),P("Chase McLaughlin","K","TB")],
   "bench": [P("Michael Pittman Jr.","WR","PIT"),P("Kyle Monangai","RB","CHI"),P("Bo Nix","QB","DEN"),P("Ray Davis","RB","BUF"),P("Antonio Williams","WR","WSH"),P("Panthers D/ST","D/ST","CAR"),P("Giants D/ST","D/ST","NYG"),P("A.J. Brown (IR)","WR","NE")]},
 "ivaafay": {
   "starters": [P("Caleb Williams","QB","CHI"),P("Bijan Robinson","RB","ATL"),P("Javonte Williams","RB","DAL"),P("George Pickens","WR","DAL"),P("Davante Adams","WR","LAR"),P("Kyle Pitts Sr.","TE","ATL"),P("Jadarian Price","RB","SEA"),P("Chargers D/ST","D/ST","LAC"),P("Jake Bates","K","DET")],
   "bench": [P("DK Metcalf","WR","PIT"),P("Jordan Addison","WR","MIN"),P("Alvin Kamara","RB","NO"),P("Khalil Shakir","WR","BUF"),P("Jalen Nailor","WR","LV"),P("Mike Gesicki","TE","CIN"),P("DeeJay Dallas","RB","MIN"),P("Jordan Mason (IR)","RB","MIN")]},
 "i-eat-ass": {
   "starters": [P("Jalen Hurts","QB","PHI"),P("Christian McCaffrey","RB","SF"),P("Jeremiyah Love","RB","ARI"),P("Chris Olave","WR","NO"),P("Jameson Williams","WR","DET"),P("Dallas Goedert","TE","PHI"),P("Quinshon Judkins","RB","CLE"),P("Steelers D/ST","D/ST","PIT"),P("Eddy Pineiro","K","SF")],
   "bench": [P("MarShawn Lloyd","RB","GB"),P("Quentin Johnston","WR","LAC"),P("Woody Marks","RB","HOU"),P("Romeo Doubs","WR","NE"),P("Makai Lemon","WR","PHI"),P("Devaughn Vele","WR","NO"),P("Cairo Santos","K","CHI")]},
 "team-mbk": {
   "starters": [P("Dak Prescott","QB","DAL"),P("Jahmyr Gibbs","RB","DET"),P("David Montgomery","RB","HOU"),P("Drake London","WR","ATL"),P("Tee Higgins","WR","CIN"),P("Sam LaPorta","TE","DET"),P("Mike Evans","WR","SF"),P("Seahawks D/ST","D/ST","SEA"),P("Harrison Mevis","K","LAR")],
   "bench": [P("Rico Dowdle","RB","PIT"),P("Wan'Dale Robinson","WR","TEN"),P("Brian Robinson Jr.","RB","ATL"),P("Matthew Stafford","QB","LAR"),P("Rashid Shaheed","WR","SEA"),P("Chris Brooks","RB","GB"),P("DeMario Douglas","WR","NE"),P("Josh Jacobs (IR)","RB","GB")]},
 "gang-green": {
   "starters": [P("Trevor Lawrence","QB","JAX"),P("De'Von Achane","RB","MIA"),P("Ashton Jeanty","RB","LV"),P("Garrett Wilson","WR","NYJ"),P("Tetairoa McMillan","WR","CAR"),P("Harold Fannin Jr.","TE","CLE"),P("Chuba Hubbard","RB","CAR"),P("Jets D/ST","D/ST","NYJ"),P("Harrison Butker","K","KC")],
   "bench": [P("Luther Burden III","WR","CHI"),P("Stefon Diggs","WR","WSH"),P("Mike Washington Jr.","RB","LV"),P("Keaton Mitchell","RB","LAC"),P("Adonai Mitchell","WR","NYJ"),P("Geno Smith","QB","NYJ"),P("Kenyon Sadiq","TE","NYJ"),P("De'Zhaun Stribling (IR)","WR","SF")]},
 "chief-sheikh": {
   "starters": [P("Jordan Love","QB","GB"),P("Cam Skattebo","RB","NYG"),P("Jaylen Warren","RB","PIT"),P("Amon-Ra St. Brown","WR","DET"),P("Justin Jefferson","WR","MIN"),P("Trey McBride","TE","ARI"),P("Parker Washington","WR","JAX"),P("Chiefs D/ST","D/ST","KC"),P("Brandon Aubrey","K","DAL")],
   "bench": [P("Justin Herbert","QB","LAC"),P("Blake Corum","RB","LAR"),P("Texans D/ST","D/ST","HOU"),P("Braelon Allen","RB","NYJ"),P("Tank Bigsby","RB","PHI"),P("Dontayvion Wicks","WR","PHI"),P("Caleb Douglas","WR","MIA")]},
}
for tid, r in ROSTERS.items():
    slots = [{"slot": s, **p} for s, p in zip(S, r["starters"])]
    ROSTERS[tid] = {"starters": slots, "bench": r["bench"]}

# cumulative records + PF from all results through week 2
rec = {t: {"wins": 0, "losses": 0} for t in PRE_RANK}
pf = {t: 0.0 for t in PRE_RANK}
for wk in (1, 2):
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

# next matchup from week 3 schedule
nxt = {}
for m in schedule["weeks"]["3"]:
    nxt[m["away"]] = f'at {teams_meta[m["home"]]["teamName"]}'
    nxt[m["home"]] = f'vs {teams_meta[m["away"]]["teamName"]}'

out = {"week": 2, "publishedAt": "2026-09-22", "deck": editorial["deck"], "teams": []}
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

json.dump(out, open(f"{ROOT}/data/weeks/week-2.json", "w"), indent=2)
print("odds sum:", round(sum(t["titleOdds"] for t in out["teams"]), 1))
print("playoff sum:", round(sum(t["playoffOdds"] for t in out["teams"]), 1))
for t in out["teams"]:
    mv = PRE_RANK[t["teamId"]] - t["powerRank"]
    delta_sum = round(sum(m["delta"] for m in t["movementReasons"]), 1)
    print(f'#{t["powerRank"]:>2} {t["teamId"]:<28} {"↑" + str(mv) if mv > 0 else "↓" + str(-mv) if mv < 0 else "—":>3}  {t["powerScore"]:>5}  {t["titleOdds"]:>4}%  {t["record"]["wins"]}-{t["record"]["losses"]}  PF {t["pointsFor"]:>6}  Δreasons {delta_sum}')

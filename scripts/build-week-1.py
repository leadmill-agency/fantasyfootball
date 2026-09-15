#!/usr/bin/env python3
"""Build data/weeks/week-1.json — the first in-season power snapshot.

Board: authored by the desk on the ~75% preseason prior / 25% Week 1 blend,
plus structural news (A.J. Brown IR ~6wk, Jacobs exempt indefinitely, Lloyd
inheriting the GB backfield). Approved by the commissioner 2026-09-15.
Rosters: transcribed from ESPN box scores (final, 2026-09-15); IR players
listed at the end of the bench. Records/PF from data/results/week-1.json.
Ceiling ranks: one structural change only — IEA 7->6, MBK 6->7.
"""
import json, math, os

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
grades = {t["teamId"]: t["grade"] for t in json.load(open(f"{ROOT}/data/draft-grades.json"))["teams"]}
teams_meta = {t["teamId"]: t for t in json.load(open(f"{ROOT}/data/teams.json"))["teams"]}
results = json.load(open(f"{ROOT}/data/results/week-1.json"))
editorial = json.load(open(f"{ROOT}/scripts/editorial-week-1.json"))
schedule = json.load(open(f"{ROOT}/data/schedule.json"))

PRE_RANK = {"team-noor": 1, "bizzy": 2, "team-mbk": 3, "bazan": 4, "rambam": 5,
            "mustafas-magnificent-team": 6, "hnfnr-aint-busy": 7, "i-eat-ass": 8,
            "chief-sheikh": 9, "gang-green": 10, "ivaafay": 11, "deddybaba": 12}

# rank, teamId, powerScore, tier, ceilingRank
BOARD = [
    (1, "bizzy", 87.0, "Favorite", 2),
    (2, "hnfnr-aint-busy", 85.2, "Favorite", 10),
    (3, "team-noor", 84.0, "Favorite", 3),
    (4, "bazan", 81.5, "Contender", 4),
    (5, "team-mbk", 79.8, "Contender", 7),
    (6, "i-eat-ass", 78.9, "Contender", 6),
    (7, "chief-sheikh", 77.4, "Contender", 8),
    (8, "mustafas-magnificent-team", 74.8, "Playoff-caliber", 9),
    (9, "rambam", 73.6, "Playoff-caliber", 1),
    (10, "gang-green", 72.8, "Playoff-caliber", 5),
    (11, "ivaafay", 69.5, "Fringe contender", 11),
    (12, "deddybaba", 65.0, "Fragile", 12),
]

ARCHETYPE = {"team-noor": "The Complete Team", "bizzy": "The RB Machine", "team-mbk": "The Floor Monster",
             "bazan": "The Nuclear Core", "rambam": "The Venture Portfolio",
             "mustafas-magnificent-team": "The Deep Bench", "hnfnr-aint-busy": "The Stars Up Top",
             "i-eat-ass": "The Volatility Bet", "chief-sheikh": "The WR Superteam",
             "gang-green": "The Moonshot", "ivaafay": "The Bijan Build", "deddybaba": "The No-RB Experiment"}

MOVEMENT = {
  "bizzy": [(1.8, "Walker and Taylor validate the backfield thesis"), (-1.2, "TreVeyon Henderson injured"), (-0.8, "Loveland zero / thin WR output")],
  "hnfnr-aint-busy": [(4.0, "League-high 150.06"), (2.4, "Henry's role and production"), (1.5, "Bowers returning within weeks"), (-0.6, "Flowers hamstring")],
  "team-noor": [(-3.4, "Median score against an elite field"), (-2.0, "Chase and Waddle silent"), (0.8, "Dart emergence at QB")],
  "bazan": [(2.6, "Second-best score of the week"), (1.6, "Coker's role is real"), (-2.8, "A.J. Brown to IR, out ~6 weeks")],
  "team-mbk": [(-3.5, "Jacobs' exempt-list absence now priced in"), (-2.0, "Loss at 5-6 all-play"), (-1.2, "London's QB environment")],
  "i-eat-ass": [(1.7, "132-point opener"), (1.4, "Lloyd inherits the Green Bay job"), (-0.6, "Lloyd/Brooks committee split")],
  "chief-sheikh": [(2.5, "WR core consistency"), (0.9, "Parker Washington flex emergence"), (-1.1, "K + D/ST combined for -2.0")],
  "mustafas-magnificent-team": [(1.0, "1-0 result"), (-2.2, "3-8 all-play, league-high luck"), (-2.6, "McConkey, Kyler, Charbonnet injuries")],
  "rambam": [(-3.6, "Second-worst score of the week"), (-2.6, "Receiver portfolio combined for 23.8"), (0.4, "Golden's role signal")],
  "gang-green": [(2.2, "7-4 all-play quality"), (1.4, "Jeanty and Lawrence validated"), (-2.6, "Achane usage concern")],
  "ivaafay": [(1.6, "Caleb Williams led all NFL QBs"), (-1.5, "Pitts and D/ST zeros"), (-0.8, "Starting lineup underperformance")],
  "deddybaba": [(1.5, "Allen's historic opener"), (-1.8, "0-11 all-play"), (-1.2, "RB room performed as constructed")],
}

STOCK = {
  "bizzy": ("Kenneth Walker III", "Colston Loveland"),
  "hnfnr-aint-busy": ("Derrick Henry", "Zay Flowers"),
  "team-noor": ("Jaxson Dart", "Ja'Marr Chase"),
  "bazan": ("Jalen Coker", "A.J. Brown"),
  "team-mbk": ("David Montgomery", "Drake London"),
  "i-eat-ass": ("Devaughn Vele", "Jameson Williams"),
  "chief-sheikh": ("Parker Washington", "Texans D/ST"),
  "mustafas-magnificent-team": ("Isaiah Likely", "Ladd McConkey"),
  "rambam": ("Matthew Golden", "Rome Odunze"),
  "gang-green": ("Ashton Jeanty", "De'Von Achane"),
  "ivaafay": ("Caleb Williams", "Kyle Pitts Sr."),
  "deddybaba": ("Josh Allen", "Terry McLaurin"),
}

DEVELOPMENT = {
  "bizzy": "Kenneth Walker's 32.6 on Monday night flipped the week's only comeback.",
  "hnfnr-aint-busy": "150.06 without Brock Bowers, who returns within weeks.",
  "team-noor": "Dart over Purdy worked; the schedule didn't.",
  "bazan": "A.J. Brown to IR — out until roughly Week 6.",
  "team-mbk": "Jacobs to IR as the exempt list drags on.",
  "i-eat-ass": "Lloyd led the Green Bay backfield; Kaleb Johnson played zero snaps.",
  "chief-sheikh": "Won by 9.5 with -2.0 combined from the kicker and defense.",
  "mustafas-magnificent-team": "Won at 3-8 all-play, then lost McConkey and Kyler to injuries.",
  "rambam": "The young-receiver portfolio combined for 23.8.",
  "gang-green": "Beat 7 of 11 teams and lost anyway.",
  "ivaafay": "Caleb Williams led every quarterback in football.",
  "deddybaba": "0-11 all-play despite the week's best QB game.",
}

S = ["QB", "RB", "RB", "WR", "WR", "TE", "FLEX", "D/ST", "K"]
def P(name, pos, nfl): return {"player": name, "position": pos, "nflTeam": nfl}
ROSTERS = {
 "rambam": {
   "starters": [P("Jayden Daniels","QB","WSH"),P("Chase Brown","RB","CIN"),P("Travis Etienne Jr.","RB","NO"),P("CeeDee Lamb","WR","DAL"),P("Emeka Egbuka","WR","TB"),P("Tyler Warren","TE","IND"),P("Rome Odunze","WR","CHI"),P("Lions D/ST","D/ST","DET"),P("Cameron Dicker","K","LAC")],
   "bench": [P("Jonathon Brooks","RB","CAR"),P("Matthew Golden","WR","GB"),P("Xavier Worthy","WR","KC"),P("KC Concepcion","WR","CLE"),P("Kaelon Black","RB","SF"),P("Emmett Johnson","RB","KC"),P("Kayshon Boutte","WR","HOU"),P("Tank Dell (IR)","WR","HOU")]},
 "mustafas-magnificent-team": {
   "starters": [P("Patrick Mahomes","QB","KC"),P("Omarion Hampton","RB","LAC"),P("Saquon Barkley","RB","PHI"),P("DeVonta Smith","WR","PHI"),P("Ladd McConkey","WR","LAC"),P("Isaiah Likely","TE","NYG"),P("Chris Godwin Jr.","WR","TB"),P("Ravens D/ST","D/ST","BAL"),P("Jason Myers","K","SEA")],
   "bench": [P("DJ Moore","WR","BUF"),P("Marvin Harrison Jr.","WR","ARI"),P("Justice Hill","RB","BAL"),P("Najee Harris","RB","NYG"),P("Travis Kelce","TE","KC"),P("Kyler Murray","QB","MIN"),P("George Holani","RB","SEA"),P("Zach Charbonnet (IR)","RB","SEA")]},
 "bizzy": {
   "starters": [P("Drake Maye","QB","NE"),P("Jonathan Taylor","RB","IND"),P("Kenneth Walker III","RB","KC"),P("Nico Collins","WR","HOU"),P("Carnell Tate","WR","TEN"),P("Colston Loveland","TE","CHI"),P("Alec Pierce","WR","IND"),P("Rams D/ST","D/ST","LAR"),P("Cam Little","K","JAX")],
   "bench": [P("TreVeyon Henderson","RB","NE"),P("Rachaad White","RB","WSH"),P("Deebo Samuel Sr.","WR","SF"),P("Keenan Allen","WR","IND"),P("Hunter Henry","TE","NE"),P("Baker Mayfield","QB","TB"),P("Emari Demercado","RB","DAL"),P("Jordyn Tyson (IR)","WR","NO")]},
 "deddybaba": {
   "starters": [P("Josh Allen","QB","BUF"),P("Bhayshul Tuten","RB","JAX"),P("Kenny Gainwell","RB","TB"),P("Puka Nacua","WR","LAR"),P("Terry McLaurin","WR","WSH"),P("Tucker Kraft","TE","GB"),P("Rashee Rice","WR","KC"),P("Broncos D/ST","D/ST","DEN"),P("Ka'imi Fairbairn","K","HOU")],
   "bench": [P("RJ Harvey","RB","DEN"),P("Josh Downs","WR","IND"),P("Tyjae Spears","RB","TEN"),P("Terrance Ferguson","TE","LAR"),P("Kimani Vidal","RB","LAC"),P("Kaleb Johnson","RB","GB"),P("Malik Willis","QB","MIA")]},
 "team-noor": {
   "starters": [P("Jaxson Dart","QB","NYG"),P("Breece Hall","RB","NYJ"),P("Kyren Williams","RB","LAR"),P("Ja'Marr Chase","WR","CIN"),P("Jaylen Waddle","WR","DEN"),P("Mark Andrews","TE","BAL"),P("Bucky Irving","RB","TB"),P("Patriots D/ST","D/ST","NE"),P("Tyler Loop","K","BAL")],
   "bench": [P("Christian Watson","WR","GB"),P("Aaron Jones Sr.","RB","MIN"),P("George Kittle","TE","SF"),P("J.K. Dobbins","RB","DEN"),P("Brock Purdy","QB","SF"),P("Jakobi Meyers","WR","JAX"),P("Jalen McMillan","WR","TB")]},
 "hnfnr-aint-busy": {
   "starters": [P("Joe Burrow","QB","CIN"),P("Derrick Henry","RB","BAL"),P("Rhamondre Stevenson","RB","NE"),P("Jaxon Smith-Njigba","WR","SEA"),P("Zay Flowers","WR","BAL"),P("Dalton Kincaid","TE","BUF"),P("Tony Pollard","RB","TEN"),P("Eagles D/ST","D/ST","PHI"),P("Evan McPherson","K","CIN")],
   "bench": [P("Brock Bowers","TE","LV"),P("Brian Thomas Jr.","WR","JAX"),P("Jacory Croskey-Merritt","RB","WSH"),P("Michael Wilson","WR","ARI"),P("Tyler Allgeier","RB","ARI"),P("Jayden Reed","WR","GB"),P("Tyrone Tracy Jr.","RB","NYG")]},
 "bazan": {
   "starters": [P("Lamar Jackson","QB","BAL"),P("James Cook III","RB","BUF"),P("D'Andre Swift","RB","CHI"),P("A.J. Brown","WR","NE"),P("Jalen Coker","WR","CAR"),P("Juwan Johnson","TE","NO"),P("Courtland Sutton","WR","DEN"),P("Jaguars D/ST","D/ST","JAX"),P("Spencer Shrader","K","IND")],
   "bench": [P("Malik Nabers","WR","NYG"),P("Michael Pittman Jr.","WR","PIT"),P("Kyle Monangai","RB","CHI"),P("Bo Nix","QB","DEN"),P("Chris Rodriguez Jr.","RB","JAX"),P("Ray Davis","RB","BUF"),P("Michael Mayer","TE","LV")]},
 "ivaafay": {
   "starters": [P("Caleb Williams","QB","CHI"),P("Bijan Robinson","RB","ATL"),P("Javonte Williams","RB","DAL"),P("George Pickens","WR","DAL"),P("Davante Adams","WR","LAR"),P("Kyle Pitts Sr.","TE","ATL"),P("Jadarian Price","RB","SEA"),P("Chargers D/ST","D/ST","LAC"),P("Jake Bates","K","DET")],
   "bench": [P("DK Metcalf","WR","PIT"),P("Jordan Mason","RB","MIN"),P("Jordan Addison","WR","MIN"),P("Alvin Kamara","RB","NO"),P("Khalil Shakir","WR","BUF"),P("Dylan Sampson","RB","CLE"),P("Jalen Nailor","WR","LV")]},
 "i-eat-ass": {
   "starters": [P("Jalen Hurts","QB","PHI"),P("Christian McCaffrey","RB","SF"),P("Jeremiyah Love","RB","ARI"),P("Chris Olave","WR","NO"),P("Jameson Williams","WR","DET"),P("Dallas Goedert","TE","PHI"),P("MarShawn Lloyd","RB","GB"),P("Steelers D/ST","D/ST","PIT"),P("Eddy Pineiro","K","SF")],
   "bench": [P("Quinshon Judkins","RB","CLE"),P("Quentin Johnston","WR","LAC"),P("Woody Marks","RB","HOU"),P("Romeo Doubs","WR","NE"),P("Makai Lemon","WR","PHI"),P("Jerry Jeudy","WR","CLE"),P("Devaughn Vele","WR","NO")]},
 "team-mbk": {
   "starters": [P("Dak Prescott","QB","DAL"),P("Jahmyr Gibbs","RB","DET"),P("David Montgomery","RB","HOU"),P("Drake London","WR","ATL"),P("Tee Higgins","WR","CIN"),P("Sam LaPorta","TE","DET"),P("Rico Dowdle","RB","PIT"),P("Seahawks D/ST","D/ST","SEA"),P("Harrison Mevis","K","LAR")],
   "bench": [P("Mike Evans","WR","SF"),P("Wan'Dale Robinson","WR","TEN"),P("Jake Ferguson","TE","DAL"),P("Brian Robinson Jr.","RB","ATL"),P("Matthew Stafford","QB","LAR"),P("Rashid Shaheed","WR","SEA"),P("Sean Tucker","RB","TB"),P("Josh Jacobs (IR)","RB","GB")]},
 "gang-green": {
   "starters": [P("Trevor Lawrence","QB","JAX"),P("De'Von Achane","RB","MIA"),P("Ashton Jeanty","RB","LV"),P("Garrett Wilson","WR","NYJ"),P("Tetairoa McMillan","WR","CAR"),P("Harold Fannin Jr.","TE","CLE"),P("Luther Burden III","WR","CHI"),P("Jets D/ST","D/ST","NYJ"),P("Harrison Butker","K","KC")],
   "bench": [P("Chuba Hubbard","RB","CAR"),P("Stefon Diggs","WR","WSH"),P("Mike Washington Jr.","RB","LV"),P("De'Zhaun Stribling","WR","SF"),P("Keaton Mitchell","RB","LAC"),P("Adonai Mitchell","WR","NYJ"),P("Geno Smith","QB","NYJ")]},
 "chief-sheikh": {
   "starters": [P("Justin Herbert","QB","LAC"),P("Cam Skattebo","RB","NYG"),P("Jaylen Warren","RB","PIT"),P("Amon-Ra St. Brown","WR","DET"),P("Justin Jefferson","WR","MIN"),P("Trey McBride","TE","ARI"),P("Parker Washington","WR","JAX"),P("Texans D/ST","D/ST","HOU"),P("Brandon Aubrey","K","DAL")],
   "bench": [P("Blake Corum","RB","LAR"),P("Braelon Allen","RB","NYJ"),P("Tank Bigsby","RB","PHI"),P("Dontayvion Wicks","WR","PHI"),P("Tre Tucker","WR","LV"),P("Jacob Saylors","RB","DET"),P("Malachi Fields","WR","NYG")]},
}
for tid, r in ROSTERS.items():
    slots = [{"slot": s, **p} for s, p in zip(S, r["starters"])]
    ROSTERS[tid] = {"starters": slots, "bench": r["bench"]}

# records + PF from results
rec, pf = {}, {}
for m in results["matchups"]:
    hw = m["homeScore"] > m["awayScore"]
    rec[m["homeTeamId"]] = {"wins": 1 if hw else 0, "losses": 0 if hw else 1}
    rec[m["awayTeamId"]] = {"wins": 0 if hw else 1, "losses": 1 if hw else 0}
    pf[m["homeTeamId"]] = m["homeScore"]
    pf[m["awayTeamId"]] = m["awayScore"]

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

# next matchup from week 2 schedule
nxt = {}
for m in schedule["weeks"]["2"]:
    nxt[m["away"]] = f'at {teams_meta[m["home"]]["teamName"]}'
    nxt[m["home"]] = f'vs {teams_meta[m["away"]]["teamName"]}'

out = {"week": 1, "publishedAt": "2026-09-15", "deck": editorial["deck"], "teams": []}
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

json.dump(out, open(f"{ROOT}/data/weeks/week-1.json", "w"), indent=2)
print("odds sum:", round(sum(t["titleOdds"] for t in out["teams"]), 1))
for t in out["teams"]:
    mv = PRE_RANK[t["teamId"]] - t["powerRank"]
    print(f'#{t["powerRank"]:>2} {t["teamId"]:<28} {"↑" + str(mv) if mv > 0 else "↓" + str(-mv) if mv < 0 else "—":>3}  {t["powerScore"]:>5}  {t["titleOdds"]:>4}%  {t["record"]["wins"]}-{t["record"]["losses"]}  PF {t["pointsFor"]}')

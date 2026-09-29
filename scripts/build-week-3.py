#!/usr/bin/env python3
"""Build data/weeks/week-3.json — the third in-season power snapshot.

Board: the first built on the Week 3+ method Rameel set on 2026-09-29 —
about 70% season results (record, all-play, points for) and 30% structure
(roster going forward after trades/injuries, schedule). Blend inputs are in
the SEASON-LOG; power scores keep the blend's order on the familiar 65-88 scale.
Ceiling ranks now also move on waiver pickups and player performance (not only
structural news). Rosters: transcribed from ESPN box scores (final,
2026-09-29) — Week 3 lineups as played, i.e. BEFORE the RamBam-Bizzy trade
(Lamb/Chase Brown/Emmett Johnson for Taylor/Henderson/Emanuel Wilson), which
was still pending its veto window. IR players are listed at the end of the bench.
"""
import json, math, os

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
grades = {t["teamId"]: t["grade"] for t in json.load(open(f"{ROOT}/data/draft-grades.json"))["teams"]}
teams_meta = {t["teamId"]: t for t in json.load(open(f"{ROOT}/data/teams.json"))["teams"]}
editorial = json.load(open(f"{ROOT}/scripts/editorial-week-3.json"))
schedule = json.load(open(f"{ROOT}/data/schedule.json"))

PRE_RANK = {"hnfnr-aint-busy": 1, "team-noor": 2, "bizzy": 3, "chief-sheikh": 4,
            "team-mbk": 5, "i-eat-ass": 6, "bazan": 7, "gang-green": 8,
            "mustafas-magnificent-team": 9, "deddybaba": 10, "rambam": 11, "ivaafay": 12}

# rank, teamId, powerScore, tier, ceilingRank
BOARD = [
    (1, "hnfnr-aint-busy", 88.4, "Favorite", 2),
    (2, "team-noor", 86.8, "Favorite", 1),
    (3, "team-mbk", 83.6, "Contender", 3),
    (4, "chief-sheikh", 80.6, "Contender", 6),
    (5, "bazan", 78.8, "Contender", 7),
    (6, "gang-green", 74.4, "Playoff-caliber", 10),
    (7, "i-eat-ass", 73.8, "Playoff-caliber", 8),
    (8, "ivaafay", 72.0, "Playoff-caliber", 9),
    (9, "bizzy", 71.6, "Playoff-caliber", 5),
    (10, "mustafas-magnificent-team", 70.4, "Fringe contender", 11),
    (11, "rambam", 67.6, "Fringe contender", 4),
    (12, "deddybaba", 67.0, "Fragile", 12),
]

ARCHETYPE = {"team-noor": "The Complete Team", "bizzy": "The RB Machine", "team-mbk": "The Floor Monster",
             "bazan": "The Nuclear Core", "rambam": "The Venture Portfolio",
             "mustafas-magnificent-team": "The Deep Bench", "hnfnr-aint-busy": "The Stars Up Top",
             "i-eat-ass": "The Volatility Bet", "chief-sheikh": "The WR Superteam",
             "gang-green": "The Moonshot", "ivaafay": "The Bijan Build", "deddybaba": "The No-RB Experiment"}

MOVEMENT = {
  "hnfnr-aint-busy": [(1.2, "3-0 and 27-6 all-play, best in the league"), (0.8, "Bowers healthy — 22.6 from the bench"), (-0.4, "Eagles D/ST at −1.0; 56.5 points benched")],
  "team-noor": [(1.4, "Back-to-back week highs, 138.48"), (0.7, "Purdy's four TDs, Kittle promoted"), (-0.8, "Breece Hall week-to-week")],
  "team-mbk": [(1.8, "136.34 at 10-1 all-play"), (1.4, "Gibbs' 37.9"), (0.6, "Results now weigh 70% of the board"), (-0.6, "Stafford benched again; Jacobs still no timeline")],
  "chief-sheikh": [(0.8, "25-8 all-play, second-best in the league"), (-0.7, "Jefferson's ankle — out until about Week 8"), (-0.5, "Benched Darnold's 27.66 for Love")],
  "bazan": [(1.2, "Win at 6-5 all-play"), (0.9, "Lamar's 20.44 answered the trade talk"), (-0.5, "Coker and Adonai Mitchell hurt")],
  "gang-green": [(1.0, "2-1 under the new results weighting"), (-0.8, "Won at 2-9 all-play"), (-0.4, "Achane out for the season")],
  "i-eat-ass": [(-2.0, "1-2 and 14-19 all-play"), (-1.4, "Results now weigh 70% of the board"), (-0.8, "Goedert out; Lloyd's role shrinking")],
  "ivaafay": [(2.6, "First win, 9-2 all-play"), (2.0, "Bijan's 34.3"), (1.8, "Penix and Watson cover the QB spot"), (-0.9, "Caleb out three to four weeks")],
  "bizzy": [(-6.4, "Results now weigh 70%: 11-22 all-play, 288.94 PF"), (-3.6, "84.70 at 1-10 all-play"), (-2.4, "Traded Jonathan Taylor to the commissioner"), (0.6, "Lamb and Chase Brown arrive")],
  "mustafas-magnificent-team": [(-1.4, "Loss at 5-6 all-play"), (-1.3, "Results now weigh 70%: 11-22 all-play"), (-0.8, "Barkley and Hampton slumping")],
  "rambam": [(-2.8, "0-3, the league's only winless team"), (-1.4, "Etienne's hamstring, out extended"), (1.6, "Taylor and Henderson arrive in the trade")],
  "deddybaba": [(-2.2, "0-11 all-play week, 7-26 on the season"), (-1.2, "McLaurin's 16.7 left on the bench"), (-0.4, "Allen's knee bruise")],
}

STOCK = {
  "hnfnr-aint-busy": ("Brock Bowers", "Eagles D/ST"),
  "team-noor": ("Brock Purdy", "Breece Hall"),
  "team-mbk": ("Jahmyr Gibbs", "Sam LaPorta"),
  "chief-sheikh": ("Sam Darnold", "Justin Jefferson"),
  "bazan": ("Lamar Jackson", "Jalen Coker"),
  "gang-green": ("Kenyon Sadiq", "De'Von Achane"),
  "i-eat-ass": ("Jeremiyah Love", "MarShawn Lloyd"),
  "ivaafay": ("Bijan Robinson", "Caleb Williams"),
  "bizzy": ("Tyler Shough", "Drake Maye"),
  "mustafas-magnificent-team": ("Vikings D/ST", "Omarion Hampton"),
  "rambam": ("Kalif Raymond", "Travis Etienne Jr."),
  "deddybaba": ("Terry McLaurin", "Rashod Bateman"),
}

DEVELOPMENT = {
  "hnfnr-aint-busy": "3-0 with Bowers' 22.6 and Wilson's 20.4 on the bench.",
  "team-noor": "The weekly high again — $200 cashed, still $167 down on the buy-in.",
  "team-mbk": "Gibbs scored three TDs; MBK missed the hundo by 2.14.",
  "chief-sheikh": "Jefferson's ankle injury projects to a Week 8 return.",
  "bazan": "Traded Bryce Young for Adonai Mitchell, who was ruled out right away.",
  "gang-green": "Achane tore his ACL in the first quarter; dropped Tuesday.",
  "i-eat-ass": "Lost 96.22 to 138.48; Lloyd got four carries.",
  "ivaafay": "First win behind Bijan's 194 rushing yards.",
  "bizzy": "Traded Jonathan Taylor to RamBam for CeeDee Lamb and Chase Brown.",
  "mustafas-magnificent-team": "Dropped Coleman, Gadsden and Dell in the same minute Tuesday.",
  "rambam": "0-3, then traded for Taylor — the veto rule held.",
  "deddybaba": "Lost by 4.08 with McLaurin's 16.7 on the bench.",
}

S = ["QB", "RB", "RB", "WR", "WR", "TE", "FLEX", "D/ST", "K"]
def P(name, pos, nfl): return {"player": name, "position": pos, "nflTeam": nfl}
ROSTERS = {
 "rambam": {
   "starters": [P("C.J. Stroud","QB","HOU"),P("Chase Brown","RB","CIN"),P("Travis Etienne Jr.","RB","NO"),P("CeeDee Lamb","WR","DAL"),P("Emeka Egbuka","WR","TB"),P("Tyler Warren","TE","IND"),P("Matthew Golden","WR","GB"),P("Chiefs D/ST","D/ST","KC"),P("Tyler Bass","K","BUF")],
   "bench": [P("Rome Odunze","WR","CHI"),P("Jayden Daniels","QB","WSH"),P("Xavier Worthy","WR","KC"),P("Kaelon Black","RB","SF"),P("Emmett Johnson","RB","KC"),P("Kalif Raymond","WR","CHI"),P("Chris Rodriguez Jr.","RB","JAX"),P("Jonathon Brooks (IR)","RB","CAR")]},
 "hnfnr-aint-busy": {
   "starters": [P("Joe Burrow","QB","CIN"),P("Derrick Henry","RB","BAL"),P("Rhamondre Stevenson","RB","NE"),P("Jaxon Smith-Njigba","WR","SEA"),P("Denzel Boston","WR","CLE"),P("Dalton Kincaid","TE","BUF"),P("Tony Pollard","RB","TEN"),P("Eagles D/ST","D/ST","PHI"),P("Cameron Dicker","K","LAC")],
   "bench": [P("Brock Bowers","TE","LV"),P("Brian Thomas Jr.","WR","JAX"),P("Jacory Croskey-Merritt","RB","WSH"),P("Michael Wilson","WR","ARI"),P("Tyler Allgeier","RB","ARI"),P("Jayden Reed","WR","GB"),P("Dalton Schultz","TE","HOU"),P("Zay Flowers (IR)","WR","BAL")]},
 "bizzy": {
   "starters": [P("Tyler Shough","QB","NO"),P("Jonathan Taylor","RB","IND"),P("Kenneth Walker III","RB","KC"),P("Deebo Samuel Sr.","WR","SF"),P("Malik Washington","WR","MIA"),P("Hunter Henry","TE","NE"),P("TreVeyon Henderson","RB","NE"),P("49ers D/ST","D/ST","SF"),P("Cam Little","K","JAX")],
   "bench": [P("Nico Collins","WR","HOU"),P("Colston Loveland","TE","CHI"),P("Drake Maye","QB","NE"),P("Rachaad White","RB","WSH"),P("Emanuel Wilson","RB","SEA"),P("Rams D/ST","D/ST","LAR"),P("Ravens D/ST","D/ST","BAL"),P("Alec Pierce (IR)","WR","IND")]},
 "bazan": {
   "starters": [P("Lamar Jackson","QB","BAL"),P("James Cook III","RB","BUF"),P("D'Andre Swift","RB","CHI"),P("Malik Nabers","WR","NYG"),P("Jalen Coker","WR","CAR"),P("Juwan Johnson","TE","NO"),P("Courtland Sutton","WR","DEN"),P("Panthers D/ST","D/ST","CAR"),P("Chase McLaughlin","K","TB")],
   "bench": [P("Michael Pittman Jr.","WR","PIT"),P("Kyle Monangai","RB","CHI"),P("Bo Nix","QB","DEN"),P("Ray Davis","RB","BUF"),P("Ted Hurst III","WR","TB"),P("Adonai Mitchell","WR","NYJ"),P("Cardinals D/ST","D/ST","ARI"),P("A.J. Brown (IR)","WR","NE")]},
 "i-eat-ass": {
   "starters": [P("Jalen Hurts","QB","PHI"),P("Christian McCaffrey","RB","SF"),P("Jeremiyah Love","RB","ARI"),P("Chris Olave","WR","NO"),P("Romeo Doubs","WR","NE"),P("T.J. Hockenson","TE","MIN"),P("Quinshon Judkins","RB","CLE"),P("Steelers D/ST","D/ST","PIT"),P("Eddy Pineiro","K","SF")],
   "bench": [P("Jameson Williams","WR","DET"),P("MarShawn Lloyd","RB","GB"),P("Dallas Goedert","TE","PHI"),P("Quentin Johnston","WR","LAC"),P("Woody Marks","RB","HOU"),P("Devaughn Vele","WR","NO"),P("Carnell Tate","WR","TEN")]},
 "team-noor": {
   "starters": [P("Brock Purdy","QB","SF"),P("Breece Hall","RB","NYJ"),P("Kyren Williams","RB","LAR"),P("Ja'Marr Chase","WR","CIN"),P("Christian Watson","WR","GB"),P("George Kittle","TE","SF"),P("Bucky Irving","RB","TB"),P("Patriots D/ST","D/ST","NE"),P("Tyler Loop","K","BAL")],
   "bench": [P("Jaylen Waddle","WR","DEN"),P("Aaron Jones Sr.","RB","MIN"),P("J.K. Dobbins","RB","DEN"),P("Mark Andrews","TE","BAL"),P("Jared Goff","QB","DET"),P("Tre Tucker","WR","LV"),P("Raiders D/ST","D/ST","LV"),P("Demarcus Robinson (IR)","WR","SF")]},
 "gang-green": {
   "starters": [P("Bryce Young","QB","CAR"),P("De'Von Achane","RB","MIA"),P("Ashton Jeanty","RB","LV"),P("Garrett Wilson","WR","NYJ"),P("Tetairoa McMillan","WR","CAR"),P("Kenyon Sadiq","TE","NYJ"),P("Chuba Hubbard","RB","CAR"),P("Bengals D/ST","D/ST","CIN"),P("Harrison Butker","K","KC")],
   "bench": [P("Luther Burden III","WR","CHI"),P("Harold Fannin Jr.","TE","CLE"),P("Stefon Diggs","WR","WSH"),P("Mike Washington Jr.","RB","LV"),P("Keaton Mitchell","RB","LAC"),P("Trevor Lawrence","QB","JAX"),P("Jets D/ST","D/ST","NYJ"),P("Jordyn Tyson (IR)","WR","NO")]},
 "deddybaba": {
   "starters": [P("Josh Allen","QB","BUF"),P("Bhayshul Tuten","RB","JAX"),P("RJ Harvey","RB","DEN"),P("Rashee Rice","WR","KC"),P("Josh Downs","WR","IND"),P("Tucker Kraft","TE","GB"),P("Rashod Bateman","WR","BAL"),P("Lions D/ST","D/ST","DET"),P("Ka'imi Fairbairn","K","HOU")],
   "bench": [P("Puka Nacua","WR","LAR"),P("Terry McLaurin","WR","WSH"),P("Kenny Gainwell","RB","TB"),P("Tyjae Spears","RB","TEN"),P("Terrance Ferguson","TE","LAR"),P("Demond Claiborne","RB","MIN"),P("Broncos D/ST","D/ST","DEN")]},
 "mustafas-magnificent-team": {
   "starters": [P("Patrick Mahomes","QB","KC"),P("Omarion Hampton","RB","LAC"),P("Saquon Barkley","RB","PHI"),P("DeVonta Smith","WR","PHI"),P("Ladd McConkey","WR","LAC"),P("Travis Kelce","TE","KC"),P("DJ Moore","WR","BUF"),P("Vikings D/ST","D/ST","MIN"),P("Jason Myers","K","SEA")],
   "bench": [P("Marvin Harrison Jr.","WR","ARI"),P("Isaiah Likely","TE","NYG"),P("Chris Godwin Jr.","WR","TB"),P("Kyler Murray","QB","MIN"),P("Oronde Gadsden","TE","LAC"),P("Jonah Coleman (IR)","RB","DEN"),P("Tank Dell (IR)","WR","HOU"),P("Zach Charbonnet (IR)","RB","SEA")]},
 "ivaafay": {
   "starters": [P("Michael Penix Jr.","QB","ATL"),P("Bijan Robinson","RB","ATL"),P("Javonte Williams","RB","DAL"),P("George Pickens","WR","DAL"),P("Davante Adams","WR","LAR"),P("Kyle Pitts Sr.","TE","ATL"),P("Jadarian Price","RB","SEA"),P("Buccaneers D/ST","D/ST","TB"),P("Jake Bates","K","DET")],
   "bench": [P("DK Metcalf","WR","PIT"),P("Caleb Williams","QB","CHI"),P("Jordan Addison","WR","MIN"),P("Alvin Kamara","RB","NO"),P("Khalil Shakir","WR","BUF"),P("Darren Waller","TE","CAR"),P("Deshaun Watson","QB","CLE"),P("Jordan Mason (IR)","RB","MIN")]},
 "team-mbk": {
   "starters": [P("Dak Prescott","QB","DAL"),P("Jahmyr Gibbs","RB","DET"),P("David Montgomery","RB","HOU"),P("Drake London","WR","ATL"),P("Tee Higgins","WR","CIN"),P("Sam LaPorta","TE","DET"),P("Mike Evans","WR","SF"),P("Seahawks D/ST","D/ST","SEA"),P("Evan McPherson","K","CIN")],
   "bench": [P("Rico Dowdle","RB","PIT"),P("Wan'Dale Robinson","WR","TEN"),P("Brian Robinson Jr.","RB","ATL"),P("Matthew Stafford","QB","LAR"),P("Rashid Shaheed","WR","SEA"),P("Chris Brooks","RB","GB"),P("KC Concepcion","WR","CLE"),P("Josh Jacobs (IR)","RB","GB")]},
 "chief-sheikh": {
   "starters": [P("Jordan Love","QB","GB"),P("Cam Skattebo","RB","NYG"),P("Jaylen Warren","RB","PIT"),P("Amon-Ra St. Brown","WR","DET"),P("Justin Jefferson","WR","MIN"),P("Trey McBride","TE","ARI"),P("Parker Washington","WR","JAX"),P("Texans D/ST","D/ST","HOU"),P("Brandon Aubrey","K","DAL")],
   "bench": [P("Blake Corum","RB","LAR"),P("Braelon Allen","RB","NYJ"),P("Tank Bigsby","RB","PHI"),P("Dontayvion Wicks","WR","PHI"),P("Jake Ferguson","TE","DAL"),P("Kaleb Johnson","RB","GB"),P("Sam Darnold","QB","SEA")]},
}
for tid, r in ROSTERS.items():
    slots = [{"slot": s, **p} for s, p in zip(S, r["starters"])]
    ROSTERS[tid] = {"starters": slots, "bench": r["bench"]}

# cumulative records + PF from all results through week 3
rec = {t: {"wins": 0, "losses": 0} for t in PRE_RANK}
pf = {t: 0.0 for t in PRE_RANK}
for wk in (1, 2, 3):
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

# next matchup from week 4 schedule
nxt = {}
for m in schedule["weeks"]["4"]:
    nxt[m["away"]] = f'at {teams_meta[m["home"]]["teamName"]}'
    nxt[m["home"]] = f'vs {teams_meta[m["away"]]["teamName"]}'

out = {"week": 3, "publishedAt": "2026-09-29", "deck": editorial["deck"], "teams": []}
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

json.dump(out, open(f"{ROOT}/data/weeks/week-3.json", "w"), indent=2)
print("odds sum:", round(sum(t["titleOdds"] for t in out["teams"]), 1))
print("playoff sum:", round(sum(t["playoffOdds"] for t in out["teams"]), 1))
for t in out["teams"]:
    mv = PRE_RANK[t["teamId"]] - t["powerRank"]
    delta_sum = round(sum(m["delta"] for m in t["movementReasons"]), 1)
    print(f'#{t["powerRank"]:>2} {t["teamId"]:<28} {"↑" + str(mv) if mv > 0 else "↓" + str(-mv) if mv < 0 else "—":>3}  {t["powerScore"]:>5}  {t["titleOdds"]:>4}%  {t["record"]["wins"]}-{t["record"]["losses"]}  PF {t["pointsFor"]:>6}  Δreasons {delta_sum}')

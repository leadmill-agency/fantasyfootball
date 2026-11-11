#!/usr/bin/env python3
"""Build data/weeks/week-9.json — the ninth in-season power snapshot.

Board: Version B formula (results = 20% win% + 40% all-play% + 40% scoring vs
league average; blend 70/30 with structure) plus Rameel's calls on 2026-11-11:
DEDDYBABA holds 2nd (formula 4th), Bizzy 5th over MBK 6th (formula flipped,
0.3 apart), Bazan 10th over IVaafay 11th (formula flipped).
Rosters: Week 9 lineups as played, from the ESPN box scores (final, 2026-11-11).
"""
import json, math, os

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
grades = {t["teamId"]: t["grade"] for t in json.load(open(f"{ROOT}/data/draft-grades.json"))["teams"]}
teams_meta = {t["teamId"]: t for t in json.load(open(f"{ROOT}/data/teams.json"))["teams"]}
editorial = json.load(open(f"{ROOT}/scripts/editorial-week-9.json"))
schedule = json.load(open(f"{ROOT}/data/schedule.json"))

PRE_RANK = {"hnfnr-aint-busy": 1, "deddybaba": 2, "chief-sheikh": 3, "team-mbk": 4, "team-noor": 5,
            "bizzy": 6, "rambam": 7, "gang-green": 8, "bazan": 9, "i-eat-ass": 10,
            "ivaafay": 11, "mustafas-magnificent-team": 12}

# rank, teamId, powerScore, tier, ceilingRank
BOARD = [
    (1, "hnfnr-aint-busy", 91.4, "Favorite", 1),
    (2, "deddybaba", 87.0, "Favorite", 7),
    (3, "chief-sheikh", 86.2, "Contender", 3),
    (4, "team-noor", 83.4, "Contender", 2),
    (5, "bizzy", 82.0, "Contender", 5),
    (6, "team-mbk", 80.8, "Playoff-caliber", 4),
    (7, "rambam", 76.0, "Playoff-caliber", 6),
    (8, "gang-green", 72.6, "Playoff-caliber", 8),
    (9, "i-eat-ass", 71.0, "Playoff-caliber", 11),
    (10, "bazan", 67.4, "Fringe contender", 12),
    (11, "ivaafay", 66.6, "Fringe contender", 9),
    (12, "mustafas-magnificent-team", 63.6, "Fragile", 10),
]

ARCHETYPE = {"team-noor": "The Complete Team", "bizzy": "The RB Machine", "team-mbk": "The Floor Monster",
             "bazan": "The Nuclear Core", "rambam": "The Venture Portfolio",
             "mustafas-magnificent-team": "The Deep Bench", "hnfnr-aint-busy": "The Stars Up Top",
             "i-eat-ass": "The Volatility Bet", "chief-sheikh": "The WR Superteam",
             "gang-green": "The Moonshot", "ivaafay": "The Bijan Build", "deddybaba": "The No-RB Experiment"}

MOVEMENT = {
  "hnfnr-aint-busy": [(1.0, "110.42; 8-1, 72-27 all-play"), (-0.6, "Stevenson's knee; Henry 5.58, Flowers 3.8")],
  "deddybaba": [(2.4, "133.38, six straight wins, 7-2"), (1.0, "Purdy 25.28, Bucky 26.5; ledger +97.20 over Noor"), (-2.6, "Puka Nacua headed to IR, at least four games")],
  "chief-sheikh": [(1.6, "117.18, three straight wins; 6-3, 63-36 all-play"), (-0.4, "Jefferson 7.3, McBride 8.9; Skattebo out")],
  "team-noor": [(1.4, "103.26, a win; 1,024.02 points, second in the league"), (-0.6, "Patriots D/ST −5.0; Waddle's concussion")],
  "bizzy": [(2.6, "144.66, the weekly high"), (1.2, "Walker 34.3, Lamb 28.5; 1,003.7 points, fourth"), (0.6, "Lamb trade ledger flipped to Bizzy +2.90")],
  "team-mbk": [(-2.2, "87.6, lost by 57"), (-1.6, "Jacobs' hand injury, 0.5"), (0.4, "57-42 all-play; Dell 18.5 and Concepcion 16.8 on the bench")],
  "rambam": [(1.8, "123.36, the third-best score of the week; Stroud 35.36"), (-0.6, "Lost anyway, 4-5; Taylor 6.9")],
  "gang-green": [(-1.0, "Fourth straight loss, by 1.58"), (-0.4, "Young 20.34 and Hill 16.7 on the bench")],
  "i-eat-ass": [(1.6, "101.64, three wins in four weeks; McCaffrey 21.7"), (-0.4, "Evans and Montgomery still out")],
  "bazan": [(-2.0, "62.72, the week's low; Willis 3.82 at quarterback"), (-1.2, "Kyler dropped, Lamar on IR; Drew Lock is next")],
  "ivaafay": [(0.8, "110.06, the sixth-best score of the week"), (-1.0, "Fifth straight loss, 2-7")],
  "mustafas-magnificent-team": [(-1.0, "85.78, third straight loss; McConkey 0.0")],
}

STOCK = {
  "hnfnr-aint-busy": ("Jonah Coleman", "Derrick Henry"),
  "deddybaba": ("Bucky Irving", "Puka Nacua"),
  "chief-sheikh": ("Jordan Love", "Justin Jefferson"),
  "team-noor": ("Christian Watson", "Patriots D/ST"),
  "bizzy": ("Kenneth Walker III", "Colston Loveland"),
  "team-mbk": ("Tank Dell", "Josh Jacobs"),
  "rambam": ("C.J. Stroud", "Jonathan Taylor"),
  "gang-green": ("Bryce Young", "Ashton Jeanty"),
  "i-eat-ass": ("Christian McCaffrey", "Jameson Williams"),
  "bazan": ("Audric Estime", "Malik Willis"),
  "ivaafay": ("Bijan Robinson", "Jordan Addison"),
  "mustafas-magnificent-team": ("Bills D/ST", "Ladd McConkey"),
}

DEVELOPMENT = {
  "hnfnr-aint-busy": "110.42 with Pollard on bye; 8-1 and 73 points clear of the league in scoring.",
  "deddybaba": "Sixth straight win, 133.38; Puka Nacua (28.0) hurt his knee late and is headed to IR.",
  "chief-sheikh": "Third straight win; Love 36.18. Put Jefferson \"on block for an RB.\"",
  "team-noor": "Won by 1.58 with the Patriots D/ST at −5.0 and the 49ers D/ST's 19.0 on the bench.",
  "bizzy": "144.66, the weekly high and a second $100; the Lamb trade ledger flipped to Bizzy +2.90.",
  "team-mbk": "87.6; Jacobs 0.5 with a hand injury. Dell, dropped and re-signed, scored 18.5 on the bench.",
  "rambam": "123.36 and lost by ten; Stroud 35.36 started over Daniels. Conceded Thursday at 7:55 PM.",
  "gang-green": "Lost by 1.58 with Young's 20.34 and Hill's 16.7 on the bench; four straight losses.",
  "i-eat-ass": "Three wins in four weeks; Cousins traded to Minnesota, Mendoza claimed off waivers.",
  "bazan": "62.72 with Malik Willis (3.82); 15 moves this week, 56 on the season. \"Every qb I touch gets hurt.\"",
  "ivaafay": "110.06 and a fifth straight loss, by 7.12, with Sutton's 13.0 on the bench. Luck: −2.18.",
  "mustafas-magnificent-team": "McConkey 0.0 with back spasms; third straight loss. Signed MarShawn Lloyd.",
}

S = ["QB", "RB", "RB", "WR", "WR", "TE", "FLEX", "D/ST", "K"]
def P(name, pos, nfl): return {"player": name, "position": pos, "nflTeam": nfl}
ROSTERS = {
 "deddybaba": {
   "starters": [P("Brock Purdy","QB","SF"),P("Ollie Gordon II","RB","MIA"),P("Bucky Irving","RB","TB"),P("Puka Nacua","WR","LAR"),P("Rashee Rice","WR","KC"),P("Tucker Kraft","TE","GB"),P("Bhayshul Tuten","RB","JAX"),P("Jaguars D/ST","D/ST","JAX"),P("Ka'imi Fairbairn","K","HOU")],
   "bench": [P("Kenny Gainwell","RB","TB"),P("Josh Downs","WR","KC"),P("Broncos D/ST","D/ST","DEN"),P("Antonio Williams","WR","WSH"),P("Tyler Bass","K","BUF"),P("James Conner (IR)","RB","ARI"),P("RJ Harvey (IR)","RB","DEN")]},
 "rambam": {
   "starters": [P("C.J. Stroud","QB","HOU"),P("Kaelon Black","RB","SF"),P("Jonathan Taylor","RB","IND"),P("Matthew Golden","WR","GB"),P("Ryan Flournoy","WR","DAL"),P("Tyler Warren","TE","IND"),P("Rome Odunze","WR","CHI"),P("Saints D/ST","D/ST","NO"),P("Spencer Shrader","K","IND")],
   "bench": [P("Emeka Egbuka","WR","TB"),P("Jayden Daniels","QB","WSH"),P("Xavier Worthy","WR","KC"),P("Emanuel Wilson","RB","SEA"),P("TreVeyon Henderson","RB","NE"),P("Seth McGowan","RB","IND"),P("Travis Etienne Jr. (IR)","RB","NO")]},
 "bizzy": {
   "starters": [P("Drake Maye","QB","NE"),P("Kenneth Walker III","RB","KC"),P("Chase Brown","RB","CIN"),P("Nico Collins","WR","HOU"),P("CeeDee Lamb","WR","DAL"),P("Colston Loveland","TE","CHI"),P("DeMario Douglas","WR","NE"),P("Rams D/ST","D/ST","LAR"),P("Chase McLaughlin","K","TB")],
   "bench": [P("Rachaad White","RB","WSH"),P("Deebo Samuel Sr.","WR","SF"),P("Tyler Shough","QB","NO"),P("Emmett Johnson","RB","KC"),P("Samaje Perine","RB","CIN"),P("Keenan Allen","WR","SF"),P("Tank Bigsby (IR)","RB","PHI"),P("Alec Pierce (IR)","WR","IND")]},
 "team-mbk": {
   "starters": [P("Dak Prescott","QB","DAL"),P("Jahmyr Gibbs","RB","DET"),P("Josh Jacobs","RB","GB"),P("Drake London","WR","ATL"),P("Tee Higgins","WR","CIN"),P("Sam LaPorta","TE","DET"),P("Quinshon Judkins","RB","CLE"),P("Seahawks D/ST","D/ST","SEA"),P("Matt Gay","K","LV")],
   "bench": [P("Rico Dowdle","RB","PIT"),P("Wan'Dale Robinson","WR","TEN"),P("Matthew Stafford","QB","LAR"),P("KC Concepcion","WR","CLE"),P("Michael Mayer","TE","LV"),P("Tank Dell","WR","HOU"),P("Brian Robinson Jr. (IR)","RB","ATL"),P("Michael Pittman Jr. (IR)","WR","PIT")]},
 "ivaafay": {
   "starters": [P("Caleb Williams","QB","CHI"),P("Bijan Robinson","RB","ATL"),P("Javonte Williams","RB","DAL"),P("Jordan Addison","WR","MIN"),P("Khalil Shakir","WR","BUF"),P("Kyle Pitts Sr.","TE","ATL"),P("Jadarian Price","RB","SEA"),P("Bears D/ST","D/ST","CHI"),P("Jake Bates","K","DET")],
   "bench": [P("George Pickens","WR","DAL"),P("DK Metcalf","WR","PIT"),P("Jordan Mason","RB","MIN"),P("Alvin Kamara","RB","NO"),P("Brenton Strange","TE","JAX"),P("Courtland Sutton","WR","DEN"),P("Davante Adams (IR)","WR","LAR")]},
 "chief-sheikh": {
   "starters": [P("Jordan Love","QB","GB"),P("Blake Corum","RB","LAR"),P("Dylan Sampson","RB","CLE"),P("Amon-Ra St. Brown","WR","DET"),P("Justin Jefferson","WR","MIN"),P("Trey McBride","TE","ARI"),P("Parker Washington","WR","JAX"),P("Texans D/ST","D/ST","HOU"),P("Brandon Aubrey","K","DAL")],
   "bench": [P("Cam Skattebo","RB","NYG"),P("Jaylen Warren","RB","PIT"),P("Braelon Allen","RB","NYJ"),P("Omar Cooper Jr.","WR","NYJ"),P("Travis Hunter","WR","JAX"),P("Caleb Douglas","WR","MIA"),P("Mack Hollins","WR","NE"),P("Brandon Aiyuk (IR)","WR","SF")]},
 "hnfnr-aint-busy": {
   "starters": [P("Joe Burrow","QB","CIN"),P("Derrick Henry","RB","BAL"),P("Jonah Coleman","RB","DEN"),P("Jaxon Smith-Njigba","WR","SEA"),P("Zay Flowers","WR","BAL"),P("Brock Bowers","TE","LV"),P("Rhamondre Stevenson","RB","NE"),P("Browns D/ST","D/ST","CLE"),P("Jason Myers","K","SEA")],
   "bench": [P("Tony Pollard","RB","TEN"),P("Brian Thomas Jr.","WR","JAX"),P("Tyler Allgeier","RB","ARI"),P("Dalton Kincaid","TE","BUF"),P("Cameron Dicker","K","LAC"),P("Denzel Boston","WR","CLE"),P("Michael Wilson (IR)","WR","ARI")]},
 "mustafas-magnificent-team": {
   "starters": [P("Patrick Mahomes","QB","KC"),P("Saquon Barkley","RB","PHI"),P("Zach Charbonnet","RB","SEA"),P("Ladd McConkey","WR","LAC"),P("Makai Lemon","WR","PHI"),P("Isaiah Likely","TE","NYG"),P("DJ Moore","WR","BUF"),P("Bills D/ST","D/ST","BUF"),P("Cairo Santos","K","CHI")],
   "bench": [P("Omarion Hampton","RB","LAC"),P("DeVonta Smith","WR","PHI"),P("Marvin Harrison Jr.","WR","HOU"),P("Travis Kelce","TE","KC"),P("Vikings D/ST","D/ST","MIN"),P("Will Reichard","K","MIN"),P("Germie Bernard","WR","PIT")]},
 "team-noor": {
   "starters": [P("Josh Allen","QB","BUF"),P("Breece Hall","RB","NYJ"),P("Kyren Williams","RB","LAR"),P("Ja'Marr Chase","WR","CIN"),P("Christian Watson","WR","GB"),P("George Kittle","TE","SF"),P("Demarcus Robinson","WR","SF"),P("Patriots D/ST","D/ST","NE"),P("Evan McPherson","K","CIN")],
   "bench": [P("Jaylen Waddle","WR","DEN"),P("Aaron Jones Sr.","RB","MIN"),P("J.K. Dobbins","RB","DEN"),P("Mark Andrews","TE","BAL"),P("Jared Goff","QB","DET"),P("Tre Tucker","WR","LV"),P("49ers D/ST","D/ST","SF")]},
 "gang-green": {
   "starters": [P("Trevor Lawrence","QB","JAX"),P("Ashton Jeanty","RB","LV"),P("Chuba Hubbard","RB","CAR"),P("Tetairoa McMillan","WR","CAR"),P("Luther Burden III","WR","CHI"),P("Harold Fannin Jr.","TE","CLE"),P("Jordyn Tyson","WR","NO"),P("Lions D/ST","D/ST","DET"),P("Cam Little","K","JAX")],
   "bench": [P("Garrett Wilson","WR","NYJ"),P("Stefon Diggs","WR","WSH"),P("Mike Washington Jr.","RB","LV"),P("Bryce Young","QB","CAR"),P("Justice Hill","RB","BAL"),P("Hunter Henry","TE","NE"),P("Tyjae Spears","RB","TEN"),P("Jonathon Brooks (IR)","RB","CAR")]},
 "bazan": {
   "starters": [P("Malik Willis","QB","MIA"),P("James Cook III","RB","BUF"),P("D'Andre Swift","RB","CHI"),P("Malik Nabers","WR","NYG"),P("Adonai Mitchell","WR","NYJ"),P("Greg Dulcich","TE","MIA"),P("Devin Singletary","RB","NYG"),P("Chiefs D/ST","D/ST","KC"),P("Andre Szmyt","K","CLE")],
   "bench": [P("Kyle Monangai","RB","CHI"),P("Jalen Coker","WR","CAR"),P("Ray Davis","RB","BUF"),P("Malik Washington","WR","MIA"),P("Audric Estime","RB","NO"),P("Lamar Jackson (IR)","QB","BAL"),P("Terrance Ferguson (IR)","TE","LAR"),P("A.J. Brown (IR)","WR","NE")]},
 "i-eat-ass": {
   "starters": [P("Kirk Cousins","QB","MIN"),P("Christian McCaffrey","RB","SF"),P("Woody Marks","RB","HOU"),P("Chris Olave","WR","NO"),P("Jameson Williams","WR","DET"),P("Mike Gesicki","TE","CIN"),P("Jakobi Meyers","WR","JAX"),P("Giants D/ST","D/ST","NYG"),P("Dominic Zvada","K","NYG")],
   "bench": [P("Devaughn Vele","WR","NO"),P("T.J. Hockenson","TE","MIN"),P("Carnell Tate","WR","TEN"),P("David Montgomery","RB","HOU"),P("Mike Evans","WR","SF"),P("Chris Rodriguez Jr.","RB","JAX"),P("Joe Milton","QB","PHI"),P("Jeremiyah Love (IR)","RB","ARI")]},
}
for tid, r in ROSTERS.items():
    slots = [{"slot": s, **p} for s, p in zip(S, r["starters"])]
    ROSTERS[tid] = {"starters": slots, "bench": r["bench"]}

# cumulative records + PF from all results through week 5
rec = {t: {"wins": 0, "losses": 0} for t in PRE_RANK}
pf = {t: 0.0 for t in PRE_RANK}
for wk in (1, 2, 3, 4, 5, 6, 7, 8, 9):
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
for m in schedule["weeks"]["10"]:
    nxt[m["away"]] = f'at {teams_meta[m["home"]]["teamName"]}'
    nxt[m["home"]] = f'vs {teams_meta[m["away"]]["teamName"]}'

out = {"week": 9, "publishedAt": "2026-11-11", "deck": editorial["deck"], "teams": []}
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

json.dump(out, open(f"{ROOT}/data/weeks/week-9.json", "w"), indent=2)
print("odds sum:", round(sum(t["titleOdds"] for t in out["teams"]), 1))
for t in out["teams"]:
    mv = PRE_RANK[t["teamId"]] - t["powerRank"]
    delta_sum = round(sum(m["delta"] for m in t["movementReasons"]), 1)
    print(f'#{t["powerRank"]:>2} {t["teamId"]:<28} {"↑" + str(mv) if mv > 0 else "↓" + str(-mv) if mv < 0 else "—":>3}  {t["powerScore"]:>5}  {t["titleOdds"]:>4}%  {t["record"]["wins"]}-{t["record"]["losses"]}  PF {t["pointsFor"]:>6}  Δreasons {delta_sum}')

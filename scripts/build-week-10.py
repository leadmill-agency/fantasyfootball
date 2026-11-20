#!/usr/bin/env python3
"""Build data/weeks/week-10.json — the tenth in-season power snapshot.

Board: Version B formula (results = 20% win% + 40% all-play% + 40% scoring vs
league average; blend 70/30 with structure). Rameel said "update" on
2026-11-20 without overrides, so the recommended board shipped: DEDDYBABA 3rd
(formula 6th), Bizzy 4th and MBK 5th (formula 3rd and 4th), IEA 9th, RN 10th,
Bazan 11th, IVaafay 12th on record (formula IVaafay 9th, IEA 10th, RN 11th,
Bazan 12th).
Rosters: Week 10 lineups as played, from the ESPN box scores (final, 2026-11-20).
"""
import json, math, os

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
grades = {t["teamId"]: t["grade"] for t in json.load(open(f"{ROOT}/data/draft-grades.json"))["teams"]}
teams_meta = {t["teamId"]: t for t in json.load(open(f"{ROOT}/data/teams.json"))["teams"]}
editorial = json.load(open(f"{ROOT}/scripts/editorial-week-10.json"))
schedule = json.load(open(f"{ROOT}/data/schedule.json"))

PRE_RANK = {"hnfnr-aint-busy": 1, "deddybaba": 2, "chief-sheikh": 3, "team-noor": 4, "bizzy": 5,
            "team-mbk": 6, "rambam": 7, "gang-green": 8, "i-eat-ass": 9, "bazan": 10,
            "ivaafay": 11, "mustafas-magnificent-team": 12}

# rank, teamId, powerScore, tier, ceilingRank
BOARD = [
    (1, "hnfnr-aint-busy", 90.2, "Favorite", 1),
    (2, "chief-sheikh", 87.6, "Favorite", 2),
    (3, "deddybaba", 84.4, "Contender", 8),
    (4, "bizzy", 83.6, "Contender", 6),
    (5, "team-mbk", 82.8, "Contender", 3),
    (6, "team-noor", 80.6, "Playoff-caliber", 4),
    (7, "gang-green", 76.4, "Playoff-caliber", 7),
    (8, "rambam", 75.6, "Playoff-caliber", 5),
    (9, "i-eat-ass", 69.6, "Playoff-caliber", 11),
    (10, "mustafas-magnificent-team", 67.2, "Fringe contender", 9),
    (11, "bazan", 65.4, "Fringe contender", 12),
    (12, "ivaafay", 64.8, "Fragile", 10),
]

ARCHETYPE = {"team-noor": "The Complete Team", "bizzy": "The RB Machine", "team-mbk": "The Floor Monster",
             "bazan": "The Nuclear Core", "rambam": "The Venture Portfolio",
             "mustafas-magnificent-team": "The Deep Bench", "hnfnr-aint-busy": "The Stars Up Top",
             "i-eat-ass": "The Volatility Bet", "chief-sheikh": "The WR Superteam",
             "gang-green": "The Moonshot", "ivaafay": "The Bijan Build", "deddybaba": "The No-RB Experiment"}

MOVEMENT = {
  "hnfnr-aint-busy": [(-1.6, "104.96, lost to MBK; Steelers D/ST −7.0, Bowers 2.8"), (0.4, "Still 8-2, 76-34 all-play; Burrow 33.16")],
  "chief-sheikh": [(1.8, "126.7, beat DEDDYBABA; four straight wins, 7-3"), (-0.4, "Love 10.8, McBride 6.2; Love on bye next")],
  "deddybaba": [(-1.2, "111.56; six-game winning streak ended"), (-1.8, "Puka Nacua out for the regular season after knee surgery"), (0.4, "Purdy 31.66; ledger +106.52 over Noor")],
  "bizzy": [(2.8, "151.42, back-to-back weekly highs; 1,155.12 points, second"), (0.8, "Emmett Johnson 32.1, Deebo 24.4, Chase Brown 24.3"), (-2.0, "Drake Maye's fractured fibula; Walker out")],
  "team-mbk": [(2.4, "136.16, beat the No. 1 team; Gibbs 40.7"), (0.2, "66-44 all-play, tied for third"), (-0.6, "Jacobs out; Higgins 9.1")],
  "team-noor": [(-2.0, "93.14, lost to RN by 35; 4-6"), (-0.8, "Kyren 4.2, Watson 5.2; Aaron Jones' MCL")],
  "gang-green": [(3.0, "136.88, ended a four-game skid; Hubbard 31.7, Lawrence 26.78"), (0.8, "5-5, sixth in the standings")],
  "rambam": [(0.6, "Won, 5-5"), (-1.0, "89.24, second-lowest score of the week; 49-61 all-play")],
  "i-eat-ass": [(-1.8, "90.28, lost by 46; 43-67 all-play"), (0.4, "McCaffrey 44.3, the season's best individual game")],
  "mustafas-magnificent-team": [(3.0, "128.42, beat Noor by 35; Mahomes 35.42, Likely 23.2"), (0.6, "Hampton 17.0, Moore 17.4; 4-6")],
  "bazan": [(-1.6, "66.6, the week's low for the third time in four weeks"), (-0.4, "38-72 all-play, fewest points; 66 roster moves")],
  "ivaafay": [(-1.4, "Sixth straight loss, 2-8"), (-0.4, "Desk drops him to last on record despite 115.82")],
}

STOCK = {
  "hnfnr-aint-busy": ("Joe Burrow", "Steelers D/ST"),
  "chief-sheikh": ("Cam Skattebo", "Trey McBride"),
  "deddybaba": ("Brock Purdy", "Puka Nacua"),
  "bizzy": ("Emmett Johnson", "Drake Maye"),
  "team-mbk": ("Jahmyr Gibbs", "Tee Higgins"),
  "team-noor": ("Ja'Marr Chase", "Kyren Williams"),
  "gang-green": ("Chuba Hubbard", "Tetairoa McMillan"),
  "rambam": ("Ryan Flournoy", "Tyler Warren"),
  "i-eat-ass": ("Christian McCaffrey", "Chris Olave"),
  "mustafas-magnificent-team": ("Patrick Mahomes", "Germie Bernard"),
  "bazan": ("James Cook III", "Jalen Coker"),
  "ivaafay": ("George Pickens", "Javonte Williams"),
}

DEVELOPMENT = {
  "hnfnr-aint-busy": "Lost 136.16-104.96; started Burrow (33.16) and the Steelers D/ST that faced him (−7.0).",
  "chief-sheikh": "Ended Asim's six-game streak; Skattebo 25.7, Washington 24.7. Four straight wins.",
  "deddybaba": "Streak over at six; Puka Nacua had knee surgery and is out for the regular season.",
  "bizzy": "151.42, a second straight weekly high and third $100; Drake Maye fractured his fibula.",
  "team-mbk": "Beat the No. 1 team behind Gibbs' 40.7; Dak's 34.42 sat behind Stafford's 19.76.",
  "team-noor": "Lost to RN by 35; the 49ers D/ST scored −1.0 a week after the Patriots scored −5.0.",
  "gang-green": "136.88, a season high, ends a four-game skid; Lawrence 26.78 started over Young.",
  "rambam": "Won 89.24-66.6; Stroud 20.44 started, Daniels 20.76 sat. Lamb ledger: Bizzy +64.70.",
  "i-eat-ass": "McCaffrey's 44.3 is the season's best game; the other eight starters scored 45.98.",
  "mustafas-magnificent-team": "128.42 with Barkley, Smith and Lemon on bye; Mahomes 35.42. Tied for the last playoff spot.",
  "bazan": "66.6, the week's low again; a fifth starting QB in five weeks (Lock), Bo Nix on the bench.",
  "ivaafay": "115.82, sixth-best in the league, and a sixth straight loss. Luck: −2.73, a record.",
}

S = ["QB", "RB", "RB", "WR", "WR", "TE", "FLEX", "D/ST", "K"]
def P(name, pos, nfl): return {"player": name, "position": pos, "nflTeam": nfl}
ROSTERS = {
 "rambam": {
   "starters": [P("C.J. Stroud","QB","HOU"),P("Kaelon Black","RB","SF"),P("Jonathan Taylor","RB","IND"),P("Matthew Golden","WR","GB"),P("Ryan Flournoy","WR","DAL"),P("Tyler Warren","TE","IND"),P("Travis Etienne Jr.","RB","NO"),P("Packers D/ST","D/ST","GB"),P("Spencer Shrader","K","IND")],
   "bench": [P("Emeka Egbuka","WR","TB"),P("Rome Odunze","WR","CHI"),P("Jayden Daniels","QB","WSH"),P("Xavier Worthy","WR","KC"),P("Emanuel Wilson","RB","SEA"),P("Seth McGowan","RB","IND"),P("TreVeyon Henderson (IR)","RB","NE")]},
 "bazan": {
   "starters": [P("Drew Lock","QB","SEA"),P("James Cook III","RB","BUF"),P("Audric Estime","RB","NO"),P("Malik Nabers","WR","NYG"),P("Adonai Mitchell","WR","NYJ"),P("Eli Raridon","TE","NE"),P("Jalen Coker","WR","CAR"),P("Chiefs D/ST","D/ST","KC"),P("Chris Boswell","K","PIT")],
   "bench": [P("D'Andre Swift","RB","CHI"),P("Kyle Monangai","RB","CHI"),P("Ray Davis","RB","BUF"),P("Konata Mumpfield","WR","LAR"),P("Carnell Tate","WR","TEN"),P("Darren Waller","TE","CAR"),P("Bo Nix","QB","DEN"),P("Lamar Jackson (IR)","QB","BAL")]},
 "ivaafay": {
   "starters": [P("Aaron Rodgers","QB","PIT"),P("Bijan Robinson","RB","ATL"),P("Javonte Williams","RB","DAL"),P("George Pickens","WR","DAL"),P("DK Metcalf","WR","PIT"),P("Kyle Pitts Sr.","TE","ATL"),P("Jadarian Price","RB","SEA"),P("Commanders D/ST","D/ST","WSH"),P("Jake Bates","K","DET")],
   "bench": [P("Caleb Williams","QB","CHI"),P("Jordan Mason","RB","MIN"),P("Jordan Addison","WR","MIN"),P("Alvin Kamara","RB","NO"),P("Khalil Shakir","WR","BUF"),P("Bears D/ST","D/ST","CHI"),P("Courtland Sutton","WR","DEN"),P("Davante Adams (IR)","WR","LAR")]},
 "bizzy": {
   "starters": [P("Drake Maye","QB","NE"),P("Emmett Johnson","RB","KC"),P("Chase Brown","RB","CIN"),P("Nico Collins","WR","HOU"),P("CeeDee Lamb","WR","DAL"),P("Darnell Washington","TE","PIT"),P("Deebo Samuel Sr.","WR","SF"),P("Rams D/ST","D/ST","LAR"),P("Jason Sanders","K","NYJ")],
   "bench": [P("Kenneth Walker III","RB","KC"),P("Colston Loveland","TE","CHI"),P("Rachaad White","RB","WSH"),P("Tyler Shough","QB","NO"),P("Keenan Allen","WR","SF"),P("DeMario Douglas","WR","NE"),P("Corey Kiner","RB","NE"),P("Alec Pierce (IR)","WR","IND")]},
 "team-mbk": {
   "starters": [P("Matthew Stafford","QB","LAR"),P("Jahmyr Gibbs","RB","DET"),P("Quinshon Judkins","RB","CLE"),P("Drake London","WR","ATL"),P("Tee Higgins","WR","CIN"),P("Brenton Strange","TE","JAX"),P("KC Concepcion","WR","CLE"),P("Seahawks D/ST","D/ST","SEA"),P("Matt Gay","K","LV")],
   "bench": [P("Josh Jacobs","RB","GB"),P("Sam LaPorta","TE","DET"),P("Dak Prescott","QB","DAL"),P("Rico Dowdle","RB","PIT"),P("Tank Dell","WR","HOU"),P("Sione Vaki","RB","DET"),P("Wan'Dale Robinson (IR)","WR","TEN"),P("Michael Pittman Jr. (IR)","WR","PIT")]},
 "hnfnr-aint-busy": {
   "starters": [P("Joe Burrow","QB","CIN"),P("Derrick Henry","RB","BAL"),P("Tony Pollard","RB","TEN"),P("Jaxon Smith-Njigba","WR","SEA"),P("Zay Flowers","WR","BAL"),P("Brock Bowers","TE","LV"),P("Denzel Boston","WR","CLE"),P("Steelers D/ST","D/ST","PIT"),P("Jason Myers","K","SEA")],
   "bench": [P("Rhamondre Stevenson","RB","NE"),P("Brian Thomas Jr.","WR","JAX"),P("Tyler Allgeier","RB","ARI"),P("Dalton Kincaid","TE","BUF"),P("Cameron Dicker","K","LAC"),P("Jonah Coleman","RB","DEN"),P("Michael Wilson (IR)","WR","ARI"),P("Jacory Croskey-Merritt (IR)","RB","WSH")]},
 "chief-sheikh": {
   "starters": [P("Jordan Love","QB","GB"),P("Cam Skattebo","RB","NYG"),P("Jaylen Warren","RB","PIT"),P("Justin Jefferson","WR","MIN"),P("Parker Washington","WR","JAX"),P("Trey McBride","TE","ARI"),P("Amon-Ra St. Brown","WR","DET"),P("Texans D/ST","D/ST","HOU"),P("Brandon Aubrey","K","DAL")],
   "bench": [P("Blake Corum","RB","LAR"),P("Braelon Allen","RB","NYJ"),P("Omar Cooper Jr.","WR","NYJ"),P("Dylan Sampson","RB","CLE"),P("Mack Hollins","WR","NE"),P("Kaleb Johnson","RB","GB"),P("Buccaneers D/ST","D/ST","TB"),P("Brandon Aiyuk (IR)","WR","SF")]},
 "deddybaba": {
   "starters": [P("Brock Purdy","QB","SF"),P("Bhayshul Tuten","RB","JAX"),P("Ollie Gordon II","RB","MIA"),P("Rashee Rice","WR","KC"),P("Antonio Williams","WR","WSH"),P("Tucker Kraft","TE","GB"),P("Josh Downs","WR","KC"),P("Jaguars D/ST","D/ST","JAX"),P("Ka'imi Fairbairn","K","HOU")],
   "bench": [P("Kenny Gainwell","RB","TB"),P("Broncos D/ST","D/ST","DEN"),P("Bucky Irving","RB","TB"),P("Tyler Bass","K","BUF"),P("Puka Nacua (IR)","WR","LAR"),P("James Conner (IR)","RB","ARI"),P("RJ Harvey (IR)","RB","DEN")]},
 "mustafas-magnificent-team": {
   "starters": [P("Patrick Mahomes","QB","KC"),P("Omarion Hampton","RB","LAC"),P("Zach Charbonnet","RB","SEA"),P("DJ Moore","WR","BUF"),P("Germie Bernard","WR","PIT"),P("Isaiah Likely","TE","NYG"),P("Travis Kelce","TE","KC"),P("Bills D/ST","D/ST","BUF"),P("Brandon McManus","K","LAR")],
   "bench": [P("Saquon Barkley","RB","PHI"),P("Ladd McConkey","WR","LAC"),P("Vikings D/ST","D/ST","MIN"),P("Makai Lemon","WR","PHI"),P("MarShawn Lloyd","RB","GB"),P("Efton Chism III","WR","NE"),P("Kimani Vidal","RB","LAC"),P("DeVonta Smith (IR)","WR","PHI")]},
 "team-noor": {
   "starters": [P("Josh Allen","QB","BUF"),P("Breece Hall","RB","NYJ"),P("Kyren Williams","RB","LAR"),P("Ja'Marr Chase","WR","CIN"),P("Christian Watson","WR","GB"),P("George Kittle","TE","SF"),P("Tutu Atwell","WR","LAR"),P("49ers D/ST","D/ST","SF"),P("Evan McPherson","K","CIN")],
   "bench": [P("Jaylen Waddle","WR","DEN"),P("Aaron Jones Sr.","RB","MIN"),P("J.K. Dobbins","RB","DEN"),P("Mark Andrews","TE","BAL"),P("Demarcus Robinson","WR","SF"),P("Jared Goff","QB","DET"),P("Tre Tucker","WR","LV")]},
 "gang-green": {
   "starters": [P("Trevor Lawrence","QB","JAX"),P("Ashton Jeanty","RB","LV"),P("Chuba Hubbard","RB","CAR"),P("Tetairoa McMillan","WR","CAR"),P("Stefon Diggs","WR","WSH"),P("Harold Fannin Jr.","TE","CLE"),P("Garrett Wilson","WR","NYJ"),P("Ravens D/ST","D/ST","BAL"),P("Cam Little","K","JAX")],
   "bench": [P("Luther Burden III","WR","CHI"),P("Mike Washington Jr.","RB","LV"),P("Jordyn Tyson","WR","NO"),P("Bryce Young","QB","CAR"),P("Justice Hill","RB","BAL"),P("Hunter Henry","TE","NE"),P("Tyjae Spears","RB","TEN"),P("Jonathon Brooks (IR)","RB","CAR")]},
 "i-eat-ass": {
   "starters": [P("Kirk Cousins","QB","MIN"),P("Christian McCaffrey","RB","SF"),P("Woody Marks","RB","HOU"),P("Chris Olave","WR","NO"),P("Jameson Williams","WR","DET"),P("Mike Gesicki","TE","CIN"),P("A.J. Brown","WR","NE"),P("Giants D/ST","D/ST","NYG"),P("Dominic Zvada","K","NYG")],
   "bench": [P("Devaughn Vele","WR","NO"),P("T.J. Hockenson","TE","MIN"),P("David Montgomery","RB","HOU"),P("Mike Evans","WR","SF"),P("Jakobi Meyers","WR","JAX"),P("Chris Rodriguez Jr.","RB","JAX"),P("Fernando Mendoza","QB","LV"),P("Jeremiyah Love (IR)","RB","ARI")]},
}
for tid, r in ROSTERS.items():
    slots = [{"slot": s, **p} for s, p in zip(S, r["starters"])]
    ROSTERS[tid] = {"starters": slots, "bench": r["bench"]}

# cumulative records + PF from all results through week 5
rec = {t: {"wins": 0, "losses": 0} for t in PRE_RANK}
pf = {t: 0.0 for t in PRE_RANK}
for wk in (1, 2, 3, 4, 5, 6, 7, 8, 9, 10):
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
for m in schedule["weeks"]["11"]:
    nxt[m["away"]] = f'at {teams_meta[m["home"]]["teamName"]}'
    nxt[m["home"]] = f'vs {teams_meta[m["away"]]["teamName"]}'

out = {"week": 10, "publishedAt": "2026-11-20", "deck": editorial["deck"], "teams": []}
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

json.dump(out, open(f"{ROOT}/data/weeks/week-10.json", "w"), indent=2)
print("odds sum:", round(sum(t["titleOdds"] for t in out["teams"]), 1))
for t in out["teams"]:
    mv = PRE_RANK[t["teamId"]] - t["powerRank"]
    delta_sum = round(sum(m["delta"] for m in t["movementReasons"]), 1)
    print(f'#{t["powerRank"]:>2} {t["teamId"]:<28} {"↑" + str(mv) if mv > 0 else "↓" + str(-mv) if mv < 0 else "—":>3}  {t["powerScore"]:>5}  {t["titleOdds"]:>4}%  {t["record"]["wins"]}-{t["record"]["losses"]}  PF {t["pointsFor"]:>6}  Δreasons {delta_sum}')

#!/usr/bin/env python3
"""Build data/weeks/week-7.json — the seventh in-season power snapshot.

Board: Version B formula (results = 20% win% + 40% all-play% + 40% scoring vs
league average; blend 70/30 with structure) plus Rameel's calls on 2026-10-27:
DEDDYBABA to 4th (formula 7th), everyone between pushed down; Bazan 10th,
IVaafay 11th, RN 12th (formula had IVaafay 8th, IEA 10th, Bazan 11th).
Rosters: Week 7 lineups as played, from the ESPN box scores (final, 2026-10-27).
"""
import json, math, os

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
grades = {t["teamId"]: t["grade"] for t in json.load(open(f"{ROOT}/data/draft-grades.json"))["teams"]}
teams_meta = {t["teamId"]: t for t in json.load(open(f"{ROOT}/data/teams.json"))["teams"]}
editorial = json.load(open(f"{ROOT}/scripts/editorial-week-7.json"))
schedule = json.load(open(f"{ROOT}/data/schedule.json"))

PRE_RANK = {"team-noor": 1, "hnfnr-aint-busy": 2, "chief-sheikh": 3, "rambam": 4, "deddybaba": 5,
            "gang-green": 6, "team-mbk": 7, "bizzy": 8, "bazan": 9, "ivaafay": 10,
            "mustafas-magnificent-team": 11, "i-eat-ass": 12}

# rank, teamId, powerScore, tier, ceilingRank
BOARD = [
    (1, "hnfnr-aint-busy", 90.2, "Favorite", 1),
    (2, "team-noor", 85.4, "Favorite", 2),
    (3, "chief-sheikh", 84.6, "Contender", 4),
    (4, "deddybaba", 82.8, "Contender", 6),
    (5, "team-mbk", 81.6, "Contender", 3),
    (6, "bizzy", 78.0, "Playoff-caliber", 7),
    (7, "rambam", 77.0, "Playoff-caliber", 5),
    (8, "gang-green", 74.6, "Playoff-caliber", 8),
    (9, "i-eat-ass", 72.2, "Playoff-caliber", 12),
    (10, "bazan", 69.4, "Fringe contender", 10),
    (11, "ivaafay", 68.6, "Fringe contender", 9),
    (12, "mustafas-magnificent-team", 65.2, "Fragile", 11),
]

ARCHETYPE = {"team-noor": "The Complete Team", "bizzy": "The RB Machine", "team-mbk": "The Floor Monster",
             "bazan": "The Nuclear Core", "rambam": "The Venture Portfolio",
             "mustafas-magnificent-team": "The Deep Bench", "hnfnr-aint-busy": "The Stars Up Top",
             "i-eat-ass": "The Volatility Bet", "chief-sheikh": "The WR Superteam",
             "gang-green": "The Moonshot", "ivaafay": "The Bijan Build", "deddybaba": "The No-RB Experiment"}

MOVEMENT = {
  "hnfnr-aint-busy": [(2.4, "156.08, the weekly high; 6-1, 55-22 all-play, most points in the league"), (0.4, "Burrow back with 28.88")],
  "team-noor": [(-2.0, "86.22, lost the rematch with Allen on bye; Tucker 18.8 on the bench"), (-1.2, "3-4; Jones' knee, Kittle on bye next")],
  "chief-sheikh": [(2.0, "127.36, won the Sheikh bowl; 48-29 all-play"), (-1.2, "Texans D/ST 0.0, Jefferson 6.4; Skattebo's 18.6 on the bench")],
  "deddybaba": [(3.0, "5-2, four straight wins, second in the standings"), (1.2, "Bucky 23.5; trade ledger +63.84 over Noor"), (-1.0, "31-46 all-play; Luckbox Index +2.18, a league record")],
  "team-mbk": [(2.8, "132.0; Jacobs 17.6 in his return, Judkins 22.9, Higgins 23.8"), (1.6, "46-31 all-play; full roster for the first time")],
  "bizzy": [(2.0, "99.64, beat RN; Maye 27.44, Lamb 21.9, Loveland started"), (1.2, "745.68 points, sixth; 38-39 all-play")],
  "rambam": [(-3.0, "84.62, lost the Sheikh bowl by 42.74"), (-1.6, "3-4, 38-39 all-play"), (-0.8, "Worthy 2.6, Golden 6.9, Titans D/ST 0.0")],
  "gang-green": [(-2.4, "76.42, second straight loss; Young 5.42"), (-1.4, "30-47 all-play, eleventh; 4-3 record keeps him eighth")],
  "i-eat-ass": [(3.4, "114.9, two straight wins, 3-4"), (2.6, "Jameson Williams 23.6, Cousins 20.4"), (1.4, "Desk moves him above Bazan and IVaafay on record")],
  "bazan": [(-2.4, "61.4, the week's low; Panthers D/ST −3.0"), (-0.8, "Lamar out a third week; 37 moves")],
  "ivaafay": [(-2.0, "2-5, three straight losses"), (-0.8, "Desk call: record over the 40-37 all-play")],
  "mustafas-magnificent-team": [(-1.0, "76.4; Mahomes 6.0, Likely 2.2; 20-57 all-play"), (-0.8, "Override retired; Ivan has won two straight")],
}

STOCK = {
  "hnfnr-aint-busy": ("Tony Pollard", "Dominic Zvada"),
  "team-noor": ("Jared Goff", "Aaron Jones Sr."),
  "chief-sheikh": ("Trey McBride", "Texans D/ST"),
  "deddybaba": ("Bucky Irving", "Christian Kirk"),
  "team-mbk": ("Quinshon Judkins", "Sam LaPorta"),
  "bizzy": ("Drake Maye", "Nico Collins"),
  "rambam": ("Emanuel Wilson", "Xavier Worthy"),
  "gang-green": ("Luther Burden III", "Bryce Young"),
  "i-eat-ass": ("Jameson Williams", "Mike Evans"),
  "bazan": ("D'Andre Swift", "Panthers D/ST"),
  "ivaafay": ("Caleb Williams", "DK Metcalf"),
  "mustafas-magnificent-team": ("Makai Lemon", "Patrick Mahomes"),
}

DEVELOPMENT = {
  "hnfnr-aint-busy": "156.08, the weekly high and his second $100; Pollard 35.0, Burrow 28.88, JSN 26.8.",
  "team-noor": "Lost the Allen-for-Purdy rematch 98.22-86.22 with Allen on bye; Tucker 18.8 on the bench.",
  "chief-sheikh": "Won the Sheikh bowl by 42.74 with every star back; McBride 22.1.",
  "deddybaba": "Four straight wins, 5-2; declared his season over Thursday, then beat Haroon Sunday.",
  "team-mbk": "132.0 with Jacobs back (17.6), Judkins 22.9 and Higgins 23.8; Dak 23.28 on the bench.",
  "bizzy": "Started Loveland this time (16.4); Maye 27.44 on Thursday night.",
  "rambam": "84.62 in the Sheikh bowl with Daniels on bye; Worthy 2.6, Titans D/ST 0.0.",
  "gang-green": "Second straight loss; Young 5.42 in a 43-13 Panthers loss. \"I have full hate now.\"",
  "i-eat-ass": "Two straight wins; Jameson Williams 23.6 from the flex. Evans and Montgomery both out.",
  "bazan": "61.4, the week's low; conceded at 8:48 PM Thursday. Kyler started; Panthers D/ST −3.0.",
  "ivaafay": "108.12 and lost by 6.78; three straight losses at 40-37 all-play. Unluckiest in the league.",
  "mustafas-magnificent-team": "Mahomes 6.0, Likely 2.2; conceded Thursday night. Barkley back with 14.1.",
}

S = ["QB", "RB", "RB", "WR", "WR", "TE", "FLEX", "D/ST", "K"]
def P(name, pos, nfl): return {"player": name, "position": pos, "nflTeam": nfl}
ROSTERS = {
 "chief-sheikh": {
   "starters": [P("Jordan Love","QB","GB"),P("Jaylen Warren","RB","PIT"),P("Blake Corum","RB","LAR"),P("Amon-Ra St. Brown","WR","DET"),P("Justin Jefferson","WR","MIN"),P("Trey McBride","TE","ARI"),P("Braelon Allen","RB","NYJ"),P("Texans D/ST","D/ST","HOU"),P("Brandon Aubrey","K","DAL")],
   "bench": [P("Cam Skattebo","RB","NYG"),P("Parker Washington","WR","JAX"),P("Chiefs D/ST","D/ST","KC"),P("Kendrick Bourne","WR","ARI"),P("Omar Cooper Jr.","WR","NYJ"),P("Travis Hunter","WR","JAX"),P("Jaylen Wright","RB","MIA"),P("Dylan Sampson (IR)","RB","CLE")]},
 "rambam": {
   "starters": [P("C.J. Stroud","QB","HOU"),P("Emanuel Wilson","RB","SEA"),P("Jonathan Taylor","RB","IND"),P("Matthew Golden","WR","GB"),P("Xavier Worthy","WR","KC"),P("Hunter Henry","TE","NE"),P("Ryan Flournoy","WR","DAL"),P("Titans D/ST","D/ST","TEN"),P("Spencer Shrader","K","IND")],
   "bench": [P("Emeka Egbuka","WR","TB"),P("Tyler Warren","TE","IND"),P("Rome Odunze","WR","CHI"),P("Jayden Daniels","QB","WSH"),P("Kaelon Black","RB","SF"),P("TreVeyon Henderson","RB","NE"),P("Seth McGowan","RB","IND"),P("Travis Etienne Jr. (IR)","RB","NO")]},
 "bizzy": {
   "starters": [P("Drake Maye","QB","NE"),P("Kenneth Walker III","RB","KC"),P("Chase Brown","RB","CIN"),P("Nico Collins","WR","HOU"),P("CeeDee Lamb","WR","DAL"),P("Colston Loveland","TE","CHI"),P("DeMario Douglas","WR","NE"),P("Rams D/ST","D/ST","LAR"),P("Chase McLaughlin","K","TB")],
   "bench": [P("Rachaad White","RB","WSH"),P("Deebo Samuel Sr.","WR","SF"),P("Tyler Shough","QB","NO"),P("Malik Washington","WR","MIA"),P("Emmett Johnson","RB","KC"),P("Samaje Perine","RB","CIN"),P("Keenan Allen","WR","IND"),P("Alec Pierce (IR)","WR","IND")]},
 "mustafas-magnificent-team": {
   "starters": [P("Patrick Mahomes","QB","KC"),P("Saquon Barkley","RB","PHI"),P("Kendre Miller","RB","NO"),P("Germie Bernard","WR","PIT"),P("Makai Lemon","WR","PHI"),P("Isaiah Likely","TE","NYG"),P("Travis Kelce","TE","KC"),P("Vikings D/ST","D/ST","MIN"),P("Will Reichard","K","MIN")],
   "bench": [P("Omarion Hampton","RB","LAC"),P("DeVonta Smith","WR","PHI"),P("Ladd McConkey","WR","LAC"),P("DJ Moore","WR","BUF"),P("Marvin Harrison Jr.","WR","HOU"),P("Zach Charbonnet","RB","SEA"),P("J.J. McCarthy","QB","NYG"),P("Romeo Doubs (IR)","WR","NE")]},
 "team-mbk": {
   "starters": [P("Matthew Stafford","QB","LAR"),P("Jahmyr Gibbs","RB","DET"),P("Josh Jacobs","RB","GB"),P("Drake London","WR","ATL"),P("Tee Higgins","WR","CIN"),P("Sam LaPorta","TE","DET"),P("Quinshon Judkins","RB","CLE"),P("Seahawks D/ST","D/ST","SEA"),P("Matt Gay","K","LV")],
   "bench": [P("Dak Prescott","QB","DAL"),P("Rico Dowdle","RB","PIT"),P("Wan'Dale Robinson","WR","TEN"),P("Brian Robinson Jr.","RB","ATL"),P("KC Concepcion","WR","CLE"),P("Pat Freiermuth","TE","PIT"),P("Michael Mayer","TE","LV"),P("Tank Dell (IR)","WR","HOU")]},
 "gang-green": {
   "starters": [P("Bryce Young","QB","CAR"),P("Ashton Jeanty","RB","LV"),P("Chuba Hubbard","RB","CAR"),P("Garrett Wilson","WR","NYJ"),P("Tetairoa McMillan","WR","CAR"),P("Harold Fannin Jr.","TE","CLE"),P("Luther Burden III","WR","CHI"),P("Jets D/ST","D/ST","NYJ"),P("Jason Sanders","K","MIA")],
   "bench": [P("Stefon Diggs","WR","WSH"),P("Mike Washington Jr.","RB","LV"),P("Trevor Lawrence","QB","JAX"),P("Kenyon Sadiq","TE","NYJ"),P("Justice Hill","RB","BAL"),P("Jonathon Brooks (IR)","RB","CAR"),P("Dameon Pierce","RB","PHI"),P("Jordyn Tyson (IR)","WR","NO")]},
 "ivaafay": {
   "starters": [P("Caleb Williams","QB","CHI"),P("Bijan Robinson","RB","ATL"),P("Javonte Williams","RB","DAL"),P("George Pickens","WR","DAL"),P("DK Metcalf","WR","PIT"),P("Kyle Pitts Sr.","TE","ATL"),P("Jordan Mason","RB","MIN"),P("Bears D/ST","D/ST","CHI"),P("Jake Bates","K","DET")],
   "bench": [P("Jordan Addison","WR","MIN"),P("Alvin Kamara","RB","NO"),P("Khalil Shakir","WR","BUF"),P("Brenton Strange","TE","JAX"),P("Kimani Vidal","RB","LAC"),P("Jaylin Noel","WR","HOU"),P("Davante Adams (IR)","WR","LAR"),P("Jadarian Price (IR)","RB","SEA")]},
 "i-eat-ass": {
   "starters": [P("Kirk Cousins","QB","LV"),P("Christian McCaffrey","RB","SF"),P("Woody Marks","RB","HOU"),P("Chris Olave","WR","NO"),P("Carnell Tate","WR","TEN"),P("Dallas Goedert","TE","PHI"),P("Jameson Williams","WR","DET"),P("Steelers D/ST","D/ST","PIT"),P("Chris Boswell","K","PIT")],
   "bench": [P("Jeremiyah Love","RB","ARI"),P("Devaughn Vele","WR","NO"),P("T.J. Hockenson","TE","MIN"),P("David Montgomery","RB","HOU"),P("Mike Evans","WR","SF"),P("Jakobi Meyers","WR","JAX"),P("Tanner McKee","QB","PHI")]},
 "hnfnr-aint-busy": {
   "starters": [P("Joe Burrow","QB","CIN"),P("Derrick Henry","RB","BAL"),P("Tony Pollard","RB","TEN"),P("Jaxon Smith-Njigba","WR","SEA"),P("Zay Flowers","WR","BAL"),P("Brock Bowers","TE","LV"),P("Rhamondre Stevenson","RB","NE"),P("Browns D/ST","D/ST","CLE"),P("Dominic Zvada","K","NYG")],
   "bench": [P("Brian Thomas Jr.","WR","JAX"),P("Michael Wilson","WR","ARI"),P("Tyler Allgeier","RB","ARI"),P("Dalton Kincaid","TE","BUF"),P("Cameron Dicker","K","LAC"),P("Denzel Boston","WR","CLE"),P("Jacory Croskey-Merritt (IR)","RB","WSH"),P("Jonah Coleman (IR)","RB","DEN")]},
 "bazan": {
   "starters": [P("Kyler Murray","QB","MIN"),P("D'Andre Swift","RB","CHI"),P("Bam Knight","RB","ARI"),P("Malik Nabers","WR","NYG"),P("Jalen Coker","WR","CAR"),P("Tyler Higbee","TE","LAR"),P("A.J. Brown","WR","NE"),P("Panthers D/ST","D/ST","CAR"),P("Ryan Fitzgerald","K","CAR")],
   "bench": [P("James Cook III","RB","BUF"),P("Lamar Jackson","QB","BAL"),P("Kyle Monangai","RB","CHI"),P("Ray Davis","RB","BUF"),P("Adonai Mitchell","WR","NYJ"),P("Aaron Rodgers","QB","PIT"),P("Ja'Kobi Lane","WR","BAL"),P("Terrance Ferguson (IR)","TE","LAR")]},
 "deddybaba": {
   "starters": [P("Brock Purdy","QB","SF"),P("Ollie Gordon II","RB","MIA"),P("Bucky Irving","RB","TB"),P("Puka Nacua","WR","LAR"),P("Christian Kirk","WR","SF"),P("Tucker Kraft","TE","GB"),P("Roschon Johnson","RB","CHI"),P("Broncos D/ST","D/ST","DEN"),P("Ka'imi Fairbairn","K","HOU")],
   "bench": [P("Rashee Rice","WR","KC"),P("Bhayshul Tuten","RB","JAX"),P("RJ Harvey","RB","DEN"),P("Kenny Gainwell","RB","TB"),P("Josh Downs","WR","IND"),P("Tyjae Spears","RB","TEN"),P("Konata Mumpfield","WR","LAR")]},
 "team-noor": {
   "starters": [P("Jared Goff","QB","DET"),P("Kyren Williams","RB","LAR"),P("J.K. Dobbins","RB","DEN"),P("Ja'Marr Chase","WR","CIN"),P("Christian Watson","WR","GB"),P("George Kittle","TE","SF"),P("Aaron Jones Sr.","RB","MIN"),P("Patriots D/ST","D/ST","NE"),P("Tyler Loop","K","BAL")],
   "bench": [P("Breece Hall","RB","NYJ"),P("Jaylen Waddle","WR","DEN"),P("Mark Andrews","TE","BAL"),P("Tre Tucker","WR","LV"),P("Josh Allen","QB","BUF"),P("Keon Coleman","WR","BUF"),P("49ers D/ST","D/ST","SF"),P("Demarcus Robinson (IR)","WR","SF")]},
}
for tid, r in ROSTERS.items():
    slots = [{"slot": s, **p} for s, p in zip(S, r["starters"])]
    ROSTERS[tid] = {"starters": slots, "bench": r["bench"]}

# cumulative records + PF from all results through week 5
rec = {t: {"wins": 0, "losses": 0} for t in PRE_RANK}
pf = {t: 0.0 for t in PRE_RANK}
for wk in (1, 2, 3, 4, 5, 6, 7):
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
for m in schedule["weeks"]["8"]:
    nxt[m["away"]] = f'at {teams_meta[m["home"]]["teamName"]}'
    nxt[m["home"]] = f'vs {teams_meta[m["away"]]["teamName"]}'

out = {"week": 7, "publishedAt": "2026-10-27", "deck": editorial["deck"], "teams": []}
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

json.dump(out, open(f"{ROOT}/data/weeks/week-7.json", "w"), indent=2)
print("odds sum:", round(sum(t["titleOdds"] for t in out["teams"]), 1))
for t in out["teams"]:
    mv = PRE_RANK[t["teamId"]] - t["powerRank"]
    delta_sum = round(sum(m["delta"] for m in t["movementReasons"]), 1)
    print(f'#{t["powerRank"]:>2} {t["teamId"]:<28} {"↑" + str(mv) if mv > 0 else "↓" + str(-mv) if mv < 0 else "—":>3}  {t["powerScore"]:>5}  {t["titleOdds"]:>4}%  {t["record"]["wins"]}-{t["record"]["losses"]}  PF {t["pointsFor"]:>6}  Δreasons {delta_sum}')

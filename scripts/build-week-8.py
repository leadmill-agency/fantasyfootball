#!/usr/bin/env python3
"""Build data/weeks/week-8.json — the eighth in-season power snapshot.

Board: Version B formula (results = 20% win% + 40% all-play% + 40% scoring vs
league average; blend 70/30 with structure) plus Rameel's calls on 2026-11-03:
DEDDYBABA to 2nd (formula 5th), Chief 3rd over MBK 4th (formula had them
flipped), Noor 5th, Bazan 9th over I Eat Ass 10th (formula had them flipped).
Rosters: Week 8 lineups as played, from the ESPN box scores (final, 2026-11-03).
"""
import json, math, os

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
grades = {t["teamId"]: t["grade"] for t in json.load(open(f"{ROOT}/data/draft-grades.json"))["teams"]}
teams_meta = {t["teamId"]: t for t in json.load(open(f"{ROOT}/data/teams.json"))["teams"]}
editorial = json.load(open(f"{ROOT}/scripts/editorial-week-8.json"))
schedule = json.load(open(f"{ROOT}/data/schedule.json"))

PRE_RANK = {"hnfnr-aint-busy": 1, "team-noor": 2, "chief-sheikh": 3, "deddybaba": 4, "team-mbk": 5,
            "bizzy": 6, "rambam": 7, "gang-green": 8, "i-eat-ass": 9, "bazan": 10,
            "ivaafay": 11, "mustafas-magnificent-team": 12}

# rank, teamId, powerScore, tier, ceilingRank
BOARD = [
    (1, "hnfnr-aint-busy", 91.0, "Favorite", 1),
    (2, "deddybaba", 86.2, "Favorite", 5),
    (3, "chief-sheikh", 85.0, "Contender", 4),
    (4, "team-mbk", 84.2, "Contender", 3),
    (5, "team-noor", 82.6, "Contender", 2),
    (6, "bizzy", 77.6, "Playoff-caliber", 7),
    (7, "rambam", 74.8, "Playoff-caliber", 6),
    (8, "gang-green", 74.0, "Playoff-caliber", 8),
    (9, "bazan", 70.6, "Playoff-caliber", 11),
    (10, "i-eat-ass", 69.8, "Fringe contender", 12),
    (11, "ivaafay", 66.8, "Fringe contender", 9),
    (12, "mustafas-magnificent-team", 64.6, "Fragile", 10),
]

MOVEMENT = {
  "hnfnr-aint-busy": [(1.4, "139.68; 7-1, 65-23 all-play; Burrow 39.48"), (-0.6, "Flowers 0.0, Myers 2.0; Pollard on bye next")],
  "deddybaba": [(2.4, "145.86, the weekly high; five straight wins, 6-2"), (1.6, "Rice back (14.8), Tuten 28.9; ledger +58.28 over Noor"), (-0.6, "42-46 all-play; Luckbox Index +2.18")],
  "chief-sheikh": [(1.4, "119.32, beat Bizzy; 5-3, 55-33 all-play"), (-1.0, "Washington 3.1, Bengals D/ST 2.0; Bourne to IR")],
  "team-mbk": [(2.0, "125.1, two straight wins; Higgins 32.5"), (1.2, "55-33 all-play; 906.82 points, second"), (-0.6, "Judkins 5.9, London 1.3")],
  "team-noor": [(-1.8, "97.76, lost to Bazaan with Tucker 0.0 in the flex"), (-1.0, "3-5; Luckbox Index −1.73, the worst on record")],
  "bizzy": [(-1.4, "113.36 and lost by 5.96; Emmett Johnson 22.8 on the bench"), (1.0, "Maye 22.46, Douglas 15.1; 859.04 points, fifth")],
  "rambam": [(-2.4, "69.98 with Daniels back; Wilson 0.0, Taylor 4.7"), (0.2, "Won anyway; 4-4")],
  "gang-green": [(1.0, "119.4; Hubbard 21.4, Fannin 18.4"), (-1.6, "Third straight loss; 38-50 all-play")],
  "bazan": [(1.8, "105.3 and a win with 0.0 from the quarterback; Mitchell 23.7"), (-0.6, "Lamar to IR (thumb); Kyler is the quarterback")],
  "i-eat-ass": [(-1.8, "104.18, lost by 41 with the entire bench on bye"), (-0.6, "977.78 points allowed, most in the league")],
  "ivaafay": [(-1.8, "54.08, the season low; 2-6, four straight losses")],
  "mustafas-magnificent-team": [(0.6, "Mahomes 25.44; Moore back with 14.6"), (-1.2, "Reichard 0.0; 22-66 all-play, fewest points")],
}

STOCK = {
  "hnfnr-aint-busy": ("Joe Burrow", "Zay Flowers"),
  "deddybaba": ("Bhayshul Tuten", "Jacoby Brissett"),
  "chief-sheikh": ("Braelon Allen", "Parker Washington"),
  "team-mbk": ("Tee Higgins", "Drake London"),
  "team-noor": ("Josh Allen", "Tre Tucker"),
  "bizzy": ("DeMario Douglas", "Kenneth Walker III"),
  "rambam": ("Matthew Golden", "Emanuel Wilson"),
  "gang-green": ("Chuba Hubbard", "Ashton Jeanty"),
  "bazan": ("Adonai Mitchell", "Lamar Jackson"),
  "i-eat-ass": ("Kirk Cousins", "Jeremiyah Love"),
  "ivaafay": ("Bears D/ST", "DK Metcalf"),
  "mustafas-magnificent-team": ("Patrick Mahomes", "Will Reichard"),
}

DEVELOPMENT = {
  "hnfnr-aint-busy": "139.68 with a 116.8-point bench; Burrow 39.48. 7-1, two games clear.",
  "deddybaba": "145.86, the weekly high, with Brissett (3.46) at QB for Purdy's bye. Five straight.",
  "chief-sheikh": "Beat Nabil by 5.96 after Nabil conceded at 3:54 PM; \"8% to 48%.\"",
  "team-mbk": "125.1; Higgins 32.5 against Mustafa again. Judkins ledger flipped to +1.60.",
  "team-noor": "Lost to a team with 0.0 at QB; Tucker 0.0 in the flex, Waddle 13.4 on the bench.",
  "bizzy": "113.36 and lost; Emmett Johnson 22.8 on the bench. Conceded at 3:54 PM.",
  "rambam": "69.98, the lowest winning score of the season; Wilson 0.0, Taylor 4.7.",
  "gang-green": "119.4 and a third straight loss, to Arfan. \"Bro, I ran out.\"",
  "bazan": "Lamar hurt on the first snap (0.0), conceded at 12:36 PM, won anyway; Mitchell 23.7.",
  "i-eat-ass": "Entire bench on bye (0.0); lost by 41 to the weekly high. Ledger flipped to MBK.",
  "ivaafay": "54.08, the season low; Metcalf 0.9, Pitts 1.6, Mason 2.0. Four straight losses.",
  "mustafas-magnificent-team": "Mahomes 25.44 in a 40-point loss; Reichard 0.0. \"Only I can call myself a luckbox.\"",
}

S = ["QB", "RB", "RB", "WR", "WR", "TE", "FLEX", "D/ST", "K"]
def P(name, pos, nfl): return {"player": name, "position": pos, "nflTeam": nfl}
ROSTERS = {
 "rambam": {
   "starters": [P("Jayden Daniels","QB","WSH"),P("Emanuel Wilson","RB","SEA"),P("Jonathan Taylor","RB","IND"),P("Matthew Golden","WR","GB"),P("Ryan Flournoy","WR","DAL"),P("Tyler Warren","TE","IND"),P("Hunter Henry","TE","NE"),P("Packers D/ST","D/ST","GB"),P("Spencer Shrader","K","IND")],
   "bench": [P("Emeka Egbuka","WR","TB"),P("Rome Odunze","WR","CHI"),P("Xavier Worthy","WR","KC"),P("Kaelon Black","RB","SF"),P("C.J. Stroud","QB","HOU"),P("TreVeyon Henderson","RB","NE"),P("Seth McGowan","RB","IND"),P("Travis Etienne Jr. (IR)","RB","NO")]},
 "ivaafay": {
   "starters": [P("Caleb Williams","QB","CHI"),P("Bijan Robinson","RB","ATL"),P("Javonte Williams","RB","DAL"),P("George Pickens","WR","DAL"),P("DK Metcalf","WR","PIT"),P("Kyle Pitts Sr.","TE","ATL"),P("Jordan Mason","RB","MIN"),P("Bears D/ST","D/ST","CHI"),P("Jake Bates","K","DET")],
   "bench": [P("Jordan Addison","WR","MIN"),P("Alvin Kamara","RB","NO"),P("Khalil Shakir","WR","BUF"),P("Brenton Strange","TE","JAX"),P("Kimani Vidal","RB","LAC"),P("Courtland Sutton","WR","DEN"),P("Davante Adams (IR)","WR","LAR"),P("Jadarian Price (IR)","RB","SEA")]},
 "chief-sheikh": {
   "starters": [P("Jordan Love","QB","GB"),P("Jaylen Warren","RB","PIT"),P("Braelon Allen","RB","NYJ"),P("Amon-Ra St. Brown","WR","DET"),P("Justin Jefferson","WR","MIN"),P("Trey McBride","TE","ARI"),P("Parker Washington","WR","JAX"),P("Bengals D/ST","D/ST","CIN"),P("Brandon Aubrey","K","DAL")],
   "bench": [P("Cam Skattebo","RB","NYG"),P("Blake Corum","RB","LAR"),P("Texans D/ST","D/ST","HOU"),P("Omar Cooper Jr.","WR","NYJ"),P("Travis Hunter","WR","JAX"),P("Dylan Sampson","RB","CLE"),P("Kendrick Bourne (IR)","WR","ARI")]},
 "bizzy": {
   "starters": [P("Drake Maye","QB","NE"),P("Kenneth Walker III","RB","KC"),P("Chase Brown","RB","CIN"),P("CeeDee Lamb","WR","DAL"),P("DeMario Douglas","WR","NE"),P("Colston Loveland","TE","CHI"),P("Rachaad White","RB","WSH"),P("Rams D/ST","D/ST","LAR"),P("Chase McLaughlin","K","TB")],
   "bench": [P("Nico Collins","WR","HOU"),P("Deebo Samuel Sr.","WR","SF"),P("Tyler Shough","QB","NO"),P("Malik Washington","WR","MIA"),P("Emmett Johnson","RB","KC"),P("Samaje Perine","RB","CIN"),P("Keenan Allen","WR","IND"),P("Alec Pierce (IR)","WR","IND")]},
 "mustafas-magnificent-team": {
   "starters": [P("Patrick Mahomes","QB","KC"),P("Saquon Barkley","RB","PHI"),P("Zach Charbonnet","RB","SEA"),P("Germie Bernard","WR","PIT"),P("Makai Lemon","WR","PHI"),P("Travis Kelce","TE","KC"),P("DJ Moore","WR","BUF"),P("Vikings D/ST","D/ST","MIN"),P("Will Reichard","K","MIN")],
   "bench": [P("Omarion Hampton","RB","LAC"),P("DeVonta Smith","WR","PHI"),P("Ladd McConkey","WR","LAC"),P("Marvin Harrison Jr.","WR","HOU"),P("Isaiah Likely","TE","NYG"),P("Geno Smith","QB","NYJ"),P("Jaydon Blue","RB","PHI"),P("Romeo Doubs (IR)","WR","NE")]},
 "team-mbk": {
   "starters": [P("Dak Prescott","QB","DAL"),P("Jahmyr Gibbs","RB","DET"),P("Josh Jacobs","RB","GB"),P("Drake London","WR","ATL"),P("Tee Higgins","WR","CIN"),P("Pat Freiermuth","TE","PIT"),P("Quinshon Judkins","RB","CLE"),P("Seahawks D/ST","D/ST","SEA"),P("Matt Gay","K","LV")],
   "bench": [P("Sam LaPorta","TE","DET"),P("Rico Dowdle","RB","PIT"),P("Wan'Dale Robinson","WR","TEN"),P("Brian Robinson Jr.","RB","ATL"),P("Matthew Stafford","QB","LAR"),P("KC Concepcion","WR","CLE"),P("Michael Mayer","TE","LV"),P("Tank Dell (IR)","WR","HOU")]},
 "gang-green": {
   "starters": [P("Trevor Lawrence","QB","JAX"),P("Ashton Jeanty","RB","LV"),P("Chuba Hubbard","RB","CAR"),P("Garrett Wilson","WR","NYJ"),P("Tetairoa McMillan","WR","CAR"),P("Harold Fannin Jr.","TE","CLE"),P("Stefon Diggs","WR","WSH"),P("Commanders D/ST","D/ST","WSH"),P("Cam Little","K","JAX")],
   "bench": [P("Luther Burden III","WR","CHI"),P("Mike Washington Jr.","RB","LV"),P("Bryce Young","QB","CAR"),P("Justice Hill","RB","BAL"),P("Elijah Mitchell","RB","PHI"),P("Jonathon Brooks (IR)","RB","CAR"),P("Dameon Pierce (IR)","RB","PHI"),P("Jordyn Tyson (IR)","WR","NO")]},
 "hnfnr-aint-busy": {
   "starters": [P("Joe Burrow","QB","CIN"),P("Derrick Henry","RB","BAL"),P("Tony Pollard","RB","TEN"),P("Jaxon Smith-Njigba","WR","SEA"),P("Zay Flowers","WR","BAL"),P("Brock Bowers","TE","LV"),P("Rhamondre Stevenson","RB","NE"),P("Browns D/ST","D/ST","CLE"),P("Jason Myers","K","SEA")],
   "bench": [P("Brian Thomas Jr.","WR","JAX"),P("Michael Wilson","WR","ARI"),P("Tyler Allgeier","RB","ARI"),P("Dalton Kincaid","TE","BUF"),P("Cameron Dicker","K","LAC"),P("Denzel Boston","WR","CLE"),P("Jonah Coleman","RB","DEN"),P("Jacory Croskey-Merritt (IR)","RB","WSH")]},
 "i-eat-ass": {
   "starters": [P("Kirk Cousins","QB","LV"),P("Jeremiyah Love","RB","ARI"),P("Chris Rodriguez Jr.","RB","JAX"),P("Jameson Williams","WR","DET"),P("Jakobi Meyers","WR","JAX"),P("T.J. Hockenson","TE","MIN"),P("Dallas Goedert","TE","PHI"),P("Steelers D/ST","D/ST","PIT"),P("Chris Boswell","K","PIT")],
   "bench": [P("Christian McCaffrey","RB","SF"),P("Chris Olave","WR","NO"),P("Woody Marks","RB","HOU"),P("Devaughn Vele","WR","NO"),P("Carnell Tate","WR","TEN"),P("David Montgomery","RB","HOU"),P("Mike Evans","WR","SF")]},
 "deddybaba": {
   "starters": [P("Jacoby Brissett","QB","ARI"),P("Ollie Gordon II","RB","MIA"),P("Bucky Irving","RB","TB"),P("Puka Nacua","WR","LAR"),P("Rashee Rice","WR","KC"),P("Tucker Kraft","TE","GB"),P("Bhayshul Tuten","RB","JAX"),P("Jaguars D/ST","D/ST","JAX"),P("Tyler Bass","K","BUF")],
   "bench": [P("Kenny Gainwell","RB","TB"),P("Josh Downs","WR","IND"),P("Broncos D/ST","D/ST","DEN"),P("Ka'imi Fairbairn","K","HOU"),P("Brock Purdy","QB","SF"),P("Antonio Williams","WR","WSH"),P("RJ Harvey (IR)","RB","DEN")]},
 "bazan": {
   "starters": [P("Lamar Jackson","QB","BAL"),P("James Cook III","RB","BUF"),P("D'Andre Swift","RB","CHI"),P("Jalen Coker","WR","CAR"),P("Ja'Kobi Lane","WR","BAL"),P("Chig Okonkwo","TE","WSH"),P("Adonai Mitchell","WR","NYJ"),P("Buccaneers D/ST","D/ST","TB"),P("Chad Ryland","K","ARI")],
   "bench": [P("A.J. Brown","WR","NE"),P("Malik Nabers","WR","NYG"),P("Kyle Monangai","RB","CHI"),P("Ray Davis","RB","BUF"),P("Bam Knight","RB","ARI"),P("Kyler Murray","QB","MIN"),P("Corey Kiner","RB","NE"),P("Terrance Ferguson (IR)","TE","LAR")]},
 "team-noor": {
   "starters": [P("Josh Allen","QB","BUF"),P("Kyren Williams","RB","LAR"),P("Aaron Jones Sr.","RB","MIN"),P("Ja'Marr Chase","WR","CIN"),P("Christian Watson","WR","GB"),P("Mark Andrews","TE","BAL"),P("Tre Tucker","WR","LV"),P("Patriots D/ST","D/ST","NE"),P("Tyler Loop","K","BAL")],
   "bench": [P("Breece Hall","RB","NYJ"),P("Jaylen Waddle","WR","DEN"),P("George Kittle","TE","SF"),P("J.K. Dobbins","RB","DEN"),P("Jared Goff","QB","DET"),P("Keon Coleman","WR","BUF"),P("49ers D/ST","D/ST","SF"),P("Demarcus Robinson (IR)","WR","SF")]},
}
ARCHETYPE = {"team-noor": "The Complete Team", "bizzy": "The RB Machine", "team-mbk": "The Floor Monster",
             "bazan": "The Nuclear Core", "rambam": "The Venture Portfolio",
             "mustafas-magnificent-team": "The Deep Bench", "hnfnr-aint-busy": "The Stars Up Top",
             "i-eat-ass": "The Volatility Bet", "chief-sheikh": "The WR Superteam",
             "gang-green": "The Moonshot", "ivaafay": "The Bijan Build", "deddybaba": "The No-RB Experiment"}

for tid, r in ROSTERS.items():
    slots = [{"slot": s, **p} for s, p in zip(S, r["starters"])]
    ROSTERS[tid] = {"starters": slots, "bench": r["bench"]}

# cumulative records + PF from all results through week 5
rec = {t: {"wins": 0, "losses": 0} for t in PRE_RANK}
pf = {t: 0.0 for t in PRE_RANK}
for wk in (1, 2, 3, 4, 5, 6, 7, 8):
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
for m in schedule["weeks"]["9"]:
    nxt[m["away"]] = f'at {teams_meta[m["home"]]["teamName"]}'
    nxt[m["home"]] = f'vs {teams_meta[m["away"]]["teamName"]}'

out = {"week": 8, "publishedAt": "2026-11-03", "deck": editorial["deck"], "teams": []}
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

json.dump(out, open(f"{ROOT}/data/weeks/week-8.json", "w"), indent=2)
print("odds sum:", round(sum(t["titleOdds"] for t in out["teams"]), 1))
for t in out["teams"]:
    mv = PRE_RANK[t["teamId"]] - t["powerRank"]
    delta_sum = round(sum(m["delta"] for m in t["movementReasons"]), 1)
    print(f'#{t["powerRank"]:>2} {t["teamId"]:<28} {"↑" + str(mv) if mv > 0 else "↓" + str(-mv) if mv < 0 else "—":>3}  {t["powerScore"]:>5}  {t["titleOdds"]:>4}%  {t["record"]["wins"]}-{t["record"]["losses"]}  PF {t["pointsFor"]:>6}  Δreasons {delta_sum}')

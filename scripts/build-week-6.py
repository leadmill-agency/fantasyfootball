#!/usr/bin/env python3
"""Build data/weeks/week-6.json — the sixth in-season power snapshot.

Board: Version B formula (results = 20% win% + 40% all-play% + 40% scoring vs
league average; blend 70/30 with structure) plus three desk calls on
2026-10-20 agreed with Rameel: Team Noor at No. 1 per the formula (3-3, most
points, best all-play); DEDDYBABA 5th and Gang Green 6th (both 4-2; formula had
7th and 8th); RN 11th over I Eat Ass (formula had them flipped).
Rosters: Week 6 lineups as played, from the ESPN box scores (final, 2026-10-20).
"""
import json, math, os

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
grades = {t["teamId"]: t["grade"] for t in json.load(open(f"{ROOT}/data/draft-grades.json"))["teams"]}
teams_meta = {t["teamId"]: t for t in json.load(open(f"{ROOT}/data/teams.json"))["teams"]}
editorial = json.load(open(f"{ROOT}/scripts/editorial-week-6.json"))
schedule = json.load(open(f"{ROOT}/data/schedule.json"))

PRE_RANK = {"hnfnr-aint-busy": 1, "team-noor": 2, "gang-green": 3, "team-mbk": 4, "chief-sheikh": 5,
            "rambam": 6, "ivaafay": 7, "bizzy": 8, "deddybaba": 9, "bazan": 10,
            "mustafas-magnificent-team": 11, "i-eat-ass": 12}

# rank, teamId, powerScore, tier, ceilingRank
BOARD = [
    (1, "team-noor", 88.6, "Favorite", 1),
    (2, "hnfnr-aint-busy", 87.4, "Favorite", 2),
    (3, "chief-sheikh", 83.8, "Contender", 3),
    (4, "rambam", 82.4, "Contender", 4),
    (5, "deddybaba", 79.6, "Contender", 7),
    (6, "gang-green", 78.4, "Playoff-caliber", 8),
    (7, "team-mbk", 77.2, "Playoff-caliber", 5),
    (8, "bizzy", 74.8, "Playoff-caliber", 6),
    (9, "bazan", 72.6, "Playoff-caliber", 9),
    (10, "ivaafay", 71.4, "Fringe contender", 10),
    (11, "mustafas-magnificent-team", 67.0, "Fringe contender", 11),
    (12, "i-eat-ass", 64.8, "Fragile", 12),
]

ARCHETYPE = {"team-noor": "The Complete Team", "bizzy": "The RB Machine", "team-mbk": "The Floor Monster",
             "bazan": "The Nuclear Core", "rambam": "The Venture Portfolio",
             "mustafas-magnificent-team": "The Deep Bench", "hnfnr-aint-busy": "The Stars Up Top",
             "i-eat-ass": "The Volatility Bet", "chief-sheikh": "The WR Superteam",
             "gang-green": "The Moonshot", "ivaafay": "The Bijan Build", "deddybaba": "The No-RB Experiment"}

MOVEMENT = {
  "team-noor": [(1.6, "Leads the league in points (736.78) and all-play (45-21)"), (1.0, "108.0, streak over; Dobbins started, Tucker 24.2")],
  "hnfnr-aint-busy": [(-2.4, "76.28 with Winston at quarterback; first loss"), (0.4, "Still 5-1, 44-22 all-play; Burrow back Sunday")],
  "chief-sheikh": [(-1.0, "79.84 with three starters on bye, Skattebo 0.0"), (3.2, "Kyler, Jefferson and St. Brown all return; 39-27 all-play, third")],
  "rambam": [(2.4, "Third straight win, 3-3"), (1.6, "644.12 points, third in the league"), (0.8, "Stroud's 22.98 ready for Daniels' bye")],
  "deddybaba": [(3.4, "4-2, second in the standings; beat the unbeaten team"), (2.4, "Tuten 22.7, Purdy 17.36; trade ledger +28.32"), (1.4, "Second-lowest points against"), (-1.0, "McLaurin carted off, likely done for the season")],
  "gang-green": [(-2.4, "79.64, lost to RN; Lawrence 27.34 and Burden 13.5 on the bench"), (-1.2, "28-38 all-play, tenth in points"), (-0.6, "Grupe's torn ACL")],
  "team-mbk": [(-3.0, "66.68, the week's low; three straight losses, 2-4"), (-1.4, "735.32 points allowed, most in the league"), (-0.6, "Jacobs eligible, status undetermined")],
  "bizzy": [(-1.6, "111.7 and lost by 1.9; Loveland 15.5 and Shough 26.96 on the bench"), (1.4, "Walker 26.9, Maye 23.8, Lamb back; 646.04 points, fourth")],
  "bazan": [(2.2, "116.4, the weekly high"), (1.4, "Lamar targeted for Week 7; Cook, Swift and Nabers all over 21"), (-0.6, "Cook on bye Sunday; 30 roster moves")],
  "ivaafay": [(-2.6, "Davante Adams out six to ten weeks"), (-1.4, "Second straight loss, 2-4"), (-0.8, "Jaguars D/ST −2.0, a second straight negative defense")],
  "mustafas-magnificent-team": [(1.8, "Two straight wins, 3-3, with Barkley and Moore out"), (-1.0, "19-47 all-play, fewest points; Doubs to IR")],
  "i-eat-ass": [(1.8, "110.82, first win since Week 1; McCaffrey 26.2"), (-1.6, "Hurts out for the season"), (-0.8, "Evans' Achilles; 723.8 points allowed")],
}

STOCK = {
  "team-noor": ("Tre Tucker", "Kyren Williams"),
  "hnfnr-aint-busy": ("Jaxon Smith-Njigba", "Derrick Henry"),
  "chief-sheikh": ("Jordan Love", "Cam Skattebo"),
  "rambam": ("Jonathan Taylor", "Giants D/ST"),
  "deddybaba": ("Bhayshul Tuten", "Terry McLaurin"),
  "gang-green": ("Chuba Hubbard", "MarShawn Lloyd"),
  "team-mbk": ("Matthew Stafford", "Brian Robinson Jr."),
  "bizzy": ("Kenneth Walker III", "Tyler Higbee"),
  "bazan": ("Malik Nabers", "Nick Folk"),
  "ivaafay": ("Kyle Pitts Sr.", "Davante Adams"),
  "mustafas-magnificent-team": ("Isaiah Likely", "Patrick Mahomes"),
  "i-eat-ass": ("Christian McCaffrey", "Jalen Hurts"),
}

DEVELOPMENT = {
  "team-noor": "No. 1 at 3-3: most points in the league (736.78) and the best all-play record (45-21).",
  "hnfnr-aint-busy": "First loss, 76.28, with Jameis Winston covering Burrow's bye; Henry 4.5.",
  "chief-sheikh": "Lost 110.82-79.84 with Kyler, Jefferson and St. Brown on bye; all three return Sunday.",
  "rambam": "Beat the trade partner by 1.9; Hunter Henry, added Sunday morning, scored 12.8.",
  "deddybaba": "Beat the 5-0 team; Tuten 22.7. McLaurin was carted off Monday night.",
  "gang-green": "Lost to RN with Lawrence's 27.34 on the bench and Lloyd's 1.0 in the flex.",
  "team-mbk": "66.68, the week's low, with three starters on bye and four waiver fill-ins.",
  "bizzy": "111.7 and lost by 1.9; Loveland 15.5 sat behind Higbee's 2.2.",
  "bazan": "116.4, the weekly high; Huntley started over Lamar and Rodgers. 30 moves.",
  "ivaafay": "Jaguars D/ST scored −2.0 a week after the Bears did; Adams out 6-10 weeks.",
  "mustafas-magnificent-team": "Second straight win with Barkley and Moore out; Likely 20.9, Bernard 20.2 on the bench.",
  "i-eat-ass": "First win since Week 1 (110.82); Hurts to IR for the season, Evans hurt his Achilles.",
}

S = ["QB", "RB", "RB", "WR", "WR", "TE", "FLEX", "D/ST", "K"]
def P(name, pos, nfl): return {"player": name, "position": pos, "nflTeam": nfl}
ROSTERS = {
 "rambam": {
   "starters": [P("Jayden Daniels","QB","WSH"),P("Emanuel Wilson","RB","SEA"),P("Jonathan Taylor","RB","IND"),P("Matthew Golden","WR","GB"),P("Xavier Worthy","WR","KC"),P("Hunter Henry","TE","NE"),P("Emeka Egbuka","WR","TB"),P("Giants D/ST","D/ST","NYG"),P("Spencer Shrader","K","IND")],
   "bench": [P("Tyler Warren","TE","IND"),P("Rome Odunze","WR","CHI"),P("Jonathon Brooks (IR)","RB","CAR"),P("Kaelon Black","RB","SF"),P("C.J. Stroud","QB","HOU"),P("TreVeyon Henderson","RB","NE"),P("Dontayvion Wicks","WR","PHI"),P("Travis Etienne Jr. (IR)","RB","NO")]},
 "bizzy": {
   "starters": [P("Drake Maye","QB","NE"),P("Kenneth Walker III","RB","KC"),P("Rachaad White","RB","WSH"),P("Nico Collins","WR","HOU"),P("CeeDee Lamb","WR","DAL"),P("Tyler Higbee","TE","LAR"),P("Keenan Allen","WR","IND"),P("Rams D/ST","D/ST","LAR"),P("Cam Little","K","JAX")],
   "bench": [P("Colston Loveland","TE","CHI"),P("Deebo Samuel Sr.","WR","SF"),P("Tyler Shough","QB","NO"),P("Malik Washington","WR","MIA"),P("Emmett Johnson","RB","KC"),P("Chase Brown","RB","CIN"),P("Samaje Perine","RB","CIN"),P("Alec Pierce (IR)","WR","IND")]},
 "gang-green": {
   "starters": [P("Bryce Young","QB","CAR"),P("Ashton Jeanty","RB","LV"),P("Chuba Hubbard","RB","CAR"),P("Garrett Wilson","WR","NYJ"),P("Tetairoa McMillan","WR","CAR"),P("Harold Fannin Jr.","TE","CLE"),P("MarShawn Lloyd","RB","GB"),P("Jets D/ST","D/ST","NYJ"),P("Blake Grupe","K","LAR")],
   "bench": [P("Luther Burden III","WR","CHI"),P("Stefon Diggs","WR","WSH"),P("Mike Washington Jr.","RB","LV"),P("Keaton Mitchell","RB","LAC"),P("Trevor Lawrence","QB","JAX"),P("Kenyon Sadiq","TE","NYJ"),P("Pierre Strong Jr.","RB","GB"),P("Jordyn Tyson (IR)","WR","NO")]},
 "mustafas-magnificent-team": {
   "starters": [P("Patrick Mahomes","QB","KC"),P("Omarion Hampton","RB","LAC"),P("Kendre Miller","RB","NO"),P("DeVonta Smith","WR","PHI"),P("Ladd McConkey","WR","LAC"),P("Isaiah Likely","TE","NYG"),P("Travis Kelce","TE","KC"),P("Colts D/ST","D/ST","IND"),P("Jason Myers","K","SEA")],
   "bench": [P("Saquon Barkley","RB","PHI"),P("DJ Moore","WR","BUF"),P("Marvin Harrison Jr.","WR","HOU"),P("Vikings D/ST","D/ST","MIN"),P("Will Reichard","K","MIN"),P("Romeo Doubs","WR","NE"),P("Germie Bernard","WR","PIT"),P("Zach Charbonnet (IR)","RB","SEA")]},
 "i-eat-ass": {
   "starters": [P("Kirk Cousins","QB","LV"),P("Christian McCaffrey","RB","SF"),P("Woody Marks","RB","HOU"),P("Chris Olave","WR","NO"),P("Mike Evans","WR","SF"),P("Dallas Goedert","TE","PHI"),P("Devaughn Vele","WR","NO"),P("Steelers D/ST","D/ST","PIT"),P("Dominic Zvada","K","NYG")],
   "bench": [P("Jeremiyah Love","RB","ARI"),P("Jameson Williams","WR","DET"),P("T.J. Hockenson","TE","MIN"),P("Carnell Tate","WR","TEN"),P("David Montgomery","RB","HOU"),P("Jakobi Meyers","WR","JAX"),P("Tanner McKee","QB","PHI"),P("Jalen Hurts (IR)","QB","PHI")]},
 "chief-sheikh": {
   "starters": [P("Jordan Love","QB","GB"),P("Jaylen Warren","RB","PIT"),P("Braelon Allen","RB","NYJ"),P("Parker Washington","WR","JAX"),P("Kendrick Bourne","WR","ARI"),P("Trey McBride","TE","ARI"),P("Cam Skattebo","RB","NYG"),P("Chiefs D/ST","D/ST","KC"),P("Brandon Aubrey","K","DAL")],
   "bench": [P("Amon-Ra St. Brown","WR","DET"),P("Justin Jefferson","WR","MIN"),P("Blake Corum","RB","LAR"),P("Texans D/ST","D/ST","HOU"),P("Jake Ferguson","TE","DAL"),P("Jaleel McLaughlin","RB","CLE"),P("Kyler Murray","QB","MIN")]},
 "bazan": {
   "starters": [P("Tyler Huntley","QB","BAL"),P("James Cook III","RB","BUF"),P("D'Andre Swift","RB","CHI"),P("Malik Nabers","WR","NYG"),P("Jalen Coker","WR","CAR"),P("Juwan Johnson","TE","NO"),P("Dameon Pierce","RB","PHI"),P("Ravens D/ST","D/ST","BAL"),P("Nick Folk","K","ATL")],
   "bench": [P("A.J. Brown","WR","NE"),P("Lamar Jackson","QB","BAL"),P("Kyle Monangai","RB","CHI"),P("Ray Davis","RB","BUF"),P("Adonai Mitchell","WR","NYJ"),P("Aaron Rodgers","QB","PIT"),P("Seth McGowan","RB","IND"),P("Ja'Kobi Lane (IR)","WR","BAL")]},
 "team-mbk": {
   "starters": [P("Matthew Stafford","QB","LAR"),P("Brian Robinson Jr.","RB","ATL"),P("Audric Estime","RB","CLE"),P("Drake London","WR","ATL"),P("Wan'Dale Robinson","WR","TEN"),P("Pat Freiermuth","TE","PIT"),P("KC Concepcion","WR","CLE"),P("Seahawks D/ST","D/ST","SEA"),P("Matt Gay","K","LV")],
   "bench": [P("Jahmyr Gibbs","RB","DET"),P("Tee Higgins","WR","CIN"),P("Sam LaPorta","TE","DET"),P("Dak Prescott","QB","DAL"),P("Rico Dowdle","RB","PIT"),P("Quinshon Judkins","RB","CLE"),P("Tank Dell (IR)","WR","HOU"),P("Josh Jacobs (IR)","RB","GB")]},
 "team-noor": {
   "starters": [P("Josh Allen","QB","BUF"),P("Kyren Williams","RB","LAR"),P("J.K. Dobbins","RB","DEN"),P("Christian Watson","WR","GB"),P("Keon Coleman","WR","BUF"),P("George Kittle","TE","SF"),P("Tre Tucker","WR","LV"),P("Patriots D/ST","D/ST","NE"),P("Tyler Loop","K","BAL")],
   "bench": [P("Ja'Marr Chase","WR","CIN"),P("Breece Hall","RB","NYJ"),P("Jaylen Waddle","WR","DEN"),P("Aaron Jones Sr.","RB","MIN"),P("Mark Andrews","TE","BAL"),P("Jared Goff","QB","DET"),P("49ers D/ST","D/ST","SF"),P("Demarcus Robinson (IR)","WR","SF")]},
 "ivaafay": {
   "starters": [P("Caleb Williams","QB","CHI"),P("Bijan Robinson","RB","ATL"),P("Javonte Williams","RB","DAL"),P("George Pickens","WR","DAL"),P("Davante Adams","WR","LAR"),P("Kyle Pitts Sr.","TE","ATL"),P("DK Metcalf","WR","PIT"),P("Jaguars D/ST","D/ST","JAX"),P("Harrison Butker","K","KC")],
   "bench": [P("Jordan Addison","WR","MIN"),P("Alvin Kamara","RB","NO"),P("Khalil Shakir","WR","BUF"),P("Deshaun Watson","QB","CLE"),P("Brenton Strange","TE","JAX"),P("Kimani Vidal","RB","LAC"),P("Jadarian Price (IR)","RB","SEA"),P("Jordan Mason (IR)","RB","MIN")]},
 "deddybaba": {
   "starters": [P("Brock Purdy","QB","SF"),P("Bhayshul Tuten","RB","JAX"),P("Bucky Irving","RB","TB"),P("Puka Nacua","WR","LAR"),P("Terry McLaurin","WR","WSH"),P("Tucker Kraft","TE","GB"),P("RJ Harvey","RB","DEN"),P("Broncos D/ST","D/ST","DEN"),P("Ka'imi Fairbairn","K","HOU")],
   "bench": [P("Rashee Rice","WR","KC"),P("Kenny Gainwell","RB","TB"),P("Josh Downs","WR","IND"),P("Tyjae Spears","RB","TEN"),P("Ollie Gordon II","RB","MIA"),P("Tre' Harris","WR","LAC"),P("Roschon Johnson","RB","CHI"),P("Christian Kirk (IR)","WR","SF")]},
 "hnfnr-aint-busy": {
   "starters": [P("Jameis Winston","QB","NYG"),P("Derrick Henry","RB","BAL"),P("Tony Pollard","RB","TEN"),P("Jaxon Smith-Njigba","WR","SEA"),P("Zay Flowers","WR","BAL"),P("Brock Bowers","TE","LV"),P("Rhamondre Stevenson","RB","NE"),P("Browns D/ST","D/ST","CLE"),P("Cameron Dicker","K","LAC")],
   "bench": [P("Joe Burrow","QB","CIN"),P("Brian Thomas Jr.","WR","JAX"),P("Michael Wilson","WR","ARI"),P("Tyler Allgeier","RB","ARI"),P("Dalton Kincaid","TE","BUF"),P("Denzel Boston","WR","CLE"),P("Jacory Croskey-Merritt (IR)","RB","WSH"),P("Jonah Coleman (IR)","RB","DEN")]},
}
for tid, r in ROSTERS.items():
    slots = [{"slot": s, **p} for s, p in zip(S, r["starters"])]
    ROSTERS[tid] = {"starters": slots, "bench": r["bench"]}

# cumulative records + PF from all results through week 5
rec = {t: {"wins": 0, "losses": 0} for t in PRE_RANK}
pf = {t: 0.0 for t in PRE_RANK}
for wk in (1, 2, 3, 4, 5, 6):
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
for m in schedule["weeks"]["7"]:
    nxt[m["away"]] = f'at {teams_meta[m["home"]]["teamName"]}'
    nxt[m["home"]] = f'vs {teams_meta[m["away"]]["teamName"]}'

out = {"week": 6, "publishedAt": "2026-10-20", "deck": editorial["deck"], "teams": []}
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

json.dump(out, open(f"{ROOT}/data/weeks/week-6.json", "w"), indent=2)
print("odds sum:", round(sum(t["titleOdds"] for t in out["teams"]), 1))
for t in out["teams"]:
    mv = PRE_RANK[t["teamId"]] - t["powerRank"]
    delta_sum = round(sum(m["delta"] for m in t["movementReasons"]), 1)
    print(f'#{t["powerRank"]:>2} {t["teamId"]:<28} {"↑" + str(mv) if mv > 0 else "↓" + str(-mv) if mv < 0 else "—":>3}  {t["powerScore"]:>5}  {t["titleOdds"]:>4}%  {t["record"]["wins"]}-{t["record"]["losses"]}  PF {t["pointsFor"]:>6}  Δreasons {delta_sum}')

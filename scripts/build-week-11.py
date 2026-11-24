#!/usr/bin/env python3
"""Build data/weeks/week-11.json — the eleventh in-season power snapshot.

Board: Version B formula (results = 20% win% + 40% all-play% + 40% scoring vs
league average; blend 70/30 with structure). Rameel approved the recommended
order on 2026-11-24: DEDDYBABA 5th (formula 6th), Noor 7th (formula 5th), RN
8th and RamBam 9th (formula 11th and 10th), IEA 10th (formula 8th), IVaafay
11th, Bazan 12th.
Rosters: Week 11 lineups as played, from the ESPN box scores (final, 2026-11-24).
"""
import json, math, os

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
grades = {t["teamId"]: t["grade"] for t in json.load(open(f"{ROOT}/data/draft-grades.json"))["teams"]}
teams_meta = {t["teamId"]: t for t in json.load(open(f"{ROOT}/data/teams.json"))["teams"]}
editorial = json.load(open(f"{ROOT}/scripts/editorial-week-11.json"))
schedule = json.load(open(f"{ROOT}/data/schedule.json"))

PRE_RANK = {"hnfnr-aint-busy": 1, "chief-sheikh": 2, "deddybaba": 3, "bizzy": 4, "team-mbk": 5,
            "team-noor": 6, "gang-green": 7, "rambam": 8, "i-eat-ass": 9,
            "mustafas-magnificent-team": 10, "bazan": 11, "ivaafay": 12}

# rank, teamId, powerScore, tier, ceilingRank
BOARD = [
    (1, "hnfnr-aint-busy", 89.4, "Favorite", 1),
    (2, "chief-sheikh", 88.0, "Favorite", 2),
    (3, "bizzy", 85.4, "Contender", 5),
    (4, "team-mbk", 84.2, "Contender", 3),
    (5, "deddybaba", 81.6, "Contender", 9),
    (6, "gang-green", 79.0, "Playoff-caliber", 6),
    (7, "team-noor", 77.8, "Playoff-caliber", 4),
    (8, "mustafas-magnificent-team", 71.4, "Playoff-caliber", 8),
    (9, "rambam", 70.2, "Playoff-caliber", 7),
    (10, "i-eat-ass", 68.8, "Fringe contender", 10),
    (11, "ivaafay", 67.0, "Fringe contender", 11),
    (12, "bazan", 63.8, "Fragile", 12),
]

ARCHETYPE = {"team-noor": "The Complete Team", "bizzy": "The RB Machine", "team-mbk": "The Floor Monster",
             "bazan": "The Nuclear Core", "rambam": "The Venture Portfolio",
             "mustafas-magnificent-team": "The Deep Bench", "hnfnr-aint-busy": "The Stars Up Top",
             "i-eat-ass": "The Volatility Bet", "chief-sheikh": "The WR Superteam",
             "gang-green": "The Moonshot", "ivaafay": "The Bijan Build", "deddybaba": "The No-RB Experiment"}

MOVEMENT = {
  "hnfnr-aint-busy": [(-1.2, "113.9, lost by 0.38; started an inactive Bowers at 0.0"), (0.4, "Clinched a playoff spot; 1,316.5 points, first")],
  "chief-sheikh": [(1.4, "94.42, fifth straight win; clinched at 8-3"), (-1.0, "Skattebo 4.3, Warren 3.9; eighth-best score of the week")],
  "bizzy": [(1.6, "114.28, third straight win, by 0.38 over the No. 1 team"), (0.8, "Second in points and all-play; Lamb 24.7, Emmett Johnson 22.3"), (-0.6, "Maye in the IR slot; Shough 14.28")],
  "team-mbk": [(1.6, "107.6, beat Noor; Dak 35.9, Gibbs 25.8"), (-0.2, "Bengals D/ST 0.0; Jacobs had finger surgery")],
  "deddybaba": [(-1.6, "86.1, lost to the last-place team; two straight losses"), (-1.2, "Dropped Puka Nacua; 58-63 all-play")],
  "gang-green": [(2.2, "112.04, second straight win, 6-5"), (0.4, "Hubbard 26.0, Jeanty 25.4")],
  "team-noor": [(-2.0, "96.86, second straight loss; 4-7, ninth"), (-0.8, "Chase 5.6; Allen 12.16 with Goff's 20.36 on the bench")],
  "mustafas-magnificent-team": [(3.0, "118.36, the weekly high; second straight win"), (1.2, "5-6 and holding the eighth playoff spot")],
  "rambam": [(-4.4, "43.86, the lowest score of the season"), (-1.0, "Taylor 4.7; 49-72 all-play")],
  "i-eat-ass": [(-1.4, "Lost by 4.46 with Mendoza's 22.88 on the bench; 4-7"), (0.6, "113.9; Evans 19.9 and Montgomery 13.9 back")],
  "ivaafay": [(2.2, "93.74, beat DEDDYBABA to end a six-game losing streak")],
  "bazan": [(-1.6, "87.9, third straight loss; started Nix (11.5) over Ward (22.22)")],
}

STOCK = {
  "hnfnr-aint-busy": ("Jonah Coleman", "Brock Bowers"),
  "chief-sheikh": ("Texans D/ST", "Cam Skattebo"),
  "bizzy": ("CeeDee Lamb", "Chase Brown"),
  "team-mbk": ("Dak Prescott", "Tank Dell"),
  "deddybaba": ("Antonio Williams", "Caleb Douglas"),
  "gang-green": ("Ashton Jeanty", "Luther Burden III"),
  "team-noor": ("Jared Goff", "Ja'Marr Chase"),
  "mustafas-magnificent-team": ("Travis Kelce", "Isaiah Likely"),
  "rambam": ("Tyler Bass", "Jonathan Taylor"),
  "i-eat-ass": ("Fernando Mendoza", "Kirk Cousins"),
  "ivaafay": ("Javonte Williams", "DK Metcalf"),
  "bazan": ("Cam Ward", "Bo Nix"),
}

DEVELOPMENT = {
  "hnfnr-aint-busy": "Lost by 0.38 with an inactive Bowers (0.0) in the lineup and Brian Thomas Jr.'s 8.3 on the bench.",
  "chief-sheikh": "Fifth straight win and a clinched playoff spot; season scoring margin: +1.08 points.",
  "bizzy": "Conceded Monday at 8:29 PM, then beat the No. 1 team by 0.38. Lamb ledger: +113.10.",
  "team-mbk": "Dak Prescott started with Stafford on bye and scored 35.9; Bilal conceded Sunday and won.",
  "deddybaba": "Dropped Puka Nacua Saturday night, then lost to IVaafay with Antonio Williams' 16.7 on the bench.",
  "gang-green": "Beat the commissioner's team by 68.18. Was right about the logo: it has been the Jets all season.",
  "team-noor": "Second straight loss; Goff's 20.36 sat behind Allen's 12.16. 4-7 and ninth, as he predicted.",
  "mustafas-magnificent-team": "118.36, the weekly high and Mustafa's first $100. \"Time to do a parlay.\"",
  "rambam": "43.86, the lowest score of the season; started Stroud against three of his own Colts in a 26-3 game.",
  "i-eat-ass": "Lost by 4.46 with Mendoza's 22.88 on the bench; Evans and Montgomery scored for the first time in weeks.",
  "ivaafay": "First win since Week 4, with Bijan, Pitts and Price on bye. \"Final fkn Lee lol.\"",
  "bazan": "Four quarterbacks rostered; started Bo Nix (11.5) over Cam Ward (22.22) and lost by 6.52.",
}

S = ["QB", "RB", "RB", "WR", "WR", "TE", "FLEX", "D/ST", "K"]
def P(name, pos, nfl): return {"player": name, "position": pos, "nflTeam": nfl}
ROSTERS = {
 "gang-green": {
   "starters": [P("Trevor Lawrence","QB","JAX"),P("Ashton Jeanty","RB","LV"),P("Chuba Hubbard","RB","CAR"),P("Tetairoa McMillan","WR","CAR"),P("Luther Burden III","WR","CHI"),P("Brenton Strange","TE","JAX"),P("Garrett Wilson","WR","NYJ"),P("Jets D/ST","D/ST","NYJ"),P("Cam Little","K","JAX")],
   "bench": [P("Harold Fannin Jr.","TE","CLE"),P("Stefon Diggs","WR","WSH"),P("Mike Washington Jr.","RB","LV"),P("Jordyn Tyson","WR","NO"),P("Bryce Young","QB","CAR"),P("Justice Hill","RB","BAL"),P("Tyjae Spears (IR)","RB","TEN"),P("Jonathon Brooks (IR)","RB","CAR")]},
 "rambam": {
   "starters": [P("C.J. Stroud","QB","HOU"),P("Kaelon Black","RB","SF"),P("Jonathan Taylor","RB","IND"),P("Emeka Egbuka","WR","TB"),P("Ryan Flournoy","WR","DAL"),P("Tyler Warren","TE","IND"),P("Travis Etienne Jr.","RB","NO"),P("Chargers D/ST","D/ST","LAC"),P("Spencer Shrader","K","IND")],
   "bench": [P("Rome Odunze","WR","CHI"),P("Jayden Daniels","QB","WSH"),P("Matthew Golden","WR","GB"),P("Xavier Worthy","WR","KC"),P("Emanuel Wilson","RB","SEA"),P("Seth McGowan","RB","IND"),P("Tyler Bass","K","BUF"),P("TreVeyon Henderson (IR)","RB","NE")]},
 "bizzy": {
   "starters": [P("Tyler Shough","QB","NO"),P("Emmett Johnson","RB","KC"),P("Chase Brown","RB","CIN"),P("Nico Collins","WR","HOU"),P("CeeDee Lamb","WR","DAL"),P("Colston Loveland","TE","CHI"),P("Deebo Samuel Sr.","WR","SF"),P("Lions D/ST","D/ST","DET"),P("Jason Sanders","K","NYJ")],
   "bench": [P("Kenneth Walker III","RB","KC"),P("Rachaad White","RB","WSH"),P("Keenan Allen","WR","SF"),P("Deshaun Watson","QB","CLE"),P("Chase McLaughlin","K","TB"),P("Samaje Perine","RB","CIN"),P("Packers D/ST","D/ST","GB"),P("Drake Maye (IR)","QB","NE")]},
 "hnfnr-aint-busy": {
   "starters": [P("Joe Burrow","QB","CIN"),P("Derrick Henry","RB","BAL"),P("Tony Pollard","RB","TEN"),P("Zay Flowers","WR","BAL"),P("Malik Washington","WR","MIA"),P("Brock Bowers","TE","LV"),P("Jonah Coleman","RB","DEN"),P("Steelers D/ST","D/ST","PIT"),P("Cameron Dicker","K","LAC")],
   "bench": [P("Jaxon Smith-Njigba","WR","SEA"),P("Rhamondre Stevenson","RB","NE"),P("Brian Thomas Jr.","WR","JAX"),P("Tyler Allgeier","RB","ARI"),P("Dalton Kincaid","TE","BUF"),P("Denzel Boston","WR","CLE"),P("Jason Myers","K","SEA"),P("Jacory Croskey-Merritt (IR)","RB","WSH")]},
 "deddybaba": {
   "starters": [P("Brock Purdy","QB","SF"),P("Ollie Gordon II","RB","MIA"),P("Bucky Irving","RB","TB"),P("Rashee Rice","WR","KC"),P("Caleb Douglas","WR","MIA"),P("Dalton Schultz","TE","HOU"),P("Bhayshul Tuten","RB","JAX"),P("Broncos D/ST","D/ST","DEN"),P("Ka'imi Fairbairn","K","HOU")],
   "bench": [P("Tucker Kraft","TE","GB"),P("Kenny Gainwell","RB","TB"),P("Josh Downs","WR","KC"),P("Antonio Williams","WR","WSH"),P("Jaguars D/ST","D/ST","JAX"),P("Pat Bryant","WR","DEN"),P("RJ Harvey (IR)","RB","DEN")]},
 "ivaafay": {
   "starters": [P("Caleb Williams","QB","CHI"),P("Javonte Williams","RB","DAL"),P("Jordan Mason","RB","MIN"),P("George Pickens","WR","DAL"),P("DK Metcalf","WR","PIT"),P("Chig Okonkwo","TE","WSH"),P("Courtland Sutton","WR","DEN"),P("Bears D/ST","D/ST","CHI"),P("Jake Bates","K","DET")],
   "bench": [P("Bijan Robinson","RB","ATL"),P("Jadarian Price","RB","SEA"),P("Kyle Pitts Sr.","TE","ATL"),P("Jordan Addison","WR","MIN"),P("Alvin Kamara","RB","NO"),P("Khalil Shakir","WR","BUF"),P("Commanders D/ST","D/ST","WSH"),P("Davante Adams (IR)","WR","LAR")]},
 "team-noor": {
   "starters": [P("Josh Allen","QB","BUF"),P("Breece Hall","RB","NYJ"),P("Aaron Jones Sr.","RB","MIN"),P("Ja'Marr Chase","WR","CIN"),P("Xavier Hutchinson","WR","HOU"),P("George Kittle","TE","SF"),P("Jaylen Waddle","WR","DEN"),P("49ers D/ST","D/ST","SF"),P("Evan McPherson","K","CIN")],
   "bench": [P("Kyren Williams","RB","LAR"),P("Christian Watson","WR","GB"),P("J.K. Dobbins","RB","DEN"),P("Mark Andrews","TE","BAL"),P("Jared Goff","QB","DET"),P("Tre Tucker","WR","LV"),P("Tutu Atwell","WR","LAR")]},
 "team-mbk": {
   "starters": [P("Dak Prescott","QB","DAL"),P("Jahmyr Gibbs","RB","DET"),P("Rico Dowdle","RB","PIT"),P("Tee Higgins","WR","CIN"),P("Tank Dell","WR","HOU"),P("Sam LaPorta","TE","DET"),P("Dallas Goedert","TE","PHI"),P("Bengals D/ST","D/ST","CIN"),P("Chris Boswell","K","PIT")],
   "bench": [P("Drake London","WR","ATL"),P("Seahawks D/ST","D/ST","SEA"),P("Matthew Stafford","QB","LAR"),P("KC Concepcion","WR","CLE"),P("Quinshon Judkins","RB","CLE"),P("Sione Vaki","RB","DET"),P("Michael Pittman Jr. (IR)","WR","PIT"),P("Josh Jacobs (IR)","RB","GB")]},
 "bazan": {
   "starters": [P("Bo Nix","QB","DEN"),P("James Cook III","RB","BUF"),P("D'Andre Swift","RB","CHI"),P("Malik Nabers","WR","NYG"),P("Carnell Tate","WR","TEN"),P("Pat Freiermuth","TE","PIT"),P("Adonai Mitchell","WR","NYJ"),P("Chiefs D/ST","D/ST","KC"),P("Will Reichard","K","MIN")],
   "bench": [P("Kyle Monangai","RB","CHI"),P("Jalen Coker","WR","CAR"),P("Ray Davis","RB","BUF"),P("Konata Mumpfield","WR","LAR"),P("Cam Ward","QB","TEN"),P("Elic Ayomanor","WR","TEN"),P("Aaron Rodgers","QB","PIT"),P("Lamar Jackson (IR)","QB","BAL")]},
 "chief-sheikh": {
   "starters": [P("J.J. McCarthy","QB","NYG"),P("Cam Skattebo","RB","NYG"),P("Jaylen Warren","RB","PIT"),P("Justin Jefferson","WR","MIN"),P("Parker Washington","WR","JAX"),P("Trey McBride","TE","ARI"),P("Amon-Ra St. Brown","WR","DET"),P("Texans D/ST","D/ST","HOU"),P("Brandon Aubrey","K","DAL")],
   "bench": [P("Blake Corum","RB","LAR"),P("Braelon Allen","RB","NYJ"),P("Jordan Love","QB","GB"),P("Dylan Sampson","RB","CLE"),P("Mack Hollins","WR","NE"),P("Buccaneers D/ST","D/ST","TB"),P("Roman Wilson","WR","PIT"),P("Brandon Aiyuk (IR)","WR","FA")]},
 "i-eat-ass": {
   "starters": [P("Kirk Cousins","QB","MIN"),P("Christian McCaffrey","RB","SF"),P("David Montgomery","RB","HOU"),P("Chris Olave","WR","NO"),P("Jameson Williams","WR","DET"),P("T.J. Hockenson","TE","MIN"),P("Mike Evans","WR","SF"),P("Panthers D/ST","D/ST","CAR"),P("Dominic Zvada","K","NYG")],
   "bench": [P("Woody Marks","RB","HOU"),P("Devaughn Vele","WR","NO"),P("Jakobi Meyers","WR","JAX"),P("Chris Rodriguez Jr.","RB","JAX"),P("Mike Gesicki","TE","CIN"),P("Fernando Mendoza","QB","LV"),P("A.J. Brown","WR","NE"),P("Jeremiyah Love (IR)","RB","ARI")]},
 "mustafas-magnificent-team": {
   "starters": [P("Patrick Mahomes","QB","KC"),P("Omarion Hampton","RB","LAC"),P("Saquon Barkley","RB","PHI"),P("DeVonta Smith","WR","PHI"),P("DJ Moore","WR","BUF"),P("Isaiah Likely","TE","NYG"),P("Travis Kelce","TE","KC"),P("Bills D/ST","D/ST","BUF"),P("Cairo Santos","K","CHI")],
   "bench": [P("Ladd McConkey","WR","LAC"),P("Zach Charbonnet","RB","SEA"),P("Vikings D/ST","D/ST","MIN"),P("Germie Bernard","WR","PIT"),P("Makai Lemon","WR","PHI"),P("Kimani Vidal","RB","LAC"),P("Tank Bigsby (IR)","RB","PHI")]},
}
for tid, r in ROSTERS.items():
    slots = [{"slot": s, **p} for s, p in zip(S, r["starters"])]
    ROSTERS[tid] = {"starters": slots, "bench": r["bench"]}

# cumulative records + PF from all results through week 5
rec = {t: {"wins": 0, "losses": 0} for t in PRE_RANK}
pf = {t: 0.0 for t in PRE_RANK}
for wk in (1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11):
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
for m in schedule["weeks"]["12"]:
    nxt[m["away"]] = f'at {teams_meta[m["home"]]["teamName"]}'
    nxt[m["home"]] = f'vs {teams_meta[m["away"]]["teamName"]}'

out = {"week": 11, "publishedAt": "2026-11-24", "deck": editorial["deck"], "teams": []}
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

json.dump(out, open(f"{ROOT}/data/weeks/week-11.json", "w"), indent=2)
print("odds sum:", round(sum(t["titleOdds"] for t in out["teams"]), 1))
for t in out["teams"]:
    mv = PRE_RANK[t["teamId"]] - t["powerRank"]
    delta_sum = round(sum(m["delta"] for m in t["movementReasons"]), 1)
    print(f'#{t["powerRank"]:>2} {t["teamId"]:<28} {"↑" + str(mv) if mv > 0 else "↓" + str(-mv) if mv < 0 else "—":>3}  {t["powerScore"]:>5}  {t["titleOdds"]:>4}%  {t["record"]["wins"]}-{t["record"]["losses"]}  PF {t["pointsFor"]:>6}  Δreasons {delta_sum}')

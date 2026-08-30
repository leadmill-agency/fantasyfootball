#!/usr/bin/env python3
"""Fetch ESPN Live Draft Results ADP and match it to the league's 192 picks.

The league drafts in the ESPN app, so ESPN ADP is the market the room
actually drafted against. Output: data/adp-espn.json. Players ESPN doesn't
rank get adp: null — unknowns stay unknown, never invented.

The FFC source (data/adp.json) is untouched: it remains the recorded input
of the frozen team draft grades and the compare-page positional edges.
"""
import json, os, re, unicodedata, urllib.request

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
ENDPOINT = ("https://lm-api-reads.fantasy.espn.com/apis/v3/games/ffl/seasons/2026"
            "/segments/0/leaguedefaults/3?scoringPeriodId=0&view=kona_player_info")
FILTER = '{"players":{"limit":1200,"sortAdp":{"sortAsc":true,"sortPriority":1}}}'

req = urllib.request.Request(ENDPOINT, headers={
    "x-fantasy-filter": FILTER,
    "Accept": "application/json",
    "User-Agent": "Mozilla/5.0",
})
with urllib.request.urlopen(req, timeout=60) as r:
    espn = json.load(r)["players"]

def norm(name):
    n = unicodedata.normalize("NFKD", name).lower()
    n = re.sub(r"[.'’\-]", "", n)
    n = re.sub(r"\b(jr|sr|ii|iii|iv|v)\b", "", n)
    return re.sub(r"\s+", " ", n).strip()

by_name, dst_by_name = {}, {}
for p in espn:
    pl = p["player"]
    adp = pl.get("ownership", {}).get("averageDraftPosition")
    if adp is None:
        continue
    entry = {"adp": round(adp, 1), "espnName": pl["fullName"]}
    if pl.get("defaultPositionId") == 16:
        dst_by_name[pl["fullName"]] = entry
    else:
        by_name.setdefault(norm(pl["fullName"]), entry)

draft = json.load(open(f"{ROOT}/data/draft.json"))
out_players, unmatched = [], []
for pick in draft["picks"]:
    src = (dst_by_name.get(pick["player"]) if pick["position"] == "D/ST"
           else by_name.get(norm(pick["player"])))
    entry = {
        "player": pick["player"],
        "position": pick["position"],
        "nflTeam": pick["nflTeam"],
        "overallPick": pick["overall"],
        "teamId": pick["teamId"],
    }
    if src:
        entry["adp"] = src["adp"]
        entry["adpDiff"] = round(pick["overall"] - src["adp"], 1)
        entry["espnName"] = src["espnName"]
    else:
        entry["adp"] = None
        entry["note"] = "Not ranked in ESPN Live Draft Results at retrieval time"
        unmatched.append(f'{pick["player"]} (pick {pick["overall"]})')
    out_players.append(entry)

out = {
    "source": {
        "name": "ESPN Live Draft Results",
        "url": "https://fantasy.espn.com/football/livedraftresults",
        "api": ENDPOINT,
        "retrievedAt": "2026-08-29",
        "note": "The league drafts in the ESPN app; this is the market the room drafted against. adpDiff = overall pick minus ADP: positive = drafted later than price (value), negative = earlier (reach).",
    },
    "players": out_players,
}
json.dump(out, open(f"{ROOT}/data/adp-espn.json", "w"), indent=2)
matched = sum(1 for p in out_players if p["adp"] is not None)
print(f"matched {matched}/192")
if unmatched:
    print("null ADP:", "; ".join(unmatched))

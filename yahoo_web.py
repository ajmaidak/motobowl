#!/usr/bin/env python3
"""Fetch Yahoo Fantasy web pages with a logged-in browser session.

A stopgap until the Yahoo API is provisioned: replaces hand-pasting by
requesting the same pages the browser shows, authenticated with the session
cookie copied out of the browser. Read-only — GETs only, never a form post.

The cookie is a full Yahoo account credential. It lives in .yahoo-cookie
(gitignored; this repo is public) or the YAHOO_COOKIE environment variable,
and is never logged or cached. To get it:

    1. Log in at football.fantasysports.yahoo.com in Chrome.
    2. DevTools -> Network -> reload -> click the first document request.
    3. Request Headers -> copy the value of `cookie:` (the value only).
    4. pbpaste > .yahoo-cookie && chmod 600 .yahoo-cookie

Sessions expire; when a fetch lands on the login page this fails loudly
rather than caching the login page as if it were data. Repeat the steps.

Raw HTML is cached under cache/yahoo/ with an age check, like sources.py.

    python3 yahoo_web.py check                 # is the cookie logged in?
    python3 yahoo_web.py roster [WEEK]         # My Team page
    python3 yahoo_web.py matchup WEEK          # my matchup for a week
    python3 yahoo_web.py fa [WEEK]             # free agents, every position
    python3 yahoo_web.py all WEEK              # roster + matchup + free agents
    python3 yahoo_web.py sync WEEK             # fetch all, parse, write data/*.json

`sync` writes the same parsed files the paste workflow produced —
data/my-roster.json, data/opponent-roster.json, data/free-agents.json — so
nothing downstream needs to know which one made them.
"""

import json
import os
import sys
import time
from datetime import datetime, timezone

import requests

HERE = os.path.dirname(os.path.abspath(__file__))
COOKIE_FILE = os.path.join(HERE, ".yahoo-cookie")
CACHE_DIR = os.path.join(HERE, "cache", "yahoo")
DATA_DIR = os.path.join(HERE, "data")

LEAGUE_ID = 130450
TEAM_ID = 9
BASE = f"https://football.fantasysports.yahoo.com/f1/{LEAGUE_ID}"

FA_POSITIONS = ["QB", "RB", "WR", "TE", "K", "DEF"]
FA_PAGES = 2            # 25 rows per page
REQUEST_GAP_SECONDS = 2  # be a polite, human-paced client

USER_AGENT = (
    "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 "
    "(KHTML, like Gecko) Chrome/128.0 Safari/537.36"
)


class SessionError(Exception):
    pass


def _cookie():
    value = os.environ.get("YAHOO_COOKIE")
    if not value and os.path.exists(COOKIE_FILE):
        with open(COOKIE_FILE) as fh:
            value = fh.read()
    value = (value or "").strip()
    if value.lower().startswith("cookie:"):
        value = value[len("cookie:"):].strip()
    if not value:
        raise SessionError(f"No Yahoo cookie. See the steps at the top of {__file__}.")
    return value


_last_request = 0.0


def fetch(url, name, max_age_hours=1):
    """GET a page as the logged-in user, caching the HTML. Returns (html, from_cache)."""
    global _last_request
    os.makedirs(CACHE_DIR, exist_ok=True)
    path = os.path.join(CACHE_DIR, name + ".html")
    if os.path.exists(path) and (time.time() - os.path.getmtime(path)) / 3600 < max_age_hours:
        with open(path, encoding="utf-8") as fh:
            return fh.read(), True

    wait = REQUEST_GAP_SECONDS - (time.time() - _last_request)
    if wait > 0:
        time.sleep(wait)
    resp = requests.get(
        url,
        headers={"Cookie": _cookie(), "User-Agent": USER_AGENT},
        timeout=30,
    )
    _last_request = time.time()

    if "login.yahoo.com" in resp.url:
        raise SessionError("Redirected to Yahoo login — the cookie is expired or incomplete.")
    if resp.status_code != 200:
        raise SessionError(f"{resp.status_code} from {url}")
    if f"/f1/{LEAGUE_ID}" not in resp.text:
        raise SessionError(f"{url} returned a page that doesn't mention league {LEAGUE_ID}.")

    with open(path, "w", encoding="utf-8") as fh:
        fh.write(resp.text)
    return resp.text, False


# URLs. Verified against the pages' own controls on 2026-09-16: stat1=S_PW_<week>
# is "Week N (proj)", S_W_<week> actual, S_S_2026 season total; status=A is
# free agents plus players on waivers; sort=PTS&sdir=1 is by points, descending.

def roster_url(week=None):
    return f"{BASE}/{TEAM_ID}" + (f"?week={week}" if week else "")


def matchup_url(week):
    return f"{BASE}/matchup?week={week}&mid1={TEAM_ID}"


def fa_url(pos, week=None, start=0):
    stat = f"S_PW_{week}" if week else "S_S_2026"   # projected week vs season
    return (f"{BASE}/players?status=A&pos={pos}&stat1={stat}"
            f"&sort=PTS&sdir=1&count={start}")


def fetch_roster(week=None, **kw):
    return fetch(roster_url(week), f"roster_w{week or 'current'}", **kw)


def fetch_matchup(week, **kw):
    return fetch(matchup_url(week), f"matchup_w{week}", **kw)


def fetch_free_agents(week=None, **kw):
    pages = {}
    for pos in FA_POSITIONS:
        for page in range(FA_PAGES):
            start = page * 25
            name = f"fa_{pos.lower()}_w{week or 'season'}_p{page}"
            pages[name], _ = fetch(fa_url(pos, week, start), name, **kw)
    return pages


def _write_json(name, obj):
    path = os.path.join(DATA_DIR, name)
    with open(path, "w", encoding="utf-8") as fh:
        json.dump(obj, fh, indent=2, ensure_ascii=False)
        fh.write("\n")
    return path


def sync(week):
    """Fetch every page for a week and write the parsed data/*.json files."""
    from parse_yahoo_html import parse_matchup, parse_players, parse_roster

    fetched = datetime.now(timezone.utc).isoformat(timespec="seconds")
    source = {"source": "yahoo-web", "fetched": fetched}

    roster = parse_roster(fetch_roster(week, max_age_hours=0)[0])
    if roster["meta"]["week"] != week:
        raise SessionError(f"asked for week {week}, roster page shows week {roster['meta']['week']}")
    roster["meta"].update(source)
    print(f"  my roster: {len(roster['players'])} players -> {_write_json('my-roster.json', roster)}")

    matchup = parse_matchup(fetch_matchup(week, max_age_hours=0)[0])
    opp = matchup["opponent"]
    opp["meta"].update(week=week, **source)
    print(f"  opponent:  {opp['meta']['team_name']}, {len(opp['players'])} players, "
          f"proj {opp['meta']['proj_total']} vs mine {matchup['me']['meta']['proj_total']} "
          f"-> {_write_json('opponent-roster.json', opp)}")

    players, seen, views = [], set(), set()
    for name, html in fetch_free_agents(week, max_age_hours=0).items():
        page = parse_players(html)
        views.add(page["meta"]["stat_view"])
        for p in page["players"]:
            if p["yahoo_id"] not in seen:
                seen.add(p["yahoo_id"])
                players.append(p)
    if views != {f"S_PW_{week}"}:
        raise SessionError(f"free-agent pages came back in stat view(s) {views}, not week {week} projections")
    fa = {"meta": {"week": week, "stat_view": f"S_PW_{week}", "projected": True, **source},
          "players": players}
    by_pos = {pos: sum(p["pos"] == pos for p in players) for pos in FA_POSITIONS}
    print(f"  free agents: {len(players)} {by_pos} -> {_write_json('free-agents.json', fa)}")


def check():
    html, cached = fetch_roster(max_age_hours=0)
    print(f"OK — logged in, roster page fetched ({len(html):,} bytes) "
          f"-> {os.path.join(CACHE_DIR, 'roster_wcurrent.html')}")


def main():
    args = sys.argv[1:]
    cmd = args[0] if args else "check"
    week = int(args[1]) if len(args) > 1 else None
    try:
        if cmd == "check":
            check()
        elif cmd == "roster":
            fetch_roster(week, max_age_hours=0)
        elif cmd == "matchup":
            fetch_matchup(week, max_age_hours=0)
        elif cmd == "fa":
            fetch_free_agents(week, max_age_hours=0)
        elif cmd == "sync":
            if week is None:
                sys.exit("usage: yahoo_web.py sync WEEK")
            sync(week)
            return
        elif cmd == "all":
            fetch_roster(week, max_age_hours=0)
            fetch_matchup(week, max_age_hours=0)
            fetch_free_agents(week, max_age_hours=0)
        else:
            print(__doc__)
            return
    except SessionError as exc:
        sys.exit(f"error: {exc}")
    if cmd != "check":
        print(f"saved under {CACHE_DIR}")


if __name__ == "__main__":
    main()

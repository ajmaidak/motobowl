#!/usr/bin/env python3
"""Clients for external data sources.

    Sleeper      free, no auth. Player dump (canonical IDs, positions, injury
                 status, depth chart), waiver trends, weekly stats, and weekly
                 projections for every player (scored under league rules).
    nflverse     free, no auth. Flat CSV/parquet released on GitHub — weekly
                 stats, snap counts, depth charts, injuries, rosters, pbp.
    FantasyPros  API key required (valid). Projections and 2025 consensus
                 rankings. Free tier caps results at top 10 per position.
    DynastyProcess  free. Player-ID crosswalk (yahoo_id <-> sleeper_id <-> gsis_id).
    ffopportunity   free. Actual vs expected fantasy points from play-by-play.
    ESPN         free, no auth. Spreads, totals -> implied team totals; venues.
    Open-Meteo   free, no auth. Kickoff-hour wind/rain for outdoor games.
    QBERT        Silver Bulletin QB ratings, from the post's free preview.

Everything is cached under cache/ (gitignored) with an age check, so repeated
calls in a week don't re-download. Sleeper's player dump alone is ~14MB.

    python3 sources.py check          # health-check all three
    python3 sources.py cache          # what is cached and how old
    python3 sources.py refresh        # force re-fetch everything
    python3 sources.py refresh injuries sleeper-trending
    python3 sources.py trending       # top waiver adds right now
    python3 sources.py games [WEEK]   # lines, implied totals, weather
    python3 sources.py qbert          # current QBERT ratings
"""

import csv
import io
import json
import os
import re
import sys
import time

import requests

HERE = os.path.dirname(os.path.abspath(__file__))
CACHE_DIR = os.path.join(HERE, "cache")
CREDS_FILE = os.path.join(HERE, ".credentials.json")

SLEEPER_BASE = "https://api.sleeper.app/v1"
NFLVERSE_BASE = "https://github.com/nflverse/nflverse-data/releases/download"
FANTASYPROS_BASE = "https://api.fantasypros.com/public/v2/json"
SLEEPER_PROJ_BASE = "https://api.sleeper.com"
DP_IDS_URL = "https://github.com/dynastyprocess/data/raw/master/files/db_playerids.csv"
FFOPP_BASE = "https://github.com/ffverse/ffopportunity/releases/download/v1.0.0-data"
ESPN_SCOREBOARD = "https://site.api.espn.com/apis/site/v2/sports/football/nfl/scoreboard"
GEOCODE_URL = "https://geocoding-api.open-meteo.com/v1/search"
FORECAST_URL = "https://api.open-meteo.com/v1/forecast"
SILVER_API = "https://www.natesilver.net/api/v1"
DATAWRAPPER_BASE = "https://datawrapper.dwcdn.net"


class SourceError(Exception):
    pass


# --------------------------------------------------------------------------
# cache
# --------------------------------------------------------------------------

def _cache_file(name):
    os.makedirs(CACHE_DIR, exist_ok=True)
    return os.path.join(CACHE_DIR, name)


def _fresh(path, max_age_hours):
    if not os.path.exists(path):
        return False
    age_hours = (time.time() - os.path.getmtime(path)) / 3600
    return age_hours < max_age_hours


def cached_get(url, filename, max_age_hours=24, headers=None):
    """GET a URL, caching the raw body. Returns (text, from_cache)."""
    path = _cache_file(filename)
    if _fresh(path, max_age_hours):
        with open(path, encoding="utf-8") as fh:
            return fh.read(), True

    resp = requests.get(url, headers=headers or {}, timeout=60)
    if resp.status_code != 200:
        raise SourceError(f"{resp.status_code} from {url}: {resp.text[:200]}")

    with open(path, "w", encoding="utf-8") as fh:
        fh.write(resp.text)
    return resp.text, False


def cache_age_hours(filename):
    """How stale is a cached file? None if absent. Report this when it matters."""
    path = _cache_file(filename)
    if not os.path.exists(path):
        return None
    return (time.time() - os.path.getmtime(path)) / 3600


# --------------------------------------------------------------------------
# Sleeper — no auth
# --------------------------------------------------------------------------

def sleeper_players(max_age_hours=24):
    """Full NFL player dump keyed by Sleeper player_id (~14MB, cache it).

    Sleeper's player_id is the best canonical key available for joining these
    sources: records carry gsis_id (joins nflverse), espn_id, yahoo_id, and
    fantasy_data_id alongside position, team, depth chart order and injury
    status.
    """
    text, _ = cached_get(
        f"{SLEEPER_BASE}/players/nfl", "sleeper_players.json", max_age_hours
    )
    return json.loads(text)


def sleeper_trending(kind="add", lookback_hours=24, limit=25, max_age_hours=3):
    """Most-added (or dropped) players league-wide — a live waiver signal.

    Returns [{player_id, count}]; join against sleeper_players() for names.
    Cached briefly since the whole point is that it moves.
    """
    url = f"{SLEEPER_BASE}/players/nfl/trending/{kind}?lookback_hours={lookback_hours}&limit={limit}"
    # limit belongs in the cache key: a small fetch must not satisfy a larger one.
    cache_name = f"sleeper_trending_{kind}_{lookback_hours}h_{limit}.json"
    text, _ = cached_get(url, cache_name, max_age_hours)
    return json.loads(text)


def sleeper_stats(season, week, season_type="regular", max_age_hours=6):
    """Weekly stats keyed by Sleeper player_id."""
    url = f"{SLEEPER_BASE}/stats/nfl/{season_type}/{season}/{week}"
    text, _ = cached_get(url, f"sleeper_stats_{season}_w{week}.json", max_age_hours)
    return json.loads(text)


def trending_named(kind="add", limit=15):
    """Trending adds/drops resolved to names — the usable form."""
    trend = sleeper_trending(kind=kind, limit=limit)
    players = sleeper_players()
    out = []
    for row in trend:
        p = players.get(row["player_id"], {})
        out.append({
            "name": p.get("full_name") or p.get("last_name") or row["player_id"],
            "pos": p.get("position"),
            "team": p.get("team"),
            "injury_status": p.get("injury_status"),
            "count": row["count"],
        })
    return out


# --------------------------------------------------------------------------
# nflverse — no auth, flat files
# --------------------------------------------------------------------------

def nflverse_csv(release, filename, max_age_hours=12):
    """Fetch a CSV asset from an nflverse-data release as a list of dicts.

    Useful (release, filename) pairs:
        injuries        injuries_{season}.csv        weekly injury reports
        depth_charts    depth_charts_{season}.csv    depth chart position
        weekly_rosters  roster_weekly_{season}.csv   who is actually rostered
        snap_counts     snap_counts_{season}.csv     snap share
        stats_player    stats_player_week_{season}.csv
        schedules       games.csv                    all seasons, one file

    Current-season files appear only once there is data to put in them, so a
    404 early in a season is expected rather than an error in the caller.
    """
    url = f"{NFLVERSE_BASE}/{release}/{filename}"
    text, _ = cached_get(url, f"nflverse_{filename}", max_age_hours)
    return list(csv.DictReader(io.StringIO(text)))


def nfl_injuries(season, week=None, max_age_hours=6):
    """Injury report rows, optionally filtered to one week.

    Reports fill in through the practice week (Wed-Fri) and are sparse before
    that, so check how many rows come back before trusting an empty result as
    'nobody is hurt'.
    """
    rows = nflverse_csv("injuries", f"injuries_{season}.csv", max_age_hours)
    if week is not None:
        rows = [r for r in rows if str(r.get("week")) == str(week)]
    return rows


# --------------------------------------------------------------------------
# FantasyPros — API key required
# --------------------------------------------------------------------------
#
# The key is valid and every endpoint works.
#
# TRANSIENT 403s: when the key was first used (2026-09-09) every endpoint
# returned 403 ForbiddenException for ~15 minutes, indistinguishable from an
# invalid key, then began working with no change on our side — most likely key
# provisioning propagating. If a 403 appears, retry before concluding anything
# is wrong. Re-verified after: 12/12 and 8/8 successes, with and without an
# Origin header.
#
# REAL LIMIT — free tier: results are capped at the top 10 players per position
# (`limit: 10`, `public_api_limited: true`, `tier: free`) while `count` reports
# the full field (462 for week-1 rankings, 213 WRs for projections). That cap
# skews to obvious starters — see fp_projections() for what that costs.

def _fantasypros_key():
    key = os.environ.get("FANTASYPROS_API_KEY")
    if key:
        return key
    if os.path.exists(CREDS_FILE):
        key = json.load(open(CREDS_FILE)).get("fantasypros_api_key")
        if key:
            return key
    raise SourceError("No FantasyPros API key (set FANTASYPROS_API_KEY or add it to .credentials.json)")


def fantasypros(path, max_age_hours=6, **params):
    """GET a FantasyPros v2 endpoint, e.g. 'nfl/2026/consensus-rankings'."""
    key = _fantasypros_key()
    query = "&".join(f"{k}={v}" for k, v in sorted(params.items()))
    url = f"{FANTASYPROS_BASE}/{path.lstrip('/')}" + (f"?{query}" if query else "")
    slug = path.strip("/").replace("/", "_") + ("_" + query.replace("&", "_").replace("=", "-") if query else "")

    try:
        text, _ = cached_get(url, f"fp_{slug}.json", max_age_hours, headers={"x-api-key": key})
    except SourceError as exc:
        if "403" in str(exc):
            raise SourceError(
                f"FantasyPros 403 for {path}. The key is valid — 403s have been "
                "observed transiently. Retry before concluding the key or the "
                "endpoint is wrong."
            ) from exc
        raise
    return json.loads(text)


def consensus_rankings(season, week=None, position="ALL", scoring="PPR", max_age_hours=6):
    """Expert consensus rankings (ECR) with tiers. Weekly if week is given."""
    params = {"position": position, "scoring": scoring}
    params["type"] = "weekly" if week else "draft"
    if week:
        params["week"] = week
    return fantasypros(f"nfl/{season}/consensus-rankings", max_age_hours=max_age_hours, **params)


def current_week(default=1):
    """The league week the last `yahoo_web.py sync` was run for.

    Read from data/my-roster.json's meta.week so weekly fetchers (rankings,
    projections) follow the sync rather than a hard-coded number. Falls back
    to `default` when no roster has been synced yet.
    """
    path = os.path.join(HERE, "data", "my-roster.json")
    try:
        with open(path) as fh:
            week = json.load(fh).get("meta", {}).get("week")
        return int(week) if week else default
    except (OSError, ValueError, AttributeError):
        return default


def fp_projections(season, week, position, max_age_hours=6):
    """Projected stat lines, keyed by player name.

    Each record's `stats` carries `points_ppr`, `points_half` and `points` (STD)
    plus the raw components (rec_rec, rec_yds, rec_tds, rush_*, fumbles, ...),
    so league-exact scoring can be computed from the components rather than
    trusting the prepackaged totals. Ignore the top-level `scoring` field — it
    reports STD regardless of what was requested.

    Free tier returns only the top 10 per position, which in practice covers the
    starters you were never unsure about and omits the bench/flex players the
    decision actually turns on. Check membership before relying on it.
    """
    data = fantasypros(f"nfl/{season}/projections", max_age_hours=max_age_hours,
                       position=position, week=week)
    return {p["name"]: p for p in data.get("players", [])}


# --------------------------------------------------------------------------
# Sleeper projections — no auth, full coverage, league-exact scoring
# --------------------------------------------------------------------------
#
# api.sleeper.com (not api.sleeper.app) serves weekly projections for every
# player, supplied by Rotowire (`company`). Undocumented but stable, and unlike
# the FantasyPros free tier it covers the whole roster and the waiver wire.
# Each record carries raw stat components, so points are computed from the
# league's own rules in data/league-settings.json rather than Sleeper's
# pts_ppr (which uses 4-point pass TDs and -1 INTs).

SETTINGS_FILE = os.path.join(HERE, "data", "league-settings.json")

# Yahoo rule name (as parsed into league-settings.json) -> Sleeper stat keys.
# An unmapped rule raises rather than silently scoring it as zero.
_SCORING_KEYS = {
    "offense": {
        "Passing Yards": ["pass_yd"],
        "Passing Touchdowns": ["pass_td"],
        "Interceptions": ["pass_int"],
        "Rushing Yards": ["rush_yd"],
        "Rushing Touchdowns": ["rush_td"],
        "Receptions": ["rec"],
        "Receiving Yards": ["rec_yd"],
        "Receiving Touchdowns": ["rec_td"],
        "Return Touchdowns": ["kr_td", "pr_td"],
        "2-Point Conversions": ["pass_2pt", "rush_2pt", "rec_2pt"],
        "Fumbles Lost": ["fum_lost"],
        "Offensive Fumble Return TD": ["fum_rec_td"],
    },
    "kickers": {
        "Field Goals 0-19 Yards": ["fgm_0_19"],
        "Field Goals 20-29 Yards": ["fgm_20_29"],
        "Field Goals 30-39 Yards": ["fgm_30_39"],
        "Field Goals 40-49 Yards": ["fgm_40_49"],
        "Field Goals 50+ Yards": ["fgm_50p"],
        "Point After Attempt Made": ["xpm"],
    },
    "dst": {
        "Sack": ["sack"],
        "Interception": ["int"],
        "Fumble Recovery": ["fum_rec"],
        "Touchdown": ["def_td", "st_td"],
        "Safety": ["safe"],
        "Block Kick": ["blk_kick"],
        "Points Allowed 0 points": ["pts_allow_0"],
        "Points Allowed 1-6 points": ["pts_allow_1_6"],
        "Points Allowed 7-13 points": ["pts_allow_7_13"],
        "Points Allowed 14-20 points": ["pts_allow_14_20"],
        "Points Allowed 21-27 points": ["pts_allow_21_27"],
        "Points Allowed 28-34 points": ["pts_allow_28_34"],
        "Points Allowed 35+ points": ["pts_allow_35p"],
        "Extra Point Returned": ["def_2pt"],
    },
}

_PTS_ALLOW_BUCKETS = [(0, "pts_allow_0"), (6, "pts_allow_1_6"), (13, "pts_allow_7_13"),
                      (20, "pts_allow_14_20"), (27, "pts_allow_21_27"),
                      (34, "pts_allow_28_34"), (float("inf"), "pts_allow_35p")]


def league_scoring():
    """The league's scoring rules, from data/league-settings.json."""
    with open(SETTINGS_FILE) as fh:
        return json.load(fh)["scoring"]


def league_points(stats, pos, scoring=None):
    """Score a Sleeper stat line (projected or actual) under league rules.

    Unrounded on purpose: Yahoo scores whole points, but a projection is an
    expectation, and rounding it just hides the gap. Treat differences under
    ~2 points as noise either way.
    """
    scoring = scoring or league_scoring()
    section = {"K": "kickers", "DEF": "dst"}.get(pos, "offense")
    stats = dict(stats)
    if section == "dst" and "pts_allow" in stats and not any(
            k in stats for _, k in _PTS_ALLOW_BUCKETS):
        allowed = stats["pts_allow"]
        stats[next(k for cap, k in _PTS_ALLOW_BUCKETS if allowed <= cap)] = 1.0

    total = 0.0
    for rule, value in scoring[section].items():
        keys = _SCORING_KEYS[section].get(rule)
        if keys is None:
            raise SourceError(f"no Sleeper stat mapping for {section} rule {rule!r} — "
                              "add it to _SCORING_KEYS in sources.py")
        amount = sum(stats.get(k, 0) or 0 for k in keys)
        if isinstance(value, dict):
            total += amount / value["yards_per_point"]
        else:
            total += amount * value
    return round(total, 1)


def sleeper_projections(season, week, season_type="regular", max_age_hours=6):
    """Weekly projections for every QB/RB/WR/TE/K/DEF, keyed by Sleeper player_id.

    Each value: name, pos, team, opponent, company, stats (raw components plus
    Sleeper's pts_ppr) and league_pts (scored under this league's rules).
    A player is absent when Rotowire isn't projecting him to play — bye, or
    ruled out (Rico Dowdle, Out/toe, 2026-09-25) — so a rostered player with
    no projection is a flag to check, not a gap. DEF ids are team abbreviations.
    """
    positions = "&".join(f"position[]={p}" for p in ("QB", "RB", "WR", "TE", "K", "DEF"))
    url = (f"{SLEEPER_PROJ_BASE}/projections/nfl/{season}/{week}"
           f"?season_type={season_type}&{positions}")
    text, _ = cached_get(url, f"sleeper_proj_{season}_w{week}.json", max_age_hours)
    scoring = league_scoring()
    out = {}
    for row in json.loads(text):
        stats = row.get("stats") or {}
        player = row.get("player") or {}
        if not stats.get("gp"):
            continue
        pos = player.get("position")
        out[row["player_id"]] = {
            "name": f"{player.get('first_name', '')} {player.get('last_name', '')}".strip(),
            "pos": pos,
            "team": row.get("team"),
            "opponent": row.get("opponent"),
            "company": row.get("company"),
            "stats": stats,
            "league_pts": league_points(stats, pos, scoring),
        }
    if not out:
        raise SourceError(f"Sleeper returned no projections for {season} week {week}")
    return out


# --------------------------------------------------------------------------
# DynastyProcess player-ID crosswalk — no auth
# --------------------------------------------------------------------------
#
# One row per player with yahoo_id, sleeper_id, gsis_id, fantasypros_id,
# espn_id, pfr_id and more. Covers far more yahoo_ids than Sleeper's own
# yahoo_id field (12 of 16 roster players vs 5 on 2026-09-25). New rookies lag,
# hence the name fallback in yahoo_to_sleeper().

def ff_player_ids(max_age_hours=24 * 7):
    """The DynastyProcess ID crosswalk as a list of dicts ('NA' -> '')."""
    text, _ = cached_get(DP_IDS_URL, "dp_playerids.csv", max_age_hours)
    return [{k: ("" if v == "NA" else v) for k, v in row.items()}
            for row in csv.DictReader(io.StringIO(text))]


def _norm_name(name):
    name = re.sub(r"[^a-z ]", "", (name or "").lower().replace("-", " "))
    return " ".join(w for w in name.split() if w not in {"jr", "sr", "ii", "iii", "iv", "v"})


def yahoo_to_sleeper(records):
    """Map Yahoo player records (data/*.json) to Sleeper ids: {yahoo_id: sleeper_id}.

    Tries, in order: DEF -> team abbreviation; DynastyProcess crosswalk;
    Sleeper's own yahoo_id; unique name + position + team match. Players that
    match none are left out — check len() against the input.
    """
    dp = {r["yahoo_id"]: r["sleeper_id"] for r in ff_player_ids()
          if r["yahoo_id"] and r["sleeper_id"]}
    players = sleeper_players()
    by_yahoo = {str(p["yahoo_id"]): pid for pid, p in players.items() if p.get("yahoo_id")}
    by_name = {}
    for pid, p in players.items():
        key = (_norm_name(p.get("full_name")), p.get("position"), p.get("team"))
        by_name.setdefault(key, []).append(pid)

    out = {}
    for rec in records:
        yid = str(rec.get("yahoo_id") or "")
        if rec.get("pos") == "DEF":
            out[yid] = rec["team"]
        elif yid in dp:
            out[yid] = dp[yid]
        elif yid in by_yahoo:
            out[yid] = by_yahoo[yid]
        else:
            hits = by_name.get((_norm_name(rec.get("name")), rec.get("pos"), rec.get("team")), [])
            if len(hits) == 1:
                out[yid] = hits[0]
    return out


# --------------------------------------------------------------------------
# ffopportunity expected points — no auth
# --------------------------------------------------------------------------

def expected_points(season, week=None, max_age_hours=24):
    """Actual vs expected fantasy output per player-week, from play-by-play.

    `*_exp` columns are what an average player would have produced with the
    same opportunities; `*_diff` is actual minus expected. A big positive
    total_fantasy_points_diff is usually TD luck that won't repeat; high
    total_fantasy_points_exp is earned volume. player_id is the gsis_id (join
    via sleeper_players()). Points are generic PPR, not league scoring — use
    them for comparison, not as projections. Updated after games are played.
    """
    url = f"{FFOPP_BASE}/ep_weekly_{season}.csv"
    text, _ = cached_get(url, f"ffopp_ep_weekly_{season}.csv", max_age_hours)
    rows = list(csv.DictReader(io.StringIO(text)))
    if week is not None:
        rows = [r for r in rows if str(r.get("week")) == str(week)]
    return rows


# --------------------------------------------------------------------------
# ESPN scoreboard — no auth: betting lines, kickoff, venue
# --------------------------------------------------------------------------

_ESPN_TEAM = {"WSH": "WAS"}  # ESPN abbreviations that differ from Yahoo/Sleeper


def nfl_games(season, week, max_age_hours=6):
    """One record per game: kickoff (UTC), teams, venue, spread and implied totals.

    Lines are ESPN's listed book (DraftKings as of 2026-09-25). spread_home is
    from the home team's view (negative = home favored). Implied team total =
    (total - spread_home) / 2 for home, (total + spread_home) / 2 for away —
    the market's expected points for each offense, the best single matchup
    signal for streaming QB, K and DEF. Line fields are None when no line is
    posted yet.
    """
    url = f"{ESPN_SCOREBOARD}?week={week}&seasontype=2&dates={season}"
    text, _ = cached_get(url, f"espn_scoreboard_{season}_w{week}.json", max_age_hours)
    games = []
    for event in json.loads(text).get("events", []):
        comp = event["competitions"][0]
        teams = {c["homeAway"]: _ESPN_TEAM.get(c["team"]["abbreviation"], c["team"]["abbreviation"])
                 for c in comp["competitors"]}
        venue = comp.get("venue") or {}
        address = venue.get("address") or {}
        odds = (comp.get("odds") or [{}])[0]
        total, spread = odds.get("overUnder"), odds.get("spread")
        implied = (None, None)
        if total is not None and spread is not None:
            implied = ((total - spread) / 2, (total + spread) / 2)
        games.append({
            "game_id": event["id"],
            "kickoff": event.get("date"),
            "home": teams.get("home"),
            "away": teams.get("away"),
            "spread_home": spread,
            "total": total,
            "implied_home": implied[0],
            "implied_away": implied[1],
            "book": (odds.get("provider") or {}).get("name"),
            "venue": venue.get("fullName"),
            "city": address.get("city"),
            "state": address.get("state"),
            "country": address.get("country"),
            "indoor": venue.get("indoor"),
        })
    if not games:
        raise SourceError(f"ESPN returned no games for {season} week {week}")
    return games


def implied_totals(season, week, max_age_hours=6):
    """{team: implied points} for every team with a posted line."""
    out = {}
    for g in nfl_games(season, week, max_age_hours):
        if g["implied_home"] is not None:
            out[g["home"]] = g["implied_home"]
            out[g["away"]] = g["implied_away"]
    return out


# --------------------------------------------------------------------------
# Open-Meteo weather — no auth
# --------------------------------------------------------------------------

_US_STATES = {  # states with an NFL venue; extend if a game lands elsewhere
    "AL": "Alabama", "AZ": "Arizona", "CA": "California", "CO": "Colorado",
    "FL": "Florida", "GA": "Georgia", "IL": "Illinois", "IN": "Indiana",
    "LA": "Louisiana", "MA": "Massachusetts", "MD": "Maryland", "MI": "Michigan",
    "MN": "Minnesota", "MO": "Missouri", "NC": "North Carolina", "NJ": "New Jersey",
    "NV": "Nevada", "NY": "New York", "OH": "Ohio", "PA": "Pennsylvania",
    "TN": "Tennessee", "TX": "Texas", "WA": "Washington", "WI": "Wisconsin",
}


def _geocode(city, state, country):
    """(lat, lon) for a venue city. Cached for a year — stadiums don't move."""
    params = f"name={requests.utils.quote(city)}&count=10"
    if country == "USA":
        params += "&countryCode=US"
    slug = re.sub(r"[^a-z0-9]+", "_", f"{city}_{state or country}".lower())
    text, _ = cached_get(f"{GEOCODE_URL}?{params}", f"geo_{slug}.json", 24 * 365)
    results = json.loads(text).get("results") or []
    if country == "USA":
        results = [r for r in results if r.get("admin1") == _US_STATES.get(state)]
    if not results:
        raise SourceError(f"could not geocode {city}, {state or country} — "
                          "add its state to _US_STATES in sources.py")
    return results[0]["latitude"], results[0]["longitude"]


def game_weather(season, week, max_age_hours=3):
    """Kickoff-hour forecast for every outdoor game: {game_id: {...}}.

    Fields: temp_f, wind_mph, gust_mph, precip_prob (%), precip_in. Sustained
    wind above ~15 mph is the threshold that measurably hurts kickers and deep
    passing; temperature alone rarely matters. Indoor games (ESPN's `indoor`
    flag, which may not reflect a retractable roof's state on the day) are
    skipped. Forecasts only reach 16 days ahead; later games get None.
    """
    out = {}
    for g in nfl_games(season, week):
        if g["indoor"] or not g["city"]:
            continue
        lat, lon = _geocode(g["city"], g["state"], g["country"])
        url = (f"{FORECAST_URL}?latitude={lat}&longitude={lon}"
               "&hourly=temperature_2m,wind_speed_10m,wind_gusts_10m,"
               "precipitation_probability,precipitation"
               "&temperature_unit=fahrenheit&wind_speed_unit=mph"
               "&precipitation_unit=inch&timezone=GMT&forecast_days=16")
        text, _ = cached_get(url, f"weather_{lat:.2f}_{lon:.2f}.json", max_age_hours)
        hourly = json.loads(text).get("hourly") or {}
        hour = (g["kickoff"] or "")[:13] + ":00"  # 2026-10-02T00:15Z -> 2026-10-02T00:00
        times = hourly.get("time") or []
        if hour not in times:
            out[g["game_id"]] = None
            continue
        i = times.index(hour)
        out[g["game_id"]] = {
            "game": f"{g['away']} @ {g['home']}",
            "kickoff": g["kickoff"],
            "temp_f": hourly["temperature_2m"][i],
            "wind_mph": hourly["wind_speed_10m"][i],
            "gust_mph": hourly["wind_gusts_10m"][i],
            "precip_prob": hourly["precipitation_probability"][i],
            "precip_in": hourly["precipitation"][i],
        }
    return out


# --------------------------------------------------------------------------
# QBERT (Nate Silver, Silver Bulletin) — no auth for the free preview
# --------------------------------------------------------------------------
#
# The post is paid, but Substack's API serves the free preview, which embeds
# the current-season ratings as a Datawrapper chart. Datawrapper publishes each
# chart's data at dwcdn.net/<id>/<version>/dataset.csv. The version bumps on
# every republish, so it is read from the post each time rather than pinned.
# The paywalled half of the post (projections, spread impacts) is not reachable.
# Personal use only — don't republish the data.

def qbert(max_age_hours=24):
    """Current-season QBERT ratings: {"meta": {...}, "players": [...]}.

    Player rows: team, player, qbert, adj_qbert, est_plays, war. Name + team
    only, no IDs — about 32 QBs, so match on name + team.
    """
    ua = {"User-Agent": "Mozilla/5.0"}
    text, _ = cached_get(f"{SILVER_API}/archive?search=QBERT&limit=10",
                         "qbert_archive.json", max_age_hours, headers=ua)
    posts = sorted((p for p in json.loads(text) if p.get("slug", "").startswith("qbert")),
                   key=lambda p: p["post_date"], reverse=True)
    if not posts:
        raise SourceError("no QBERT post found in the Silver Bulletin archive")
    slug = posts[0]["slug"]
    text, _ = cached_get(f"{SILVER_API}/posts/{slug}", f"qbert_post_{slug}.json",
                         max_age_hours, headers=ua)
    post = json.loads(text)

    charts = dict.fromkeys(re.findall(r"datawrapper\.dwcdn\.net/(\w+)/(\d+)/",
                                      post.get("body_html") or ""))
    for chart_id, version in charts:
        # A chart version is immutable, so its CSV never needs re-fetching.
        csv_text, _ = cached_get(f"{DATAWRAPPER_BASE}/{chart_id}/{version}/dataset.csv",
                                 f"datawrapper_{chart_id}_v{version}.csv", 24 * 365)
        rows = list(csv.DictReader(io.StringIO(csv_text)))
        if rows and {"team", "player", "qbert"} <= set(rows[0]):
            players = []
            for row in rows:
                rec = {k: re.sub(r"<[^>]+>", "", v).strip() for k, v in row.items()}
                for k in ("qbert", "adj_qbert", "est_plays", "war"):
                    try:
                        rec[k] = float(rec[k])
                    except (KeyError, ValueError):
                        pass
                players.append(rec)
            return {
                "meta": {
                    "source": post.get("canonical_url"),
                    "title": post.get("title"),
                    "post_date": post.get("post_date"),
                    "chart": f"{DATAWRAPPER_BASE}/{chart_id}/{version}/",
                },
                "players": players,
            }
    raise SourceError(f"no current-season ratings table in {slug} "
                      f"(checked {len(charts)} Datawrapper charts) — layout or paywall changed?")


# --------------------------------------------------------------------------
# cache maintenance
# --------------------------------------------------------------------------
#
# Every fetch takes max_age_hours. Passing 0 forces a re-fetch, which is all
# "refreshing" means here — there is no separate invalidation step.

# name -> (fetcher, default TTL hours, what it is)
REFRESHERS = {
    "sleeper-players":  (lambda a: sleeper_players(max_age_hours=a), 24,
                         "player dump: IDs, positions, injury_status, depth chart"),
    "sleeper-trending": (lambda a: sleeper_trending(max_age_hours=a), 3,
                         "league-wide waiver adds"),
    "injuries":         (lambda a: nfl_injuries(2026, max_age_hours=a), 6,
                         "nflverse weekly injury report"),
    "depth-charts":     (lambda a: nflverse_csv("depth_charts", "depth_charts_2026.csv", a), 12,
                         "nflverse depth charts"),
    "rosters":          (lambda a: nflverse_csv("weekly_rosters", "roster_weekly_2026.csv", a), 12,
                         "nflverse weekly rosters"),
    "fp-rankings":      (lambda a: consensus_rankings(2026, week=current_week(), max_age_hours=a), 6,
                         "FantasyPros ECR (top 10/position only)"),
    "sleeper-projections": (lambda a: sleeper_projections(2026, current_week(), max_age_hours=a), 6,
                            "weekly projections, all players, league-scored"),
    "player-ids":       (lambda a: ff_player_ids(max_age_hours=a), 24 * 7,
                         "DynastyProcess yahoo/sleeper/gsis ID crosswalk"),
    "expected-points":  (lambda a: expected_points(2026, max_age_hours=a), 24,
                         "ffopportunity actual vs expected points"),
    "lines":            (lambda a: nfl_games(2026, current_week(), max_age_hours=a), 6,
                         "ESPN spreads, totals, implied team totals"),
    "weather":          (lambda a: game_weather(2026, current_week(), max_age_hours=a), 3,
                         "Open-Meteo kickoff forecast, outdoor games"),
    "qbert":            (lambda a: qbert(max_age_hours=a)["players"], 24,
                         "Silver Bulletin QBERT QB ratings"),
}


def cache_status():
    """List cached files with their age. Stale is not wrong — just old."""
    if not os.path.isdir(CACHE_DIR):
        print("  cache/ does not exist yet — nothing fetched")
        return
    files = sorted(os.listdir(CACHE_DIR))
    if not files:
        print("  cache/ is empty")
        return
    width = max(len(f) for f in files)
    total = 0
    for name in files:
        path = os.path.join(CACHE_DIR, name)
        size = os.path.getsize(path)
        total += size
        age = (time.time() - os.path.getmtime(path)) / 3600
        age_str = f"{age:.1f}h" if age < 48 else f"{age / 24:.1f}d"
        print(f"  {name:<{width}}  {size / 1024:>8.0f} KB  {age_str:>6} old")
    print(f"\n  {len(files)} files, {total / 1e6:.1f} MB total")


def refresh(names=None):
    """Force re-fetch. No names = everything in REFRESHERS."""
    targets = names or list(REFRESHERS)
    unknown = [n for n in targets if n not in REFRESHERS]
    if unknown:
        raise SourceError(
            f"unknown target(s): {', '.join(unknown)}. "
            f"Known: {', '.join(REFRESHERS)}"
        )
    for name in targets:
        fetch, _ttl, desc = REFRESHERS[name]
        try:
            result = fetch(0)  # age 0 forces a re-fetch
            size = len(result) if hasattr(result, "__len__") else "?"
            print(f"  ok    {name:<18} {size} records   ({desc})")
        except SourceError as exc:
            print(f"  FAIL  {name:<18} {exc}")


# --------------------------------------------------------------------------
# CLI
# --------------------------------------------------------------------------

def check():
    print("\nSource health check\n" + "=" * 19)

    print("\nSleeper")
    try:
        trend = sleeper_trending(limit=3)
        print(f"  ok   trending adds        {len(trend)} rows")
        players = sleeper_players()
        print(f"  ok   player dump          {len(players):,} players")
    except SourceError as exc:
        print(f"  FAIL {exc}")

    print("\nnflverse")
    for release, fname in (
        ("injuries", "injuries_2026.csv"),
        ("depth_charts", "depth_charts_2026.csv"),
        ("weekly_rosters", "roster_weekly_2026.csv"),
        ("stats_player", "stats_player_week_2026.csv"),
    ):
        try:
            rows = nflverse_csv(release, fname)
            print(f"  ok   {fname:<30} {len(rows):>6} rows")
        except SourceError as exc:
            note = "not published yet" if "404" in str(exc) else str(exc)[:60]
            print(f"  --   {fname:<30} {note}")

    print("\nFantasyPros")
    try:
        week = current_week()
        data = consensus_rankings(2026, week=week)
        print(f"  ok   consensus rankings    week {week}, {len(data.get('players', []))} players")
    except SourceError as exc:
        print(f"  FAIL {exc}")

    print("\nOther")
    week = current_week()
    for label, fetch in (
        (f"sleeper projections w{week}", lambda: sleeper_projections(2026, week)),
        ("player-id crosswalk", ff_player_ids),
        ("expected points", lambda: expected_points(2026)),
        (f"ESPN lines w{week}", lambda: nfl_games(2026, week)),
        (f"weather w{week}", lambda: game_weather(2026, week)),
        ("QBERT", lambda: qbert()["players"]),
    ):
        try:
            print(f"  ok   {label:<26} {len(fetch()):>6} rows")
        except (SourceError, requests.RequestException) as exc:
            print(f"  FAIL {label:<26} {str(exc)[:80]}")
    print()


def print_games(week):
    """Lines, implied totals and kickoff weather for a week, lowest total first."""
    games = nfl_games(2026, week)
    weather = game_weather(2026, week)
    book = next((g["book"] for g in games if g["book"]), None)
    print(f"\nWeek {week} — implied points (book: {book})\n")
    for g in sorted(games, key=lambda g: g["total"] or 0):
        if g["total"] is None:
            line = f"{g['away']} @ {g['home']}: no line (played, or not posted)"
        else:
            line = (f"{g['away']:>3} {g['implied_away']:4.1f}  @ {g['home']:<3} {g['implied_home']:4.1f}"
                    f"   total {g['total']:4.1f}  spread(home) {g['spread_home']:+.1f}")
        w = weather.get(g["game_id"])
        if g["indoor"]:
            wx = "indoor"
        elif w:
            wx = f"{w['temp_f']:.0f}F wind {w['wind_mph']:.0f} (gust {w['gust_mph']:.0f}) rain {w['precip_prob']}%"
        else:
            wx = "no forecast yet"
        print(f"  {line}   {wx}")
    print()


def main():
    cmd = sys.argv[1] if len(sys.argv) > 1 else "check"
    if cmd == "check":
        check()
    elif cmd == "cache":
        cache_status()
    elif cmd == "refresh":
        refresh(sys.argv[2:] or None)
    elif cmd == "trending":
        for row in trending_named(limit=15):
            inj = f"  [{row['injury_status']}]" if row["injury_status"] else ""
            print(f"  {row['count']:>9,}  {row['name']:<24} {row['pos'] or '?':<3} "
                  f"{row['team'] or 'FA':<4}{inj}")
    elif cmd == "games":
        print_games(int(sys.argv[2]) if len(sys.argv) > 2 else current_week())
    elif cmd == "qbert":
        data = qbert()
        print(f"\n{data['meta']['title']} ({data['meta']['post_date'][:10]})\n{data['meta']['source']}\n")
        for i, p in enumerate(data["players"], 1):
            print(f"  {i:>2}. {p['player']:<24} {p['team']:<4} QBERT {p['qbert']:>6}  WAR {p['war']}")
        print()
    else:
        print(__doc__)


if __name__ == "__main__":
    main()

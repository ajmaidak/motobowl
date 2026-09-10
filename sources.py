#!/usr/bin/env python3
"""Clients for the three external data sources.

    Sleeper      free, no auth. Player dump (canonical IDs, positions, injury
                 status, depth chart), waiver trends, weekly stats.
    nflverse     free, no auth. Flat CSV/parquet released on GitHub — weekly
                 stats, snap counts, depth charts, injuries, rosters, pbp.
    FantasyPros  API key required (valid). Projections and 2025 consensus
                 rankings. Free tier caps results at top 10 per position.

Everything is cached under cache/ (gitignored) with an age check, so repeated
calls in a week don't re-download. Sleeper's player dump alone is ~14MB.

    python3 sources.py check          # health-check all three
    python3 sources.py cache          # what is cached and how old
    python3 sources.py refresh        # force re-fetch everything
    python3 sources.py refresh injuries sleeper-trending
    python3 sources.py trending       # top waiver adds right now
"""

import csv
import io
import json
import os
import sys
import time

import requests

HERE = os.path.dirname(os.path.abspath(__file__))
CACHE_DIR = os.path.join(HERE, "cache")
CREDS_FILE = os.path.join(HERE, ".credentials.json")

SLEEPER_BASE = "https://api.sleeper.app/v1"
NFLVERSE_BASE = "https://github.com/nflverse/nflverse-data/releases/download"
FANTASYPROS_BASE = "https://api.fantasypros.com/public/v2/json"


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


def consensus_rankings(season, week=None, position="ALL", scoring="PPR"):
    """Expert consensus rankings (ECR) with tiers. Weekly if week is given."""
    params = {"position": position, "scoring": scoring}
    params["type"] = "weekly" if week else "draft"
    if week:
        params["week"] = week
    return fantasypros(f"nfl/{season}/consensus-rankings", **params)


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
    "fp-rankings":      (lambda a: consensus_rankings(2026, week=1), 6,
                         "FantasyPros ECR (top 10/position only)"),
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
        data = consensus_rankings(2026, week=1)
        print(f"  ok   consensus rankings    {len(data.get('players', []))} players")
    except SourceError as exc:
        print(f"  FAIL {exc}")
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
    else:
        print(__doc__)


if __name__ == "__main__":
    main()

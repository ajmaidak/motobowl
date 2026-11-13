# CLAUDE.md

Orientation for an agent picking up this project cold. Read this before touching
`data/` or writing anything that consumes league data.

## What this project is

A personal fantasy football assistant for **one** Yahoo league: **Moto Bowl**,
league ID `130450`, my team ID `9`. The team name is "Team Auto Pick", but the
roster was drafted by Claude Fable, not by Yahoo autodraft. It has soft spots.
The project reads league data and recommends waiver pickups and weekly lineups.

**All roster moves are made by hand in the Yahoo app.** The Yahoo API is
read-only, and no code here should attempt writes. Recommend, don't execute.

## Status, 2026-11-12

Check this table before trusting anything below. Update the date when it changes.

| Thing | State | Note |
|---|---|---|
| Yahoo web session (`yahoo_web.py`) | **Active, the only league data source** | Cookie in `.yahoo-cookie`. Re-copy when a fetch hits a login redirect |
| Yahoo Fantasy API (`yahoo_api.py`, `roster.py`) | **Blocked.** Every call 403s | Waiting on Yahoo since 2026-09-25. History: `docs/yahoo-api-history.md` |
| `.credentials.json` | **Absent in this checkout** | Holds Yahoo app and FantasyPros keys when present. Gitignored |
| FantasyPros | **Unusable here** (no key) | Free tier only covers the top 10 per position anyway |
| QBERT (`qbert()`) | **Broken**, parse error on 2026-11-07 | Silver Bulletin changed the post layout. Fix or skip |
| Sleeper, nflverse, ffopportunity, ESPN lines, Open-Meteo | Working | See "External data sources" |
| `weeks/week-09.md` After | Filled 2026-11-12 | Lost 96–110. `week-10.md` After waits for Mon Nov 16 |

## League data: the Yahoo web session

```bash
.venv/bin/python yahoo_web.py check      # is the cookie still logged in?
.venv/bin/python yahoo_web.py sync 9     # fetch + parse -> data/my-roster.json,
                                         #   data/opponent-roster.json, data/free-agents.json
.venv/bin/python lineup_check.py         # starters that score 0 unless changed
```

`yahoo_web.py` GETs the same pages the browser shows, authenticated with the
browser's session cookie in `.yahoo-cookie` (gitignored; it is a full account
credential; never print, log or commit it). Raw HTML caches to `cache/yahoo/`.
`parse_yahoo_html.py` turns it into player records plus `yahoo_id`, `opp_rank`
and a `stats` dict keyed by column title.

* Free agents come from `status=A` (free agents **and** waivers; check
  `roster_status`, e.g. `W (Sep 19)`), in the `Week N (proj)` stat view, sorted
  by projection, top 50 per position. `sync` refuses to write if a page came
  back in any other stat view, so `proj_pts` there is a real weekly projection.
* When the cookie expires, fetches fail loudly (login redirect). Re-copy the
  cookie per the docstring at the top of `yahoo_web.py`. Never ask for it in chat.
* Scraping is against Yahoo's ToS. Retire it once the API works.

### Other pages the logs use

These go through `fetch(url, cache_name)` in `yahoo_web.py`. `BASE` is
`https://football.fantasysports.yahoo.com/f1/130450`.

| Page | URL | Used for |
|---|---|---|
| My roster, a past week | `roster_url(week)` → `BASE/9?week=W` | Actual points per player (`fan_pts`), the After section |
| My matchup | `fetch_matchup(week)` → `BASE/matchup?week=W&mid1=9` | Both lineups with `proj_pts` and `fan_pts`, `fan_total` per side |
| Any team's matchup | `BASE/matchup?week=W&mid1=T` | League-wide scoring studies (`research/season/`) |
| Transactions | `BASE/transactions?transactionsfilter=all&mid=9` | Add/drop history (`weeks/add-drop-review-*.md`) |
| Trade | `BASE/viewtrade?trid=N` | A pending trade offer |
| Scoreboard | `BASE/scoreboard?week=W` | All matchups in a week |

`parse_matchup()` returns `{'me', 'opponent'}`, each with `meta.fan_total` and
per-player `fan_pts`. Those are the official league scores.

## Where the league data lives

Parsed, normalized JSON in `data/`. **Read these**:

| File | Contents | Made by |
|---|---|---|
| `data/my-roster.json` | `{meta: {team_name, week, source, fetched}, players}` | `yahoo_web.py sync WEEK` |
| `data/opponent-roster.json` | This week's opponent, same shape plus `proj_total` | `yahoo_web.py sync WEEK` |
| `data/free-agents.json` | Top 50 available per position, week projections | `yahoo_web.py sync WEEK` |
| `data/league-settings.json` | Scoring rules, roster slots, waiver config | `parse_settings.py` |

Always check `meta.week` and `meta.fetched` before trusting a file for the
current week.

The one remaining paste is `data/league-settings.txt` (Scoring & Settings page),
which rarely changes. Regenerate its JSON with:

```bash
.venv/bin/python parse_settings.py data/league-settings.txt --json data/league-settings.json
```

Player records are normalized to: `slot, name, team, pos, opponent, home,
kickoff, bye, fan_pts, proj_pts, proj_max, proj_min, pos_rank, pct_start,
pct_rostered`, plus `yahoo_id`, `status` (injury designation), `opp_rank`
and `stats`. `roster.py` emits roughly this same shape from the API, so
recommendation code should work against either source.

`parse_yahoo_html.py` anchors game cells on the trailing `vs/@ TEAM`, because
the prefix varies by state: `Sun 3:25 pm vs GB` scheduled, `Q4 1:21, 13-10 vs
NE` live, `W 20-17 @ NE` final.

### Record states that matter

| State | How it looks in the record |
|---|---|
| Scheduled | `kickoff` = `"Sun 12:00 pm"`, `fan_pts` = `None` |
| **Locked** (game started or final) | `kickoff` = `None`, `opponent` set, `fan_pts` filled |
| Bye | `kickoff` = `None`, `opponent` = `None` |

## External data sources

`sources.py` wraps these sources. Everything caches under `cache/` (gitignored,
~60MB) with an age check. Don't re-download inside a week.

```bash
.venv/bin/python sources.py check      # health-check every source
.venv/bin/python sources.py trending   # league-wide waiver adds, named
.venv/bin/python sources.py games      # lines, implied team totals, kickoff weather
.venv/bin/python sources.py qbert      # Silver Bulletin QB ratings (broken, see Status)
```

| Source | Auth | What it's for |
|---|---|---|
| **Sleeper** | none | Player dump (12k players), `injury_status`, waiver trends, weekly stats |
| **Sleeper projections** | none | Weekly projections for *every* player (Rotowire), scored under league rules (`league_pts`) |
| **nflverse** | none | Injuries, depth charts, rosters, snaps, stats, pbp |
| **DynastyProcess IDs** | none | Yahoo ↔ Sleeper ↔ gsis ID crosswalk (`yahoo_to_sleeper()`) |
| **ffopportunity** | none | Expected fantasy points (xFP) from pbp. TD luck vs earned volume |
| **ESPN scoreboard** | none | Spreads, totals, implied team totals, venues |
| **Open-Meteo** | none | Kickoff-hour wind/rain for outdoor games |
| **FantasyPros** | API key | Projections and ECR. Free tier: top 10 per position. No key in this checkout |
| **QBERT** | none | Nate Silver's QB ratings. Parser broken as of 2026-11-07 |

**Sleeper projections are the default projection source**: full coverage, and
`league_points()` scores the raw components with `data/league-settings.json`
(6-pt pass TDs, -2 INTs), which Sleeper's own `pts_ppr` gets wrong for QBs. A
rostered player **missing** from the projections usually means he's not
expected to play (bye, or ruled out). Check his status rather than treating it
as a data gap. `league_scoring()` raises on a scoring rule it can't map, so a
settings change can't silently zero out a stat.

**Sleeper player IDs are the canonical join key.** Records carry `gsis_id`
(joins nflverse), `espn_id`, `yahoo_id` and `fantasy_data_id`, so map other
sources onto Sleeper rather than matching on player names. Names collide and
punctuation varies ("Marvin Harrison Jr." vs "Marvin Harrison Jr").

**FantasyPros, when a key exists:** the free tier caps results at the top 10
per position (`public_api_limited: true`) while `count` reports the full field.
That covers the locked-in starters and none of the bench players a flex call
turns on. Check membership before relying on it. The key can 403 on every
endpoint for ~15 minutes after first use; retry before concluding it is broken.
Ignore the top-level `scoring` field (always `STD`); compute league points from
the per-player components.

**nflverse:** files appear only once there's data in them, so a 404 early in a
season is expected. `injuries_{season}.csv` fills in through the practice week.
Check row counts before reading an empty result as "nobody is hurt".

### Refreshing the cache

Everything fetched lands in `cache/` and is reused until it ages past a
per-source TTL. Refreshing is a re-fetch; there is no separate invalidation step.

```bash
.venv/bin/python sources.py cache      # what's cached, how big, how old
.venv/bin/python sources.py refresh    # force re-fetch everything
.venv/bin/python sources.py refresh injuries sleeper-trending
```

Targets: `sleeper-players`, `sleeper-trending`, `injuries`, `depth-charts`,
`rosters`, `fp-rankings`, `sleeper-projections`, `player-ids`,
`expected-points`, `lines`, `weather`, `qbert`. In code, any fetcher takes
`max_age_hours=0` to force a re-fetch.

| Source | TTL | Refresh when |
|---|---|---|
| `sleeper-trending` | 3h | Before any waiver decision. It moves hourly |
| `injuries` | 6h | **Before every lineup decision**, and again near kickoff |
| `fp-rankings` | 6h | Before lineup decisions; after significant news |
| `depth-charts` | 12h | Weekly, or after a reported role change |
| `rosters` | 12h | Weekly |
| `sleeper-players` | 24h | Weekly. It's 14MB, don't churn it |
| `sleeper-projections` | 6h | Before lineup and waiver decisions |
| `lines` | 6h | Before streaming QB/K/DEF; lines move through the week |
| `weather` | 3h | Near kickoff. Forecasts beyond ~3 days are rough |
| `expected-points` | 24h | After each week's games (it's built from pbp) |
| `qbert` | 24h | Weekly; the post is republished in place |
| `player-ids` | 7d | Weekly; rookies lag, name fallback covers them |

**The TTL is a ceiling, not permission.** Availability news breaks continuously
and inactives land ~90 minutes before kickoff, so a 5-hour-old injury file is
inside its TTL and still capable of being wrong about who plays. Before a
lineup that locks soon, refresh `injuries` explicitly, and state the age of what
was used if it could change the call.

Stats files are the opposite case: `stats_player_week_{season}` only has data
for completed weeks, so refresh those *after* the week completes, when filling
the `After` section of `weeks/week-NN.md`.

To wipe everything and start clean: `rm -rf cache/`. Nothing there is
irreplaceable. None of it is league ground truth (that's `data/`).

## Research cache

`research/week-NN/` caches external research (projections, injury reports,
matchup and beat-writer notes) behind each recommendation. `research/season/`
holds season-level studies (draft review, standings vs draft slot). Template:
`research/TEMPLATE.md`.

* **Every cached file records `source:` and `fetched:` in its header.** The
  weekly log grades reasoning after the fact, which only works if the inputs are
  still recoverable and attributable.
* **A web search that changes a call gets a file.** If a recommendation cites
  a report (a practice status, a beat-writer note, a trade rumor), write what it
  said and where it came from to `research/week-NN/`. Week 9 cited five
  searches and cached none; that cannot be graded later.
* **Availability research goes stale fast.** A Wednesday practice report is
  routinely wrong by Sunday; inactives land ~90 minutes before kickoff. Treat
  anything about who is playing as stale after ~24 hours.
* Keep it separate from `data/`: `data/` is ground truth about the league,
  `research/` is outside opinion about players.

## Start/sit analysis

The full procedure lives in the `start-sit` skill
(`.claude/skills/start-sit/SKILL.md`), invocable as `/start-sit`. It covers the
grade-last-week → refresh → zero check → read roster → availability → score →
recommend → log sequence, plus the judgment rules. Follow it rather than
improvising a lineup analysis.

`weeks/LESSONS.md` holds every rule the weekly log has produced, with its
origin week and a running tally. Read it before recommending anything.

## Weekly outcome log

`weeks/` holds one file per week: `week-NN.md`, started from `weeks/TEMPLATE.md`.

**Fill the `Before` section when setting a lineup, and the `After` section once
the games finish.** This is how the quality of the advice gets measured. The
`week-review` skill (`/week-review`) fills `After`. Two things make the log
worth keeping:

* **Record the counterfactual.** What the benched alternative actually scored,
  not just the final score. Win/loss alone can't distinguish good process from
  luck; a week can be won on bad calls and lost on good ones.
* **Record reasoning at decision time**, before the outcome is known, and log
  misses in the same detail as hits. Reasoning reconstructed afterward is
  contaminated by hindsight, and a log of only the wins is worthless.

Also note when a recommendation was *not* followed, and why.

`weeks/scorecard.md` aggregates every graded call by type. Update it when an
`After` section is filled. `weeks/LESSONS.md` is where "Anything to change"
items go once written; a lesson that only lives in one week's file is lost.

## League rules that actually change recommendations

Read `data/league-settings.json` for the full set, but these are the ones that
bite. The first three are **overrides of Yahoo defaults**; don't assume standard:

* **Full PPR**: 1.0 per reception (Yahoo default is 0.5). Favors high-target
  possession receivers over TD-dependent or committee players.
* **6-point passing TDs** and **-2 interceptions** (defaults 4 and -1). Inflates
  QB value; punishes volatile QBs harder than usual.
* **No fractional points**: everything rounds to whole numbers, so sub-point
  projection gaps are noise, not signal. Don't split hairs over 1 point.
* Starters: `QB, WR, WR, WR, RB, RB, TE, W/R/T, K, DEF` + 6 bench.
* **Unlimited acquisitions**, continual rolling waivers, 2-day period, weekly
  waivers run Tuesday game time. No scarcity cost to churning the bench, so
  streaming is cheap and viable.
* **Locks are per player, at his game's kickoff.** A locked player cannot be
  moved out of his slot or dropped until the next week starts. A starter on
  IR or Out whose game locks on Thursday scores 0 for the week, and nothing can
  fix it after kickoff. Week 9: Lamar Jackson (IR) locked at QB on Thursday.
  `lineup_check.py` finds this.
* **A free agent goes on waivers when his game kicks off** (`Game Time -
  Tuesday`). A Sunday add for next week is a claim, not an instant add. Add
  before his kickoff if the player matters.
* **Trades**: the league votes, 2-day reject period, deadline Nov 28, 2026. A
  trade accepted this week processes for next week.

## Known gaps

* **Injury designations** come through as each player's `status` (`Q`, `D`,
  `O`, `IR`, `IR-R`, `PUP-R`, `PUP-P`, `NFI-R`, `SUSP`, `GTD`). Cross-check
  against Sleeper's `injury_status`. A sync is a point-in-time snapshot and
  designations change through the week.
* **Yahoo → Sleeper joins go through `yahoo_to_sleeper()`**: DEF → team
  abbreviation, then the DynastyProcess crosswalk, then Sleeper's own (sparse)
  `yahoo_id`, then a unique name + position + team match. Unmatched players are
  omitted, so compare counts.
* Snapshots are point-in-time. Check `meta.week` in `data/my-roster.json` before
  trusting it for the current week.
* NFL rosters/depth charts move constantly, and model knowledge of the 2026
  season is unreliable. Prefer what's in `data/` over recalled player facts, and
  say so when a claim rests on memory rather than the files.

## Conventions

* Python lives at `.venv/bin/python` (venv is gitignored; `pip install -r
  requirements.txt` to rebuild).
* `.credentials.json`, `.tokens.json` and `.yahoo-cookie` are gitignored and must
  never be committed. This repo is public.
* After any lineup or waiver recommendation, write it into the current
  `weeks/week-NN.md` before ending the turn.
* Parsers are defensive by design: Yahoo's page layout shifts between pages and
  seasons. When a parser can't make sense of input, fail loudly rather than
  silently emitting a partial roster.

# CLAUDE.md

Orientation for an agent picking up this project cold. Read this before touching
`data/` or writing anything that consumes league data.

## What this project is

A personal fantasy football assistant for **one** Yahoo league: **Moto Bowl**,
league ID `130450`, my team ID `9` (team name currently "Team Auto Pick").
It reads league data and recommends waiver pickups and weekly lineups.

**All roster moves are made by hand in the Yahoo app.** The Yahoo API is
read-only, and no code here should attempt writes. Recommend, don't execute.

## Two data sources — know which one you're on

Yahoo API access was approved 2026-09-16: agreement signed, app created (Confidential
Client, credentials in `.credentials.json`), confirmation form submitted. **Waiting
on Yahoo to provision** Fantasy Sports permissions on the app. A form auto-reply
quoted 1–2 weeks (so by ~2026-09-30); check the app's API Permissions page for
Fantasy Sports rather than waiting on email.
Until it is, league data comes from Yahoo's web pages via a logged-in session.

| Source | Status | Entry point |
|---|---|---|
| Yahoo web pages, logged-in session | **Active now** | `yahoo_web.py sync WEEK` |
| Yahoo Fantasy API | Approved, awaiting provisioning | `yahoo_api.py`, `roster.py` |

### Yahoo web session (replaces pasting)

```bash
.venv/bin/python yahoo_web.py check      # is the cookie still logged in?
.venv/bin/python yahoo_web.py sync 2     # fetch + parse -> data/my-roster.json,
                                         #   data/opponent-roster.json, data/free-agents.json
```

`yahoo_web.py` GETs the same pages the browser shows, authenticated with the
browser's session cookie in `.yahoo-cookie` (gitignored — it is a full account
credential; never print, log or commit it). Raw HTML caches to `cache/yahoo/`;
`parse_yahoo_html.py` turns it into the usual player records plus `yahoo_id`,
`opp_rank` and a `stats` dict keyed by column title. Verified 2026-09-16: zero
discrepancies against the (since deleted) paste parser on the week 2 roster (16 players, 13 fields).

* Free agents come from `status=A` (free agents **and** waivers — check
  `roster_status`, e.g. `W (Sep 19)`), in the `Week N (proj)` stat view, sorted
  by projection, top 50 per position. `sync` refuses to write if a page came
  back in any other stat view, so `proj_pts` there is a real weekly projection.
* When the cookie expires, fetches fail loudly (login redirect). Re-copy the
  cookie per the docstring at the top of `yahoo_web.py`.
* Stopgap only: scraping is against Yahoo's ToS. Retire it once the API works.

`roster.py` is written and its parsing is verified against a mock payload, but
it has **never run against the live API** — credentials exist, but access isn't provisioned yet. Treat its
response handling as unproven. When access lands, the first real call may need
fixes to the JSON shape assumptions in `yahoo_api.py`.

## Where the league data lives

Parsed, normalized JSON in `data/` — **read these**:

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

The roster/free-agent pastes were retired 2026-09-16 — they lost columns to
Yahoo's icon glyphs and game-state cells and often lacked weekly projections.
The paste parsers were deleted along with them. `parse_yahoo_html.py` anchors
game cells on the trailing `vs/@ TEAM`, because the prefix varies by state —
`Sun 3:25 pm vs GB` scheduled, `Q4 1:21, 13-10 vs NE` live, `W 20-17 @ NE` final.

The Yahoo API replaces the web session once approved.

Player records are normalized to: `slot, name, team, pos, opponent, home,
kickoff, bye, fan_pts, proj_pts, proj_max, proj_min, pos_rank, pct_start,
pct_rostered`, plus `yahoo_id`, `status` (injury designation), `opp_rank`
and `stats` from the web pages. `roster.py` emits roughly this same shape from the API, so
recommendation code should work against either source.

## External data sources

`sources.py` wraps three sources. Everything caches under `cache/` (gitignored,
~60MB) with an age check — don't re-download inside a week.

```bash
.venv/bin/python sources.py check      # health-check all three
.venv/bin/python sources.py trending   # league-wide waiver adds, named
```

| Source | Auth | Status | What it's for |
|---|---|---|---|
| **Sleeper** | none | working | Player dump (12k players), waiver trends, weekly stats |
| **nflverse** | none | working | Injuries, depth charts, rosters, snaps, stats, pbp |
| **FantasyPros** | API key | working, **free tier: top 10/position** | Projections with PPR points, consensus rankings (ECR) |

### Refreshing the cache

Everything fetched lands in `cache/` (gitignored, ~64MB) and is reused until it
ages past a per-source TTL. Refreshing is just a re-fetch — there is no separate
invalidation step.

```bash
.venv/bin/python sources.py cache      # what's cached, how big, how old
.venv/bin/python sources.py refresh    # force re-fetch everything
.venv/bin/python sources.py refresh injuries sleeper-trending
```

Targets: `sleeper-players`, `sleeper-trending`, `injuries`, `depth-charts`,
`rosters`, `fp-rankings`. In code, any fetcher takes `max_age_hours=0` to force
a re-fetch.

| Source | TTL | Refresh when |
|---|---|---|
| `sleeper-trending` | 3h | Before any waiver decision — it's a live signal and moves hourly |
| `injuries` | 6h | **Before every lineup decision**, and again near kickoff |
| `fp-rankings` | 6h | Before lineup decisions; after significant news |
| `depth-charts` | 12h | Weekly, or after a reported role change |
| `rosters` | 12h | Weekly |
| `sleeper-players` | 24h | Weekly — it's 14MB, don't churn it |

**The TTL is a ceiling, not permission.** Cached-and-fresh is not the same as
current: availability news breaks continuously and inactives land ~90 minutes
before kickoff, so a 5-hour-old injury file is inside its TTL and still capable
of being wrong about who plays. Before a lineup that locks soon, refresh
`injuries` explicitly rather than trusting the TTL, and state the age of what
was used if it could change the call.

Stats files are the opposite case — `stats_player_week_{season}` doesn't exist
until games are played, so refresh those *after* the week completes, when
filling in the `After` section of `weeks/week-NN.md`.

To wipe everything and start clean: `rm -rf cache/`. Nothing there is
irreplaceable — it's all re-fetchable, and none of it is league ground truth
(that's `data/`).

**Sleeper player IDs are the canonical join key.** Records carry `gsis_id`
(joins nflverse), `espn_id`, `yahoo_id` and `fantasy_data_id`, so map other
sources onto Sleeper rather than matching on player names — names collide and
punctuation varies ("Marvin Harrison Jr." vs "Marvin Harrison Jr").

**FantasyPros works — the key is valid.** One real limitation and one trap:

* **Free tier caps results at the top 10 per position** (`public_api_limited:
  true`), while `count` reports the full field (462 ranked players, 213 WRs).
  For this roster that covered 6 of 16 — and covered exactly the locked-in
  starters while missing *every* player involved in an actual start/sit call
  (Egbuka, Harrison, Sutton, Dowdle, Pittman, Shakir). **Do not assume
  FantasyPros can settle a bench decision; check membership first.** This is the
  binding constraint on using it for this league.
* **Transient 403s.** On first use the key 403'd on every endpoint for ~15
  minutes — indistinguishable from an invalid key — then started working with no
  change made. Retry before concluding a key or endpoint is broken. Re-verified
  clean afterward (12/12, 8/8), including with an `Origin` header.

Ignore the top-level `scoring` field in projections — it says `STD` regardless.
Per-player `stats` carry `points_ppr`, `points_half` and `points`, plus raw
components (`rec_rec`, `rec_yds`, `rush_*`, `fumbles`), so league-exact points
can be computed from components using `data/league-settings.json` rather than
trusting a prepackaged total.

**nflverse current-season caveats:** files appear only once there's data in
them, so a 404 early in a season is expected, not a bug (`stats_player_week_2026`
and `snap_counts_2026` are 404 as of week 1). More importantly,
`injuries_2026.csv` currently holds **29 rows covering two teams with blank
statuses** — it is a stub, not a usable injury report. Injury reports fill in
through the practice week, so check row counts before reading an empty result as
"nobody is hurt".

## Research cache

`research/week-NN/` caches external research (projections, injury reports,
matchup and beat-writer notes) behind each recommendation. Template:
`research/TEMPLATE.md`.

* **Every cached file records `source:` and `fetched:` in its header.** The
  weekly log grades reasoning after the fact, which only works if the inputs are
  still recoverable and attributable.
* **Availability research goes stale fast.** A Wednesday practice report is
  routinely wrong by Sunday; inactives land ~90 minutes before kickoff. Treat
  anything about who is playing as stale after ~24 hours and re-fetch near
  kickoff rather than trusting a cached copy.
* When a recommendation leans on cached research, state how old it is if the age
  could change the call.
* Keep it separate from `data/`: `data/` is ground truth about the league,
  `research/` is outside opinion about players.

## Start/sit analysis

The full procedure lives in the `start-sit` skill
(`.claude/skills/start-sit/SKILL.md`), invocable as `/start-sit`. It covers the
refresh → read roster → establish availability → score → recommend → log
sequence, plus the judgment rules that keep recommendations honest (default to
no change; separate what was read from what was recalled; name the uncertainty
but still commit to a lineup).

Follow it rather than improvising a lineup analysis.

## Weekly outcome log

`weeks/` holds one file per week: `week-NN.md`, started from `weeks/TEMPLATE.md`.

**Fill the `Before` section when setting a lineup, and the `After` section once
the games finish.** This is not optional bookkeeping — it is how the quality of
the advice gets measured. Two things make the log worth keeping:

* **Record the counterfactual.** What the benched alternative actually scored,
  not just the final score. Win/loss alone can't distinguish good process from
  luck; a week can be won on bad calls and lost on good ones.
* **Record reasoning at decision time**, before the outcome is known, and log
  misses in the same detail as hits. Reasoning reconstructed afterward is
  contaminated by hindsight, and a log of only the wins is worthless.

Also note when a recommendation was *not* followed, and why.

Before recommending anything, read the most recent completed week for what the
prior reasoning got wrong.

## League rules that actually change recommendations

Read `data/league-settings.json` for the full set, but these are the ones that
bite. All three are **overrides of Yahoo defaults** — don't assume standard:

* **Full PPR** — 1.0 per reception (Yahoo default is 0.5). Favors high-target
  possession receivers over TD-dependent or committee players.
* **6-point passing TDs** and **-2 interceptions** (defaults 4 and -1). Inflates
  QB value; punishes volatile QBs harder than usual.
* **No fractional points** — everything rounds to whole numbers, so sub-point
  projection gaps are noise, not signal. Don't split hairs over 1 point.
* Starters: `QB, WR, WR, WR, RB, RB, TE, W/R/T, K, DEF` + 6 bench.
* **Unlimited acquisitions**, continual rolling waivers, 2-day period, weekly
  waivers run Tuesday game time. No scarcity cost to churning the bench, so
  streaming is cheap and viable.

## Known gaps

* **Injury designations** come through as each player's `status` (`Q`, `D`,
  `O`, `IR`, `IR-R`, `PUP-R`, `PUP-P`, `NFI-R`, `SUSP`, `GTD`). Cross-check
  against Sleeper's `injury_status` — a sync is a point-in-time snapshot and
  designations change through the week.
* **Sleeper's `yahoo_id` is sparse** (5 of 16 roster players on 2026-09-16), so
  `yahoo_id` doesn't yet join Yahoo data to Sleeper reliably; fall back to
  name + team + position, or add an ID crosswalk.
* Snapshots are point-in-time. Check `meta.week` in `data/my-roster.json` before
  trusting it for the current week.
* NFL rosters/depth charts move constantly, and model knowledge of the 2026
  season is unreliable. Prefer what's in `data/` over recalled player facts, and
  say so when a claim rests on memory rather than the files.

## Conventions

* Python lives at `.venv/bin/python` (venv is gitignored; `pip install -r
  requirements.txt` to rebuild).
* `.credentials.json`, `.tokens.json` and `.yahoo-cookie` are gitignored and must never be
  committed — this repo is public.
* After any lineup or waiver recommendation, write it into the current
  `weeks/week-NN.md` before ending the turn.
* Parsers are defensive by design: Yahoo's page layout shifts between pages and
  seasons. When a parser can't make sense of input, fail loudly rather than
  silently emitting a partial roster.

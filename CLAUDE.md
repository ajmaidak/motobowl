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

Yahoo API access was applied for (see `application.md`) but **not yet granted**.
Until it is, everything runs off hand-pasted snapshots in `data/`.

| Source | Status | Entry point |
|---|---|---|
| Pasted snapshots in `data/` | **Active now** | `parse_roster.py`, `parse_settings.py` |
| Yahoo Fantasy API | Pending approval | `yahoo_api.py`, `roster.py` |

`roster.py` is written and its parsing is verified against a mock payload, but
it has **never run against the live API** — no credentials exist yet. Treat its
response handling as unproven. When access lands, the first real call may need
fixes to the JSON shape assumptions in `yahoo_api.py`.

## Where the league data lives

Raw pastes from the Yahoo web UI (ugly, one table cell per line — that's normal):

| File | Contents | State |
|---|---|---|
| `data/league-settings.txt` | Scoring & Settings page | populated |
| `data/my-roster.txt` | My Team page, week 1 | populated |
| `data/opponent-roster.txt` | This week's opponent | **empty** |
| `data/free-agent-*.txt` | Players → Free Agents, one file per position | def + mixed offense populated |

Parsed, normalized versions — **prefer these**, don't re-parse the raw text:

* `data/league-settings.json` — scoring rules, roster slots, waiver config
* `data/my-roster.json` — `{meta: {team_name, week}, players: [...]}`

Regenerate either with:

```bash
.venv/bin/python parse_settings.py data/league-settings.txt --json data/league-settings.json
.venv/bin/python parse_roster.py   data/my-roster.txt      --json data/my-roster.json
```

`parse_yahoo_table.py` is a **generic** parser for any Yahoo table paste — it
derives columns from the pasted header instead of hardcoding them, handles
multiple pages concatenated into one file, extracts injury designations, and
de-duplicates by name+team. Verified to produce identical output to
`parse_roster.py` on the roster paste (16 players, 8 fields, zero discrepancies).

Two paste quirks it handles, both of which silently corrupted columns before:

* **Private-use glyphs.** Yahoo's copy embeds icon characters like `\ue231` at
  the end of cells. They break any regex anchored to end-of-line.
* **Game cells vary by game state** — `Sun 3:25 pm vs GB` when scheduled,
  `Q4 1:21, 13-10 vs NE` in progress, `W 20-17 @ NE` when final. Matching only
  the scheduled form shifts every later column by one.

**Free agents are split one file per position** (`data/free-agent-qb.txt`,
`-rb`, `-wr`, `-te`, `-k`, `-def`), because Yahoo paginates at 25 rows and uses
a different column set per position group. Merge them with:

```bash
.venv/bin/python free_agents.py     # -> data/free-agents.json
```

Any `data/free-agent*.txt` is picked up; multiple pages go in one file back to
back. See `data/README.md` for the copy workflow.

**These pastes may have no `Proj Pts` column.** The default Yahoo Players view
shows season columns (`GP*`, `Fan Pts`, `Pos Rank`, `% Ros`) and no weekly
projection. When that's the case, ranking falls back to `% Ros`, which is a
market-consensus proxy and *not* a projection — say so rather than presenting it
as one. Ask for a re-paste with the weekly projection stat view if a decision
needs real projections.

The Yahoo API removes all of this once approved.

Player records are normalized to: `slot, name, team, pos, opponent, home,
kickoff, bye, fan_pts, proj_pts, proj_max, proj_min, pos_rank, pct_start,
pct_rostered`. `roster.py` emits roughly this same shape from the API, so
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

* **Injury designations ARE in the pastes** — corrected finding. Yahoo embeds
  them in the player detail line (`Zach CharbonnetPUP-RPlayer Note Sea - RB`),
  and `parse_yahoo_table.py` extracts them to a `status` field (`Q`, `D`, `O`,
  `IR`, `IR-R`, `PUP-R`, `PUP-P`, `NFI-R`, `SUSP`, `GTD`). The roster paste
  happened to contain no injured players, which is why this looked absent at
  first. Cross-check against Sleeper's `injury_status` anyway — a paste is a
  point-in-time snapshot and designations change through the week.
* Week 1 pastes have empty `fan_pts` and `pos_rank` (no games played yet).
* Snapshots are point-in-time. Check `meta.week` in `data/my-roster.json` before
  trusting it for the current week.
* NFL rosters/depth charts move constantly, and model knowledge of the 2026
  season is unreliable. Prefer what's in `data/` over recalled player facts, and
  say so when a claim rests on memory rather than the files.

## Conventions

* Python lives at `.venv/bin/python` (venv is gitignored; `pip install -r
  requirements.txt` to rebuild).
* `.credentials.json` and `.tokens.json` are gitignored and must never be
  committed — this repo is public.
* After any lineup or waiver recommendation, write it into the current
  `weeks/week-NN.md` before ending the turn.
* Parsers are defensive by design: Yahoo's paste layout shifts between pages and
  seasons. When a parser can't make sense of input, fail loudly rather than
  silently emitting a partial roster.

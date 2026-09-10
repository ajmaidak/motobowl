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
| `data/free-agents.txt` | Players → Free Agents | **empty** |

Parsed, normalized versions — **prefer these**, don't re-parse the raw text:

* `data/league-settings.json` — scoring rules, roster slots, waiver config
* `data/my-roster.json` — `{meta: {team_name, week}, players: [...]}`

Regenerate either with:

```bash
.venv/bin/python parse_settings.py data/league-settings.txt --json data/league-settings.json
.venv/bin/python parse_roster.py   data/my-roster.txt      --json data/my-roster.json
```

Player records are normalized to: `slot, name, team, pos, opponent, home,
kickoff, bye, fan_pts, proj_pts, proj_max, proj_min, pos_rank, pct_start,
pct_rostered`. `roster.py` emits roughly this same shape from the API, so
recommendation code should work against either source.

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

* **Injury designations are not in the pasted data.** The Yahoo copy includes
  "Player Note" markers but no Q/O/D/IR flags. If injury status matters to a
  recommendation, ask the user — do not infer it and do not assume healthy.
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
* Parsers are defensive by design: Yahoo's paste layout shifts between pages and
  seasons. When a parser can't make sense of input, fail loudly rather than
  silently emitting a partial roster.

---
name: start-sit
description: Refresh cached NFL data, read the league roster and settings, and recommend a starting lineup for the current week. Use when asked to set a lineup, decide start/sit, or review who to play this week in the Moto Bowl league.
---

# Start/Sit Analysis

Produce a starting-lineup recommendation for the Moto Bowl league, grounded in
the project's own data rather than recalled NFL knowledge.

Read `CLAUDE.md` first if it isn't already in context — league rules, data
locations and source caveats all live there and are assumed below.

## Procedure

### 1. Refresh what decays

```bash
.venv/bin/python sources.py refresh injuries sleeper-trending fp-rankings
.venv/bin/python sources.py cache
```

Note the age of what you're using. If the lineup locks within a few hours,
refresh `injuries` again immediately before recommending — inactives land ~90
minutes before kickoff and a file inside its TTL can still be wrong about who
plays.

### 2. Load the league's own data

* `data/my-roster.json` — roster, slots, Yahoo projections, matchups, byes
* `data/league-settings.json` — scoring rules and starting slots
* `data/free-agents.json` — every available player, by position, with injury
  status and % rostered
* `data/opponent-roster.json` — this week's opponent, if pasted

Check `meta.week` matches the week you're advising on. If the snapshot is from a
previous week, stop and ask for a fresh paste rather than advising on stale
data — this is the single most likely way to give confidently wrong advice.

Regenerate from raw pastes if needed:

```bash
.venv/bin/python parse_roster.py data/my-roster.txt --json data/my-roster.json
.venv/bin/python free_agents.py                      # -> data/free-agents.json
```

**Free agents are real options, not background.** The roster was auto-drafted
and has soft spots; a widely-rostered free agent can beat a current starter
outright. Load them every time, not only when asked about waivers.

**Know what you're ranking on.** These pastes often carry no `Proj Pts` column —
only season columns (`Fan Pts`, `Pos Rank`, `% Ros`). When that's the case,
`% Ros` is the fallback sort, and it is **market consensus, not a projection**.
Say so rather than presenting it as expected points, and ask for a re-paste with
Yahoo's weekly projection view if a decision genuinely turns on projected
scoring.

### 3. Establish availability

Three sources, in rough order of usefulness:

1. **The pastes themselves.** Yahoo embeds designations in the player detail
   line and `parse_yahoo_table.py` extracts them to a `status` field (`Q`, `D`,
   `O`, `IR`, `IR-R`, `PUP-R`, `PUP-P`, `NFI-R`, `SUSP`, `GTD`). Present in both
   roster and free-agent data. A paste is point-in-time, so check its age.
2. **Sleeper** `injury_status` per player (`sleeper_players()` in `sources.py`) —
   refreshes independently of the paste, so it's the cross-check.
3. **nflverse** `nfl_injuries(season, week)` — richest when populated (practice
   status, injury type), but the 2026 file has been a near-empty stub. Check the
   row count before reading an empty result as "nobody is hurt."

**Never recommend a player carrying `IR`, `IR-R`, `PUP-R`, `PUP-P` or `NFI-R`
as a starter** — they are ineligible to play, not merely risky. `Q`/`D`/`GTD`
are judgment calls; say which way you're leaning and why.

If no source has usable status for a player the decision hinges on, **say so and
ask** rather than assuming healthy.

### 4. Score the options

Use the league's actual scoring, not generic rankings. Full PPR, 6-point passing
TDs, -2 interceptions, **no fractional points**.

* FantasyPros projections carry `points_ppr` plus raw components, so
  league-exact points can be computed from components.
* Free tier only returns the **top 10 per position** — historically covering the
  obvious starters and *none* of the bench players a flex decision turns on.
  Check membership before relying on it; fall back to Yahoo projections in
  `data/my-roster.json`, which cover the whole roster.

### 5. Recommend

Fill every starting slot: `QB, WR, WR, WR, RB, RB, TE, W/R/T, K, DEF`.

For each change, give: the swap, the reason, and your confidence. Say plainly
when a call is close to a coin flip.

Then check the waiver wire against the weakest starting slots. Recommend an
add/drop only when the free agent clearly beats the current starter — the bar is
higher than a bench swap because it costs a roster spot. The league has
**unlimited acquisitions and continual rolling waivers**, so there's no scarcity
cost to churning, but that is a reason streaming is *viable*, not a reason to
churn for its own sake.

Flag anyone whose game locks earliest — a Thursday player must be added before
kickoff, and that deadline binds well before the Sunday lineup does.

### 6. Record it

Write the recommendation into `weeks/week-NN.md` **before** the games — the
reasoning is the part worth grading later, and it's worthless if reconstructed
after the outcome. Log recommendations that were not followed too.

## Judgment rules

**Default to no change.** Projections are noisy and the roster is already
reasonable. A swap needs a real edge, not a rounding artifact. With no
fractional points in this league, gaps under about 2 points are noise — do not
recommend churn to chase them.

**Separate what you read from what you recall.** Model knowledge of the 2026
season is unreliable, and player roles change constantly. Base recommendations
on `data/` and the cached sources; when something rests on recalled knowledge of
a player, say so explicitly so the user can discount it. Never invent a depth
chart position, snap share, or injury.

**Volume beats upside in full PPR.** A reception is a guaranteed point, so a
high-target possession receiver has a higher floor than a boom/bust deep threat
with the same projection. Weight target share accordingly — this is the most
common way generic advice goes wrong for this league.

**Name the uncertainty.** Every recommendation should be checkable: which source
said what, and how old it was. "Start X over Y" is not useful; "start X over Y —
Sleeper shows Y questionable as of 2h ago, and X has the higher floor in PPR" is.

**Don't hedge into uselessness.** After stating the uncertainty, still commit to
a specific lineup. The user needs a lineup, not a list of considerations.

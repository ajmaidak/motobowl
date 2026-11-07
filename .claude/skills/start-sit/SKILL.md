---
name: start-sit
description: Refresh cached NFL data, read the league roster and settings, and recommend a starting lineup for the current week. Use when asked to set a lineup, decide start/sit, or review who to play this week in the Moto Bowl league.
---

# Start/Sit Analysis

Produce a starting-lineup recommendation for the Moto Bowl league, grounded in
the project's own data rather than recalled NFL knowledge.

Read `CLAUDE.md` first if it isn't already in context. League rules, data
locations and source caveats all live there and are assumed below. Then read
`weeks/LESSONS.md`: every rule below that cites a number refers to it.

## Recommended model

**Opus 5.5 (`claude-opus-5-5`) at high effort.** Set 2026-09-25, held through
week 9. The log shows the misses were process (unexamined slots, a missed
lock), not reasoning, so there is no case for switching. Re-evaluate after
week 12 against `weeks/scorecard.md`. Step up to Fable 5.1 or max effort only
for a genuinely hard week: several questionable starters, an add/drop with a
real tradeoff, a trade offer. Record the model on the "Analysis by" line.

## Where the points are

Eight graded weeks say the advice earns its keep on **availability** (a
fallback for an Out or IR starter: +41 net) and loses it on **slots nobody
examined** (−44 net). Bench-tier WR3 and flex tiebreaks are coin flips (15
calls, net −10). Spend the effort in that order: steps 0–3 before step 4, and
state tiebreaks as coin flips rather than arguing them.

## Procedure

### 0. Grade last week

If the most recent completed week's `After` section is empty, run
`/week-review` first. If there is no time, say so in "What this was decided
on" and read that week's `Before` section anyway. Then read `weeks/LESSONS.md`
and any `weeks/*review*.md`.

### 1. Sync and run the zero check

```bash
.venv/bin/python yahoo_web.py sync WEEK   # -> my-roster, opponent-roster, free-agents .json
.venv/bin/python lineup_check.py          # starters that score 0 unless changed
```

Check `meta.week` matches the week you're advising on. If the sync fails on a
login redirect, the session cookie expired: ask the user to re-copy it (steps
at the top of `yahoo_web.py`). Never ask for the cookie in chat.

**Lead the answer with the zero check (LESSONS rule 1).** Any starter that is
IR, O, D or Q with a lock before the user's next session gets reported first,
with the lock time and the one move that prevents a 0. The user may not have
time for the full analysis before Thursday, so this part must stand alone.

A **locked** player (`kickoff` None, `opponent` set, `fan_pts` filled) cannot
be moved or dropped until next week. A locked IR starter scores 0 and the
replacement can only help next week. Say so before building the lineup.

### 2. Refresh what decays

```bash
.venv/bin/python sources.py refresh injuries sleeper-trending sleeper-projections lines weather expected-points depth-charts
.venv/bin/python sources.py cache
.venv/bin/python sources.py games          # implied totals + kickoff weather
```

Note the age of what you're using. If the lineup locks within a few hours,
refresh `injuries` again immediately before recommending. Inactives land ~90
minutes before kickoff, and a file inside its TTL can still be wrong.

### 3. Establish availability

Sources, in order of usefulness:

1. **The synced Yahoo data.** Each player carries a `status` field (`Q`, `D`,
   `O`, `IR`, `IR-R`, `PUP-R`, `PUP-P`, `NFI-R`, `SUSP`, `GTD`). Point-in-time:
   check `meta.fetched`.
2. **Sleeper** `injury_status` (`sleeper_players()`), which refreshes
   independently of the sync. `lineup_check.py` prints both.
3. **nflverse** `nfl_injuries(season, week)`: practice status and injury type
   when populated. Check the row count before reading an empty result as
   "nobody is hurt".
4. **Web search** for anything the decision hinges on. **Write what it said
   to `research/week-NN/`** with source and time. An uncached search cannot be
   graded.

**Never recommend a player carrying `IR`, `IR-R`, `PUP-R`, `PUP-P` or `NFI-R`
as a starter.** They are ineligible, not merely risky. `Q`/`D`/`GTD` are
judgment calls.

**For every Q or D starter, choose the fallback as if he is out, and put it in
now (rule 2).** Judge the fallback on its own merits, not against the hope that
the starter plays. Give the time by which the swap must be made, which is the
earlier of the starter's inactives and the fallback's kickoff. If the starter
clears, swap back.

**Do not roster a backup QB (rule 3).** The free-agent pool is the backup, if
the add happens before the lock.

If no source has usable status for a player the decision hinges on, say so and
ask rather than assuming healthy.

### 4. Score every slot as a pool

Load `data/my-roster.json`, `data/free-agents.json`,
`data/opponent-roster.json` and `data/league-settings.json`.

**Rank every eligible player for every unlocked slot together (rule 4).** RB2
and flex are one pool; WR2, WR3 and flex are one pool. Do not take any slot as
given because it did not change. The three most expensive misses were slots
nobody compared.

**Check usage for every starter (rule 5).** Targets, carries, snap share and
xFP (`expected_points(2026)`) over the last two weeks, alongside the
projection. A starter whose volume collapsed is a swap candidate even if his
projection has not moved. For RBs in full PPR, targets per game decide, not
snap share (rule 10).

**Free agents are real options, not background.** A widely-rostered free agent
can beat a current starter outright. `proj_pts` there is Yahoo's weekly
projection (`meta.stat_view` = `S_PW_<week>`). `% Ros` is market consensus,
not a projection. Check `roster_status` (`W (Sep 19)`) before recommending an
immediate add. A free agent whose game has kicked off is on waivers until
Tuesday.

Scoring inputs, under the league's actual rules (full PPR, 6-point passing
TDs, -2 INT, no fractional points):

* **Sleeper projections are the primary source**: `sleeper_projections(2026,
  week)` covers every player and carries `league_pts`. Join with
  `yahoo_to_sleeper(records)` and compare counts. A rostered player with no
  projection is probably not expected to play.
* **Yahoo projections** in `data/*.json` are the second opinion and cover the
  whole roster.
* **Matchup context**: implied team totals (`implied_totals()`) for QB/K/DEF.
  Wind above ~15 mph (`game_weather()`) hurts kickers and deep passing.
* **Luck vs volume**: xFP well above actual means due; actual well above xFP
  means TD luck, not role.
* **QBERT** is broken as of 2026-11-07. Skip it unless `sources.py qbert` works.
* **FantasyPros** needs a key that is not in this checkout. When it is, the
  free tier returns only the top 10 per position, which never includes the
  players a flex call turns on.

**DEF: stream every week for ceiling (rule 8, user decision 2026-11-07).**
Screen free-agent DEFs every week and recommend the best one even inside the
noise bar. Rank by opponent implied total (18 or under is the target), the
opposing QB (backup, rookie, turnover- or sack-prone), then home favorite. Wind
and rain are a bonus. **K (rule 9):** change only for a bye, weather, or a
large implied-total gap.

### 5. Recommend

Fill every starting slot: `QB, WR, WR, WR, RB, RB, TE, W/R/T, K, DEF`.

For each change: the swap, the reason, the confidence. Say plainly when a call
is a coin flip, then pick a side and move on.

**Default to no change.** With no fractional points, gaps under about 2 points
are noise. A swap needs a real edge.

**Exception: underdog by 10 or more (rule 7).** Then a close loss and a big
loss count the same. Break coin flips toward the higher-ceiling player at the
weakest slots, and say that this rule is why.

**Conditional lineups (rule 6).** If a claim is pending or a status is
unresolved, write the lineup both ways: "if X clears, he starts at flex over
Y". If the roster changes after the analysis, re-run the affected pool.

**Waivers.** Recommend an add/drop only when the free agent clearly beats the
current starter. The bar is higher than a bench swap because it costs a roster
spot. Unlimited acquisitions make streaming viable, not mandatory. Flag the
earliest lock: a Thursday player must be added before Thursday kickoff.

**Trades.** When an offer is on the table, score it as rest-of-season points
per game from Sleeper projections, split into regular season (through week 14)
and playoffs (weeks 15–17), with byes left and targets over the last four
games. Value a QB against the best free-agent QB, not against zero. Net the
starting lineup before and after, say what the counter would be, and say
whether the other side is likely to accept. The trade processes for next week.

### 6. Record it

Write the recommendation into `weeks/week-NN.md` **before** the games, using
`weeks/TEMPLATE.md`. Fill "Lock timing" and "What this was decided on",
including which sources were not used and whether last week was graded. Log
recommendations that were not followed too.

## Judgment rules

**Separate what you read from what you recall (rule 12).** Model knowledge of
the 2026 season is unreliable. Base recommendations on `data/` and the cached
sources; when something rests on recalled knowledge, say so. Never invent a
depth chart position, snap share, or injury.

**Volume beats upside in full PPR.** A reception is a guaranteed point, so a
high-target receiver has a higher floor than a deep threat with the same
projection. Use it as the tiebreaker, and know that it has gone about 50/50
between players projected 8–11. It is a tiebreaker, not an edge.

**A lean that rests on a teammate being out is weak until he is ruled out
(rule 11).** Re-check it at the last status update.

**Name the uncertainty.** Every recommendation should be checkable: which
source said what, and how old it was.

**Don't hedge into uselessness.** After stating the uncertainty, commit to a
specific lineup. The user needs a lineup, not a list of considerations.

---
name: week-review
description: Grade last week's lineup. Fill the After section of weeks/week-NN.md with official scores, the counterfactual for every call, and lessons. Use after a week's games finish, or when a week's After section is empty.
---

# Week review

Fill the `After` section of `weeks/week-NN.md` for a completed week. This is
how the advice gets measured. Do it before the next `/start-sit`.

## 1. Pick the week

Default: the most recent `weeks/week-NN.md` whose `After` tables are empty and
whose games are final (Monday night is over). Say which week you are grading.

## 2. Get the official scores

```bash
.venv/bin/python -c "
from yahoo_web import fetch_matchup
from parse_yahoo_html import parse_matchup
import json; m = parse_matchup(fetch_matchup(WEEK, max_age_hours=0)[0])
json.dump(m, open('cache/yahoo/matchup_wWEEK.json','w'), indent=1)
for side in ('me','opponent'):
    t = m[side]['meta']; print(side, t['team_name'], t['fan_total'])
    for p in m[side]['players']: print(' ', p['slot'], p['name'], p['proj_pts'], p['fan_pts'])
"
```

`fan_pts` on the matchup page is the official league score, already rounded.
Use it for every rostered player, including the bench. For the roster as it
was in that week (adds and drops since), use `fetch_roster(WEEK)`.

## 3. Score the alternatives that were not on the roster

Free agents named in the `Before` section (a declined add, a DEF or K not
chosen) come from Sleeper weekly stats scored under league rules:

```bash
.venv/bin/python sources.py refresh expected-points
.venv/bin/python -c "
from sources import sleeper_stats, league_points
s = sleeper_stats(2026, WEEK, max_age_hours=0)
# s[sleeper_id] -> raw stat dict; league_points(stats, pos) -> league score
"
```

Sleeper reads about 1 point higher than Yahoo for some players, so treat a gap
under 2 as noise. Say which source each number came from.

## 4. Fill the tables

* **Header:** result and final score.
* **Actual results:** every starter, projection at lock (Yahoo / Sleeper),
  actual, delta. Add a usage note (targets, carries, snaps, xFP) where the
  delta is large.
* **Counterfactual:** one row per numbered recommendation in `Before`, with
  what the alternative scored. Then add rows for **slots no recommendation
  covered**: the best bench player at each position against the starter. The
  unexamined slots have been the most expensive misses (LESSONS rule 4).
* **Could it have been won?** Best legal lineup from that week's roster, and
  the score with only the calls that were on the table fixed. Say which calls
  decided the week, if any.
* **What to learn:** right, wrong, and anything to change. Judge the process,
  not the outcome: a coin flip that lost is not a miss, and a lucky hit on xFP
  4 is not a hit.

## 5. Update the season files

* `weeks/scorecard.md`: add one row per graded call, update the by-type table.
* `weeks/LESSONS.md`: update the tally on every rule the week touched. A new
  "Anything to change" item becomes a rule here, with its origin week. A rule
  that has been wrong three times in a row moves to Retired.
* Note in the review which rules the week confirmed or contradicted.

## Rules

* Official scores come from Yahoo. Sleeper is for players Yahoo does not show.
* Do not rewrite the `Before` section. It is the record of what was known.
* If a recommendation was not followed, grade both the recommendation and the
  lineup that was played.
* Write the review in the week file before ending the turn.

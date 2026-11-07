# Week NN

**Opponent:** ??? (team N) · **Result:** — · **Final score:** —

Team: Team Auto Pick (W–L) · Source: `yahoo_web.py sync NN` (web session),
fetched YYYY-MM-DDTHH:MMZ (local time). Analysis run <date, time>.

Analysis by: **<model name>** (`<model id>`), via `/start-sit`.

## Before

### Zero check

Output of `lineup_check.py`: every starter that is locked, on bye, or Out
before the next lineup session, with the lock time and the one move that
prevents a 0. "None" is a valid answer; write it.

### Roster changes since the last log

* Adds, drops, claims that cleared, injuries, trades. Note any move that was
  not a recommendation.

### Recommended lineup

| Slot | Player | Yahoo | Sleeper | Game (local) | Change |
|---|---|---|---|---|---|
| QB | | | | | |
| WR | | | | | |
| WR | | | | | |
| WR | | | | | |
| RB | | | | | |
| RB | | | | | |
| TE | | | | | |
| W/R/T | | | | | |
| K | | | | | |
| DEF | | | | | |

**Projected total:** Yahoo — / Sleeper —. Opponent: Yahoo — / Sleeper —.
Favorite or underdog, and by how much. If underdog by 10 or more, say that
ties break toward ceiling (LESSONS rule 7).

### Bench

| Player | Pos | Yahoo | Sleeper | Game | Status |
|---|---|---|---|---|---|
| | | | | | |

### Recommendations made

| # | Recommendation | Reasoning at the time | Confidence | Followed? |
|---|---|---|---|---|
| 1 | | | | |

For a Q or D starter: the fallback, chosen as if he is out, and the time by
which the swap must be made (LESSONS rule 2). For a pending claim: the lineup
if it clears (rule 6).

### Transactions

| Add | Drop | Reasoning |
|---|---|---|
| | | |

### Lock timing

* Thu, Sun early, Sun noon, Sun late, Sun night, Mon: which of my players and
  which decisions lock at each. Inactives land about 90 minutes before kickoff.

### What this was decided on

* **Roster/opponent/free agents:** sync time, `meta.week` check, stat view.
* **Injuries:** sources and their age.
* **Projections and usage:** sources and weeks.
* **Lines/weather:** source and age.
* **Not used, and why:** (FantasyPros, QBERT, ...)
* **Prior week graded?** Yes / no. If no, say so.
* **Research cached:** `research/week-NN/` files written this session.

### Open questions / known unknowns

*

## After

Filled <date> from <source>. (`/week-review`)

### Actual results

| Slot | Player | Proj (Yahoo / Sleeper) | Actual | Δ |
|---|---|---|---|---|
| | | | | |

**Actual total:** — vs projected —. Opponent: — vs projected —.

### Counterfactual

One row per recommendation, then one row per slot no recommendation covered
(best bench option vs the starter).

| Started | Pts | Alternative | Pts | Verdict |
|---|---|---|---|---|
| | | | | |

**Could it have been won?** Best legal lineup from this roster: —. With only
the calls on the table fixed: —. Which calls, if any, decided the week.

### What to learn

* What the reasoning got right:
* What it got wrong:
* Anything to change in how recommendations are made: (copy to `weeks/LESSONS.md`)
* Rules confirmed or contradicted this week:

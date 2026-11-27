# Week 11

**Opponent:** Let go of my Johnson (team 5) · **Result:** Loss · **Final score:** 92–103

Team: Team Auto Pick · Source: `yahoo_web.py sync 11` (web session),
fetched 2026-11-22T04:14Z (Sat Nov 21, 10:14 pm CST). Analysis run Sat Nov 21
~10:30 pm CST. Game times are as Yahoo shows them (Central). Re-synced
2026-11-22T04:26Z after the user made the moves. `lineup_check.py` reports no
starter out, on bye or locked at 0.

Analysis by: **Opus 5.5** (`claude-opus-5-5`), via `/start-sit`.

## Before

### Zero check

`lineup_check.py`: **2 slots score 0 unless changed.** Both lock Sun 12:00 pm.

* **TE: Harold Fannin Jr. (CLE, bye).** Move: Brenton Strange (bench) to TE.
* **WR: Wan'Dale Robinson (IR, ankle; Yahoo and Sleeper).** Move: Emeka
  Egbuka (bench) to WR.
* Already locked (IND @ HOU, Thu): Jonathan Taylor 6 at RB, Spencer Shrader 3
  at K. McGowan (bench) is locked too, so he cannot be dropped this week.
* No starter carries Q or D. Diggs did not practice on the nflverse report,
  marked "Not injury related - resting player". Sleeper has no status for him.

### Roster changes since the last log

* Geno Smith added and Lamar Jackson dropped, per week 10 #1.
* The Corum claim (week 10 #5) was not made.
* Robinson went to IR (ankle) after week 10. Cooper is Out (ankle) again.
* Fannin and Strange are as they were. Egbuka is back from his week 10 bye.

### Recommended lineup

| Slot | Player | Yahoo | Sleeper | Game (Central) | Change |
|---|---|---|---|---|---|
| QB | Cam Ward (add) | 21 | 19.3 | TEN @ DAL, Sun 12:00 pm (indoor) | **IN** for Geno, see #2 |
| WR | Chris Olave | 15 | 15.3 | NO @ CHI, Sun 12:00 pm | — |
| WR | Stefon Diggs | 13 | 13.4 | CIN @ WAS, Mon 7:15 pm | — |
| WR | Emeka Egbuka | 11 | 10.1 | TB @ DET, Sun 12:00 pm (indoor) | **IN** for Robinson (IR), see #1 |
| RB | Jonathan Taylor | — | — | Thu, final | **Locked: 6 pts** |
| RB | Ollie Gordon II | 11 | 11.1 | MIA @ BUF, Sun 12:00 pm | — |
| TE | Brenton Strange | 8 | 9.0 | JAX @ NYG, Sun 3:25 pm | **IN** for Fannin (bye), see #1 |
| W/R/T | Khalil Shakir | 11 | 9.6 | MIA @ BUF, Sun 12:00 pm | — |
| K | Spencer Shrader | — | — | Thu, final | **Locked: 3 pts** |
| DEF | Chargers (add) | 7 | 6.9 | NYJ @ LAC, Sun 3:05 pm | **IN** for Giants, see #3 |

**Projected total:** Yahoo 106 / Sleeper 104, with Taylor 6 and Shrader 3 as
actuals. Opponent: Yahoo 115 / Sleeper 125, with Stroud's 25 locked. **Underdog
by 9 (Yahoo) to 21 (Sleeper).** Rule 7 applies: coin flips break toward
ceiling. As synced, before the fixes, Yahoo showed 93 vs 113.

### Bench

| Player | Pos | Yahoo | Sleeper | Game | Status |
|---|---|---|---|---|---|
| Harold Fannin Jr. | TE | — | — | bye | |
| Xavier Worthy | WR | 6 | 6.8 | KC vs ARI, Sun 12:00 pm | 6, 6, 3 targets in weeks 8–10, 0 pts in week 10 |
| Chimere Dike (add) | WR | 8 | 10.2 | TEN @ DAL, Sun 12:00 pm | Added for Robinson (#8) |
| Omar Cooper Jr. | WR | 0 | — | NYJ @ LAC | **O** (ankle) |
| RJ Harvey | RB | 0 | — | DEN vs LV | **IR** |
| Seth McGowan | RB | — | — | Thu, final | Out. Locked |

### Recommendations made

| # | Recommendation | Reasoning at the time | Confidence | Followed? |
|---|---|---|---|---|
| 1 | **Strange to TE for Fannin (bye). Egbuka to WR for Robinson (IR).** Before Sun 12:00 pm | Zero check (rule 1). Both slots score 0 as set. They are the only healthy bench players at those positions besides Worthy (6.8). | High | Yes (Sat night) |
| 2 | **Add Cam Ward (QB, TEN, FA, immediate), drop Geno Smith. Start Ward.** Before Sun 12:00 pm (Ward's kickoff) | Yahoo 21 vs 17, Sleeper 19.3 vs 18.3. Sleeper calls it noise, but every tiebreak points to Ward. The rule 3 tiebreak added in week 10 says: TEN implied 23.5 indoors in a 54.5 total, vs NYJ 19.75. xFP in his last two games: Ward 23.5, 14.9. Geno 13.3, 8.1, and 5.9 actual in week 10. Rule 7: a 54.5 total is the ceiling play. Both are immediate adds, so certainty does not separate them. Herbert (18 / 18.9, LAC 22.75) is next. Rule 3: drop Geno rather than carry two QBs. **Against:** Ward scored 5.7 in week 7, and Geno's Yahoo projection is fine. | Moderate | Yes (Sat night) |
| 3 | **Stream the Chargers DEF (FA), drop the Giants** | Rule 8. Giants face JAX, implied 25.75 (S 4.8). Free-agent DEFs by opponent implied total: Chargers vs NYJ 19.75 (home, −3), Panthers vs BAL 20.5 (home, −2.5), Eagles vs PIT 20.5 (home dog). None reach the 18 target. Every DEF facing a team implied at 18 or under (KC, BUF, DEN, PIT) is rostered: none of them is in the 17-DEF free-agent pool. Chargers lead on implied total and on both projections (7 / 6.9 vs 6 / 6.7). NYJ's QB is Geno: xFP 8.1 and 5.9 points in week 10. Panthers are a close second: BAL starts Brissett (Lamar, Huntley and Thompson all IR per Sleeper depth), with gusts to 20. **If you keep Geno at QB, take the Panthers instead**, so the DEF is not playing against your own QB. | Low (coin flip with the Panthers) | Yes, Chargers (Sat night) |
| 4 | **No change at WR1/WR2, RB2 or flex** | One pool for WR3 and flex (rule 4): Egbuka 11 / 10.1, Shakir 11 / 9.6, Strange 8 / 9.0 (in at TE), Dike (FA) 8 / 10.2, Worthy 6 / 6.8. No healthy bench RB for flex. McGowan is Out and locked. Gordon (11.1) beats every free-agent RB (Dobbins 8.2). Shakir at flex is a coin flip, and rule 7 favours BUF's 30.5 implied total. Usage: Olave dropped to 4 targets in week 10 after 10 and 12 before, so I'm holding on one week. Diggs drew 10 targets. Gordon had 20 carries and 5 targets in week 10. Shakir had 3 and 4 targets, which is thin. Strange had 2, 2 and 3, also thin, but JAX is implied for 25.75. | Moderate (High on Olave, Diggs, Gordon) | |
| 5 | **No TE add (Goedert, FA, 10 / 9.8)** | Goedert has the volume (7, 4, 6 targets) but PHI is implied 17.0 with Joe Milton at QB (Hurts IR per Sleeper). Strange: JAX 25.75. Inside the noise line, and rule 7 points to the higher team total. | Low (coin flip) | |
| 6 | **No Dike add** (WR, TEN, FA, top Sleeper trending add) | 8 / 10.2 is inside the noise of Egbuka and Shakir. Robinson's IR is confirmed, so rule 11 does not weaken the case, but 3 targets in week 10 do. Revisit for week 12. | Low | |
| 7 | **K: no change possible.** Shrader locked at 3 | — | — | |
| 8 | **Drop Robinson (IR), add Chimere Dike (WR, TEN, FA). Bench depth.** Before Sun 12:00 pm, when Robinson locks and Dike goes on waivers | Asked by the user after the lineup was set. Robinson has no Sleeper projection in any of weeks 12–17, and the league has no IR slot. Dike is the best free-agent WR over the rest of the season on Sleeper: 27.8 in weeks 12–14 and 27.5 in weeks 15–17, at 8.7–9.6 a week. TEN has no bye left, and he stacks with Ward. He is the top Sleeper trending add (199k). Runner-up: Pat Bryant (DEN, 26.3 in weeks 12–14). **Against:** 3 targets in week 10. The case partly rests on Robinson's targets, which is fine under rule 11 because Robinson is ruled out. | Moderate | Yes (Sat night) |
| 9 | **Keep RJ Harvey (IR)** | Sleeper projects 0 in week 12, then 8.6 in week 13 and 7.4–8.6 through week 17. That fits the 4-game IR minimum from his Oct 31 placement (recalled, not in the data). Week 13 byes: IND (Taylor, Shrader, McGowan), NYJ (Cooper), BAL, LV. Harvey is the RB2 that week. The best free-agent RB, Perine, projects 6.6–8.4. No source gives a return date. **If he is not designated to return by about Dec 1–2, cut him for an RB.** Next cut if a spot is needed: Worthy (about 6 a week for the rest of the season), then McGowan (locked this week). | Moderate | Yes |

### Transactions

| Add | Drop | Reasoning |
|---|---|---|
| Cam Ward (QB, TEN, FA, immediate) | Geno Smith | #2. Before Sun 12:00 pm. Second choice: Herbert (LAC, 3:05 pm) |
| Chargers DEF (FA, immediate) | Giants DEF | #3. Before Sun 3:05 pm. If Geno stays at QB, add the Panthers (12:00 pm) instead |
| Chimere Dike (WR, TEN, FA, immediate) | Wan'Dale Robinson (IR) | #8. Bench depth |

All three were made Sat Nov 21 at night and confirmed by the 04:26Z re-sync.

### Lock timing

* Thu Nov 19 (IND @ HOU): final. Taylor 6, Shrader 3, McGowan (bench). Stroud 25 for the opponent.
* **Sun ~10:30 am:** inactives for the noon games. Check Ward, Olave, Egbuka, Shakir and Gordon.
* **Sun 12:00 pm:** Ward, Olave, Egbuka, Gordon and Shakir lock. Robinson's slot must be fixed by then. Ward must be added by then.
* **Sun 3:05 pm:** the Chargers DEF locks (Geno's game).
* **Sun 3:25 pm:** Strange and the Giants DEF lock. Fannin's TE slot must be fixed by then, but #1 does it before noon.
* Mon 7:15 pm: Diggs.

### What this was decided on

* **Roster/opponent/free agents:** `yahoo_web.py sync 11`, fetched
  2026-11-22T04:14Z, `meta.week` = 11 ✓, free agents in the `S_PW_11` view (264).
* **Injuries:** Yahoo sync and Sleeper `injury_status`, refreshed ~04:15Z. The
  nflverse week 11 report (310 rows) shows only Diggs (rest) and Geno (full).
  Game-day statuses are not posted yet, so re-check Sunday ~10:30 am.
* **Projections and usage:** Sleeper week 11 league-scored. Yahoo weekly
  projections. ffopportunity weeks 7–10 (week 11 only has Thursday).
* **Lines/weather:** ESPN and Open-Meteo, refreshed ~04:15Z. Sleeper depth (`depth_chart_order`) for the BAL and PHI QBs.
* **Not used, and why:** FantasyPros (no key). QBERT (parser broken). No web
  search: no call rests on a report outside the cached sources.
* **Prior week graded?** Yes, in this session. Lost 96–99. The Geno pick decided it.
* **Research cached:** none.

### Open questions / known unknowns

* Sunday inactives for the noon games, especially Ward.
* Bench: Harvey (IR, expected back week 13), Cooper (O, projected back week 12)
  and McGowan (Out, hamstring) hold three of six bench spots. The league has
  no IR slots.
* **Week 13 byes: IND, NYJ, BAL, LV.** Taylor, Shrader, McGowan and Cooper are
  all out that week. A one-week K is needed, and Harvey or a free agent at RB.

## After

Filled 2026-11-26 from the Yahoo matchup page (`cache/yahoo/matchup_w11.json`).
Free agents come from Sleeper week 11 stats, league-scored. Usage from
ffopportunity week 11. (`/week-review`)

The lineup played matched the recommendation: Ward at QB, Egbuka at WR,
Strange at TE, Shakir at flex, Chargers DEF. All three transactions were made
Saturday night.

### Actual results

| Slot | Player | Proj (Yahoo / Sleeper) | Actual | Δ |
|---|---|---|---|---|
| QB | Cam Ward (add) | 21 / 19.3 | 25 | +4. 30 attempts, xFP 17.0 |
| WR | Chris Olave | 15 / 15.3 | 19 | +4. **15 targets**, xFP 24.3. The week 10 dip (4) was one week |
| WR | Stefon Diggs | 13 / 13.4 | 8 | −5. 6 targets, xFP 11.1 |
| WR | Emeka Egbuka | 11 / 10.1 | 3 | −8. 5 targets, xFP 7.8 |
| RB | Jonathan Taylor (locked Thu) | 14 / — | 6 | −8. 11 carries, 5 targets, xFP 11.4 |
| RB | Ollie Gordon II | 11 / 11.1 | 8 | −3. 11 carries, 3 targets |
| TE | Brenton Strange | 8 / 9.0 | 4 | −4. **3 targets**, xFP 3.7 |
| W/R/T | Khalil Shakir | 11 / 9.6 | 15 | +4. 9 targets, 2 carries, xFP 17.8 |
| K | Spencer Shrader (locked Thu) | 8 / — | 3 | −5 |
| DEF | Chargers (add) | 7 / 6.9 | 1 | −6. vs NYJ (Geno 25.4 by Sleeper) |

**Actual total:** 92 vs projected 119 (Yahoo, matchup page). Opponent: 103 vs
projected 112. Bench: Dike 12, Worthy 11, McGowan 1, Cooper 0 (Out), Harvey
0 (IR), Fannin (bye).

### Counterfactual

Free-agent numbers are Sleeper, league-scored. Rostered players are Yahoo.

| Started | Pts | Alternative | Pts | Verdict |
|---|---|---|---|---|
| Strange to TE for Fannin (bye) (#1) | 4 | Empty slot | 0 | +4. Hit (rule 1). No other TE on the roster |
| Egbuka to WR for Robinson (IR) (#1) | 3 | Empty slot / Worthy (bench) | 0 / 11 | +3 vs a 0 (rule 1, hit). −8 vs Worthy, but Egbuka out-projected him 11 / 10.1 vs 6 / 6.8. Right on projection |
| Ward for Geno (#2) | 25 | Geno 25.4, Herbert 26.4 | | Noise. The implied-total tiebreak (rule 3) picked a QB who matched the field |
| Chargers DEF for Giants (#3) | 1 | Giants 8 (dropped), Panthers 5 | | **−7 vs the Giants, −4 vs the Panthers. Miss.** No free-agent DEF reached the 18 target. The Giants faced JAX at 25.75 and still outscored the stream |
| Egbuka at WR3 over Dike (#4, #6) | 3 | Dike 12 (bench after #8) | | **−9. Coin flip, lost.** Sleeper had them tied (10.1 vs 10.2); Yahoo favored Egbuka by 3. Dike was ranked in the #4 pool as a free agent, so the rule 6 re-run after the add would have changed nothing |
| Shakir at flex (#4) | 15 | Dike 12, Worthy 11 | | +3. Hit. Rule 7 cited BUF's 30.5 implied total |
| Diggs held at WR2 (#4) | 8 | Dike 12, Worthy 11 | | −4. Miss on points, right on projection (13 vs 8–10). Thursday rest DNP was not a factor |
| Olave held after a 4-target week (#4) | 19 | Worthy / Dike | 11 / 12 | +7. Hit. Holding on one bad week was right |
| No Goedert add (#5) | Strange 4 | Goedert 4.8 | | Noise |
| K (#7) | 3 | — | — | Locked Thursday. No call |
| Dike for Robinson (IR), bench (#8) | Dike 12 (bench) | Robinson 0 (IR) | | Bench only this week. Grade over weeks 12–17 |
| Keep Harvey (IR) over Perine (#9) | Harvey 0 (bench) | Perine 13.7 | | Bench only. Perine projected 7.8, so he would not have started over Gordon. Grade at week 13 |
| RB2: Gordon, no bench alternative (uncovered) | 8 | McGowan (Out, locked) | 1 | No alternative on the roster |

**Could it have been won?** **Yes, by 1.** The best legal lineup from the
roster started Olave 19, Shakir 15, Dike 12 and Worthy 11 across WR and flex
instead of Diggs 8 and Egbuka 3: 104–103. With only the calls on the table
fixed:

* Dike over Egbuka (#4): 101. Still a loss by 2.
* Keep the Giants DEF (#3): 99. Panthers instead: 96.
* Dike plus the Giants: 108, a win. Dike plus the Panthers: 105, a win.

Neither coin flip lost the week alone. The two together did: the WR3 tiebreak
(−9) and the DEF stream (−7). Taylor's 6 and Shrader's 3 locked Thursday
before any analysis, and the opponent's Purdy (28) sat on their bench.

### What to learn

* What the reasoning got right: the zero check caught both zero slots (Fannin's
  bye, Robinson's IR) before the lock. The rule 3 tiebreak picked Ward, who
  matched Geno and Herbert. The holds on Olave (after a 4-target week) and
  Shakir at flex (rule 7, BUF's implied total) were right.
* What it got wrong: the DEF stream again failed to beat the DEF it replaced
  (−7). Every free-agent DEF faced an implied total above the 18 target that
  week, and the Before section said so. The WR3 tiebreak lost 9, on a true
  coin flip. No usage signal separated Egbuka (5 targets in week 9) and Dike
  (3 in week 10).
* Anything to change in how recommendations are made:
  * **DEF streams when the 18 target is not met.** Track the streams where
    a free-agent DEF faced an implied total of 18 or under separately from
    the ones where none did. Week 11 (none met it, −7) is one data point.
    Rule 8 is a user decision, so this is a measurement, not a rule change.
    Added to LESSONS rule 8.
  * No new rule from the WR3 tiebreak. It was a coin flip that lost, which
    the tally already says to expect.
* Rules confirmed or contradicted this week: rule 1 confirmed (+4, +3 vs 0).
  Rule 3 tiebreak: noise. Rule 4: no unexamined slot; the uncovered RB2 had no
  alternative. Rule 6: the Dike add was already in the pool, so no gap.
  Rule 7: applied at flex (+3) and TE (noise). Rule 8: −7, net −1 over 9
  streams. Rule 9: no call (Shrader locked Thursday).

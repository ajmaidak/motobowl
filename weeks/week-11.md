# Week 11

**Opponent:** Let go of my Johnson (team 5) · **Result:** — · **Final score:** —

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

Filled <date> from <source>. (`/week-review`)

### Actual results

| Slot | Player | Proj (Yahoo / Sleeper) | Actual | Δ |
|---|---|---|---|---|
| | | | | |

**Actual total:** — vs projected —. Opponent: — vs projected —.

### Counterfactual

| Started | Pts | Alternative | Pts | Verdict |
|---|---|---|---|---|
| Cam Ward | | Geno Smith / Herbert | | |
| Chargers DEF | | Panthers / Giants | | |
| Egbuka at WR3 | | Dike / Worthy | | |
| Shakir at flex | | Dike / Worthy | | |
| Dike for Robinson (bench, #8) | | Bryant | | Grade over weeks 12–17 |
| Keep Harvey (#9) | | Perine | | Grade at week 13 |
| Strange at TE | | Goedert | | |

**Could it have been won?** —

### What to learn

* What the reasoning got right:
* What it got wrong:
* Anything to change in how recommendations are made:
* Rules confirmed or contradicted this week:

# Week 12

**Opponent:** Team Turf Toe (team 10, 3rd) · **Result:** — · **Final score:** —

Team: Team Auto Pick · Source: `yahoo_web.py sync 12` (web session),
fetched 2026-11-27T03:32Z (Thu Nov 26, 9:32 pm CST, during KC @ BUF).
Analysis run Thu Nov 26 ~9:30–10:15 pm CST. Game times are Yahoo's (Central).
`lineup_check.py` reports no starter out, on bye or locked at 0.

**Sync was partial.** The week 12 matchup page (`matchup?week=12&mid1=9`,
also with `&mid2=10` and bare) came back with no lineup tables, only the
"Who's Got the Skills" manager comparison. The scoreboard page returned
"document not found". This happened both before and after the user re-copied
the cookie. Week 11's matchup page still parses (92–103), so this is Yahoo's
current-week page, not the parser or the cookie. Workarounds used:
the opponent came from his team roster page (`BASE/10?week=12`), and
`data/opponent-roster.json` was written by hand from it. That page has one
extra blank cell after "Action", and `parse_roster` rejects it; the cell was
stripped in a one-off script. Free agents were fetched separately (265,
`S_PW_12` ✓).

Analysis by: **Opus 5.5** (`claude-opus-5-5`), via `/start-sit`.

## Before

### Zero check

`lineup_check.py`: **none.** No starter is IR, O, D or Q.

* Already locked: **Khalil Shakir (W/R/T)**, KC @ BUF Thursday, 4 points in the
  3rd quarter at sync time (wind 17, gusts 43, rain). Worthy (bench) is locked too
  and cannot be dropped this week.
* Earliest lock among my players: **Sun 12:00 pm.** Nothing of mine plays
  Black Friday (DEN @ PIT: only Harvey, IR, bench).
* Watch: Diggs DNP Wed and Thu (personal, excused); Fannin (bench now,
  recommended in) limited Wed, full Thu (groin). See #4 and #2.

### Roster changes since the last log

* Week 11's three moves were made (Ward for Geno, Chargers DEF for Giants,
  Dike for Robinson).
* Cooper is Q again (DNP Thu, ankle + groin). McGowan is Out. Harvey is still
  IR. Fannin is back from his week 11 bye.

### Recommended lineup

| Slot | Player | Yahoo | Sleeper | Game (Central) | Change |
|---|---|---|---|---|---|
| QB | J.J. McCarthy (add) | 18 | 19.1 | NYG @ IND, Sun 12:00 pm (indoor) | **IN** for Ward, see #1 |
| WR | Chris Olave | 15 | 15.6 | NO @ CIN, Sun 12:00 pm | — |
| WR | Stefon Diggs | 13 | 13.1 | WAS @ ARI, Sun 3:25 pm (indoor) | — (conditional, #4) |
| WR | Emeka Egbuka | 10 | 9.5 | CAR @ TB, Mon 7:15 pm | — |
| RB | Jonathan Taylor | 14 | 15.5 | NYG @ IND, Sun 12:00 pm (indoor) | — |
| RB | Ollie Gordon II | 13 | 13.1 | NYJ @ MIA, Sun 12:00 pm | — |
| TE | Harold Fannin Jr. | 12 | 11.3 | LV @ CLE, Sun 7:20 pm (rain 98%) | **IN** for Strange, see #2 |
| W/R/T | Khalil Shakir | 9 | 7.4 | KC @ BUF, Thu | **Locked** (4 at sync, live) |
| K | Spencer Shrader | 8 | 8.9 | NYG @ IND, Sun 12:00 pm (indoor) | — |
| DEF | Patriots (add) | 7 | 7.4 | NE @ LAC, Sun 3:05 pm | **IN** for Chargers, see #3 |

**Projected total:** Yahoo ~117 / Sleeper ~120 with Shakir at his projection.
Opponent: Yahoo 139 / Sleeper ~137 (Burrow 27, Chase 20, Skattebo 17, McBride
16; Kelce live, Bears 2 final). As synced, before changes: Yahoo 109.
**Underdog by ~20.** Rule 7 applies: coin flips break toward ceiling.

### Bench

| Player | Pos | Yahoo | Sleeper | Game | Status |
|---|---|---|---|---|---|
| Brenton Strange | TE | 9 | 10.6 | TEN @ JAX, Sun 12:00 pm | 2–3 targets in each of weeks 8–11 |
| Chimere Dike | WR | 8 | 9.1 | TEN @ JAX, Sun 12:00 pm | Diggs fallback (#4) |
| Omar Cooper Jr. | WR | 9 | 10.9 | NYJ @ MIA, Sun 12:00 pm | **Q**, DNP Thu (ankle, groin) |
| Xavier Worthy | WR | 5 | 5.0 | KC @ BUF, Thu | Locked |
| Cam Ward | QB | 17 | 14.7 | TEN @ JAX, Sun 12:00 pm | Benched by #1; drop Tuesday (#7) |
| RJ Harvey | RB | 0 | — | DEN @ PIT, Fri | **IR** |

(McGowan dropped for McCarthy, #1.)

### Recommendations made

| # | Recommendation | Reasoning at the time | Confidence | Followed? |
|---|---|---|---|---|
| 1 | **Add J.J. McCarthy (QB, NYG, FA, immediate), drop Seth McGowan. Start McCarthy over Ward.** Before Sun 12:00 pm | Both sources favor McCarthy: Yahoo 18 vs 17, Sleeper 19.1 vs 14.7 (avg gap 2.7). Rule 3 tiebreaks agree: NYG implied 23.8 indoors vs TEN 17.5 at JAX (14.5-point dogs). xFP last two games: McCarthy 14, 23 on 36 and 38 attempts with 6–7 rushes. Ward 15, 17 on 39 and 30 attempts. Rule 7 favors McCarthy's rushing ceiling. Depth chart (nflverse 2026-11-26) has McCarthy QB1, Winston QB2. **Geno Smith** (FA, Sleeper 20.9, Yahoo 18, NYJ 22.5) was rejected: 21 attempts in each of his last two games, xFP 8 and 13, and week 10's Geno pick lost the week. **Drop McGowan, not Ward:** McGowan is Out this week and IND is on bye in week 13, so the spot is worth 0 for two weeks. That is a deliberate one-week exception to rule 3; #7 resolves it Tuesday. **Against:** Ward's last two actuals (19, 24 generic PPR) beat his xFP, and a 14.5-point dog gets garbage-time volume. | Moderate | |
| 2 | **Fannin to TE, Strange to bench** | Rule 5: Strange's volume has collapsed (2, 2, 3, 3 targets in weeks 8–11, xFP 3.5–7.8), and only JAX's 32 implied total props up his 10.6. Fannin had 12 and 9 targets in his last two full games (xFP 16.8, 13.6). Projections: Yahoo 12 vs 9, Sleeper 11.3 vs 10.6. Rule 7 points the same way. The week 8 tiebreak (Strange over Fannin) cost 16. Groin: limited Wed, **full Thu** (research/week-12). Fannin plays SNF and Strange locks at noon, so the choice is final at noon. **If Fannin draws a Q on Friday's report or is limited again Fri/Sat, start Strange (rule 2).** | Moderate–high | |
| 3 | **Stream the Patriots DEF (FA, immediate), drop the Chargers DEF** | Rule 8. LAC implied 16.5, the lowest on the slate, with Herbert in concussion protocol (DNP Wed and Thu; DJ Uiagalelei named next up, research/week-12). NE is a road favorite (−2.5). The Chargers face NE (19.0). Free-agent DEFs by opponent implied total: Patriots vs LAC 16.5 (S 7.4), Jets vs MIA 17.0 (7.2), Commanders vs ARI 17.5 (7.5), Giants vs IND 17.8 (7.3). **If Herbert is cleared**, LAC's total will rise; the Commanders become the pick (ARI 17.5, WAS −6.5). Lock: Sun 3:05 pm (Commanders 3:25 pm). No conflict with my QB (NYG). | Moderate | |
| 4 | **Start Diggs. If Friday's report gives him a designation, or he misses Friday too with no explanation, Dike replaces him before Sun 12:00 pm** | DNP Wed and Thu, "personal", excused; reported as not in jeopardy. Sleeper projects him (13.1). Diggs kicks off at 3:25, after Dike's noon lock. A scratch announced at ~1:55 pm inactives leaves only late-window free agents (Tre Tucker, LV, SNF, 7.8; needs a drop, e.g. Worthy is locked so Cooper or Strange). Rule 2 wants the fallback set early, so the Friday and Saturday news decide. | Moderate | |
| 5 | **No change at WR3: Egbuka over Dike (coin flip)** | One pool (flex is locked): Egbuka 10 / 9.5, Dike 8 / 9.1, Cooper Q (excluded, DNP). Usage last week: Dike 7 targets (xFP 11.2), Egbuka 5 (7.8). Default no change; rule 7 tiebreak favors Egbuka's TB 23.2 implied over TEN 17.5. Coin flip. | Low | |
| 6 | **No change at RB, K** | Taylor 14 / 15.5 (4–5 targets, 11–16 carries) and Gordon 13 / 13.1 (20 and 11 carries, 5 and 3 targets) beat every FA RB (Perine 8 / 9.9). No healthy bench RB. Shrader 8 / 8.9 indoors; best FA K McLaughlin 9 / 9.0 is noise (rule 9). | High | |
| 7 | **Tuesday: drop whichever of Ward / McCarthy is the worse week-13 QB. Plan for the IND/NYJ/BAL/LV bye** | Week 13 loses Taylor, Shrader, Cooper (and McGowan, now dropped). Need a K and an RB. Harvey: cut if he is not designated to return by Dec 1–2 (week 11 #9). Worthy (5 a week) is the next cut after that. | — | |

### Transactions

| Add | Drop | Reasoning |
|---|---|---|
| J.J. McCarthy (QB, NYG, FA, immediate) | Seth McGowan (RB, Out) | #1. Before Sun 12:00 pm |
| Patriots DEF (FA, immediate) | Chargers DEF | #3. Before Sun 3:05 pm. If Herbert is cleared, add the Commanders instead (3:25 pm) |

### Lock timing

* Thu Nov 26: KC @ BUF, Shakir (flex) and Worthy (bench) locked. Opponent's Kelce
  live; Bears 2 final; Flournoy, Jacobs (bench) done.
* Fri Nov 27, 2:00 pm (DEN @ PIT): Harvey only (IR, bench). Opponent's Waddle (bench).
* **Fri/Sat injury reports:** Diggs (#4) and Fannin (#2) decide the conditionals.
* **Sun ~10:30 am:** noon inactives. McCarthy, Olave, Taylor, Gordon, Shrader;
  Strange and Dike as fallbacks.
* **Sun 12:00 pm:** McCarthy must be added and in the QB slot. The last point at which
  Strange can replace Fannin or Dike can replace Diggs.
* **Sun 3:05 pm:** Patriots DEF (Herbert's status should be known by ~1:35 pm).
* Sun 3:25 pm: Diggs. Sun 7:20 pm: Fannin. Mon 7:15 pm: Egbuka.

### What this was decided on

* **Roster/opponent/free agents:** `yahoo_web.py sync 12`, fetched
  2026-11-27T03:32Z, `meta.week` = 12 ✓. Opponent from his team roster page
  (03:34Z), not the matchup page (see the header). Free agents `S_PW_12` (265).
* **Injuries:** Yahoo sync, Sleeper `injury_status`, nflverse week 12 report
  (303 rows), all refreshed ~03:35Z Thursday. Thursday practice only; Friday
  designations are not out yet.
* **Projections and usage:** Sleeper week 12 league-scored (486 players; 16/16
  of my roster mapped). Yahoo weekly projections. ffopportunity weeks 8–11,
  joined through the DynastyProcess crosswalk (Sleeper's own `gsis_id` is blank
  for most of my roster).
* **Lines/weather:** ESPN (DraftKings) and Open-Meteo, refreshed ~03:35Z.
  nflverse depth charts (2026-11-26T17:41Z) for the NYG, LAC, TEN and NYJ QBs.
* **Not used, and why:** FantasyPros (no key). QBERT (parser broken). The
  matchup page (Yahoo returned no lineups).
* **Prior week graded?** Not before this analysis. Week 11 was graded right
  after, in the same session (2026-11-26): lost 92–103, the best legal lineup
  would have won 104–103, and the WR3 coin flip (−9) and DEF stream (−7)
  decided it. Nothing in the grade changes a week 12 call.
* **DEF target (LESSONS rule 8 tracking):** met. Patriots face LAC at 16.5.
* **Research cached:** `research/week-12/thu-status.md` (Diggs, Fannin, Herbert).

### Open questions / known unknowns

* Friday designations for Diggs and Fannin; Herbert's final status (drives #3).
* Why the current-week matchup page returns no lineups. If it persists,
  `sync` needs a fallback to the opponent's roster page, and `parse_roster`
  needs to tolerate the extra cell on other teams' pages.

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
| McCarthy | | Ward / Geno Smith | | |
| Fannin at TE | | Strange | | |
| Patriots DEF | | Chargers / Commanders | | |
| Diggs | | Dike | | |
| Egbuka at WR3 | | Dike | | |

**Could it have been won?** —

### What to learn

* What the reasoning got right:
* What it got wrong:
* Anything to change in how recommendations are made:
* Rules confirmed or contradicted this week:

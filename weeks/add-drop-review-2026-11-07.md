# Add/drop review, weeks 1–8

Run 2026-11-07 by Claude Opus 5.5 (`claude-opus-5-5`). Record at the time: 1-7, 10th of 10.

**Sources.** Transactions: Yahoo `transactions?transactionsfilter=all&mid=9`, 21 rows.
Points: Yahoo weekly roster pages (`roster_url(week)`, weeks 1–9) for rostered
players. Sleeper weekly stats scored with `league_points()` for players not on the
roster. Sleeper reads about 1 point higher than Yahoo for some players (25 of ~150
player-weeks), so a gap under 2 points is noise.

Effective week = the first week the added player could score for us.

## Moves

| Wk | Add | Drop | Source | Added player, while held (started) | Dropped player, same weeks | Verdict |
|---|---|---|---|---|---|---|
| 2 | Buccaneers DEF | Jaylen Wright | Claude | 2 (2) | 1 | Neutral |
| 2 | Xavier Worthy (claim) | Steelers DEF | Claude | 50 in 6 games (33) | DEF: see below | Neutral. Fading: 4, 4, 4 in his last 3 games |
| 3 | Chiefs DEF | Buccaneers | Claude | 8 | 5 | Small hit |
| 3 | Emanuel Wilson | Tyler Allgeier | Claude | 45, wks 3–6 (18) | 28 | Hit, but 26 of it was on the bench (wk 4) |
| 4 | Ollie Gordon II | De'Von Achane (IR) | Claude | 55, wks 4–8 (23) | 0 | **Big hit.** Now a starter |
| 4 | Packers DEF | Chiefs DEF | Claude | 8 | 2 | Hit |
| 5 | Jacoby Brissett | Rico Dowdle | Claude | 35, wks 5–6 (35) | 8, then 15 and 12 in wks 7–8 | **Hit.** 29 in Lamar's first missed week |
| 5 | Bengals DEF | Packers DEF | Claude | 9 | 18 | Miss (−9) |
| 5 | Stefon Diggs (claim) | Michael Pittman Jr. (IR) | Claude | 28 (12) | 0 | **Hit.** 16 of it on the bench (wk 6) |
| 6 | Colts DEF | Bengals DEF | Claude | 2 | bye | Forced. Weak pick |
| 6 | Tyler Bass | Jake Bates | Claude | 17 | bye | Hit (bye cover) |
| 7 | Omar Cooper Jr. (claim) | Emanuel Wilson | Claude | 22, 0 (22) | 18, 0 | Neutral. Wk 7 was 22 on 5 targets (luck) |
| 7 | C.J. Stroud (claim) | Jacoby Brissett | Claude | 20 | 18 | Neutral |
| 7 | Browns DEF (claim) | Colts DEF | Claude | 5 | 6 | Neutral |
| 7 | Jake Bates | Tyler Bass | Claude | 9 | bye | Forced (Reichard claim failed) |
| 8 | Commanders DEF | Browns DEF | Claude | 13 | 3 | **Hit (+10)** |
| 8 | Brenton Strange | Marvin Harrison Jr. | Claude | 7, then 4 in wk 9 | bye | Small miss: with Fannin at TE, Shakir (11, benched) would have filled flex |
| 8 | Spencer Shrader | Jake Bates | Claude | 1 | 7 | Miss (−6). Bet on ROS ppg; one week is noise |
| 8 | Wan'Dale Robinson (claim) | Courtland Sutton | Claude | 15 | 9 | Hit |
| 8 | Seth McGowan | C.J. Stroud | User, Sun Nov 1 9:14 am | 2 (bench) | bye | Neutral. Free-agent QBs replace a backup QB (see below) |

## Key misses

1. **Lamar stayed in the QB slot through Thursday's lock (Nov 5). This is the biggest miss.**
   He went on IR on Nov 1. The user had no time to set the lineup before the
   BAL–JAX kickoff, and nothing else checked it. A free-agent QB (Willis, Shough
   or Lock, 17–20 projected) was available all week. Result: **0 at QB in week 9**
   against the first-place team.
2. **The Stroud drop (Nov 1) was not the cause.** In a 1-QB, 10-team league with
   unlimited adds, the waiver wire is the backup QB. Stroud would have helped only if
   the lineup was set before Thursday, and then a free-agent QB would have done
   the same job (user's point, 2026-11-07).
3. **DEF streaming has not paid.** Streamed DEFs scored 47 in wks 2–8 (6.7 a week).
   Holding the Steelers would have scored 55. The single-week swaps net +5 against
   the DEF they replaced. Streaming is about break-even, not an edge.
4. **Kicker churn is noise.** Five K moves. The net is about +11, all from Bass's bye cover in week 6.

## Key hits

* **Gordon for Achane (IR):** 55 points in 4 games. The best pickup of the season.
* **Brissett for Dowdle:** 29 in week 5, when Lamar was first out.
* **Diggs for Pittman (IR)** and **Robinson for Sutton:** both turned dead bench spots into starters.
* **Wilson for Allgeier:** +17 while held, though Allgeier scored 36 in week 8 after Wilson was gone.

## Pattern: pickups scored on the bench

Pickups scored **74 points on the bench**: Wilson 26 (wk 4), Gordon 18 and 14
(wks 4–5), Diggs 16 (wk 6). The add/drop calls were mostly right, but the lineup
was slow to start the new players.

## Players passed on (week 2 screen)

None was a clear miss. Wks 3–8: Germie Bernard 59, Makai Lemon 58, KC Concepcion 54,
Emmett Johnson 37, Caleb Douglas 29, Dontayvion Wicks 25. That is about 4–10 a
week, the same level as the bench WRs we kept.

## Process changes

* **The binding constraint is the Thursday lock, not roster depth.** A starter
  whose team plays Thursday locks in his slot at kickoff. If he is IR or Out, the slot scores 0.
  The user's time is the limit, so the check must be quick or automatic: find
  starters with an IR/O/D status whose game locks before the user's next lineup session.
* **A backup QB is not needed.** The free-agent pool covers a QB loss, if the add happens before the lock.
* **DEF: keep streaming every week, and target ceiling weeks (user decision, 2026-11-07).**
  Seven weeks at about break-even is a small sample, and at 1-7 the team needs
  upside. Scoring rewards holding an offense under 14 (4–10 pts) plus turnovers
  (INT 2, FR 2, sack 1, TD 6). Rank streams by: opponent implied total (≤ 18 is
  the target), a backup, rookie or turnover-prone opposing QB, and home favorite.
  Wind and rain are a bonus. Hits so far: Commanders 13 vs PHI with McKee (implied 17.25).
* **K churn is noise.** Change kickers for a bye, a dome-vs-wind gap, or a big implied-total gap.

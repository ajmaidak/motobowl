# Lessons

Every rule the weekly log has produced, in one place. Each entry names the week
that produced it and how it has done since. Read this before any lineup or
waiver recommendation. When an `After` section ends with "Anything to change",
add or update the rule here in the same turn.

Point values are the counterfactual from the `After` sections: what the call
scored minus what the alternative scored. "Noise" means a gap under 2 points.

## Rules in force, by importance

### 1. Run the zero check first

A starter whose status is IR, O, D or Q, whose game locks before the user's next
lineup session, is the first thing to report. Give the lock time and the one
move that prevents a 0. Run `lineup_check.py` before any analysis.

* Origin: week 9 and the add/drop review (2026-11-07). Lamar Jackson (IR)
  stayed in the QB slot through the Thursday lock. **0 at QB against the first-place team.**
* Tally: 1 miss, −22 (Shough scored 21.7). Week 9 was lost by 14.
* Added week 9: when the roster has no healthy QB, do not defer the add. Enter
  the add or the claim in the same session. The week 9 plan to add a QB on
  Tue/Wed was not carried out. Lamar was still at QB on Thu Nov 12.

### 2. Choose the fallback as if the questionable starter is out, and put it in now

When a starter is Q or D, decide the fallback on its own merits, not against
the hope that the starter plays. Then make the move before the earliest lock.
If the starter clears, swap back.

* Origin: week 6 (Rodgers passed over because "Lamar might play"; Lamar sat,
  Brissett 6, Rodgers 20, lost by 1). Confirmed week 7 (Cooper in for Egbuka
  on Wednesday; Egbuka Out, Cooper 22, margin of victory). Confirmed week 8
  (Shakir in for Egbuka on Wednesday; Egbuka inactive).
* Tally: 1 miss (−14), 2 hits (+22, +11).

### 3. The waiver wire is the backup QB

Do not roster a second QB. In a 1-QB, 10-team league with unlimited adds there
is always a 17–20 point QB available. The condition is rule 1: the add must
happen before the lock.

* Origin: week 4 (no backup for Lamar, Q), confirmed week 5 (Brissett add +29
  vs Lamar inactive) and the add/drop review.
* Tally: 3 right, 0 wrong. The week 9 zero was a rule 1 failure, not a rule 3 failure.
  Week 8 did not test it: Lamar was active and was hurt on his first snap. No
  backup, rostered or free agent, can replace a starter after his lock.

### 4. Rank every eligible player for every unlocked slot, as one pool

Do not take any slot as given. RB2 and flex are one pool; WR2, WR3 and flex are
one pool. The biggest misses came from slots nobody examined.

A player benched by a swap at his own position stays in the flex pool. Rank him
for flex before the analysis ends (week 8: Fannin).

* Origin: week 5 (Harvey 0 at RB2, Gordon 14 on the bench, never compared;
  lost by 2). Repeated week 6 (Wilson 5 at RB2 vs Shakir 13; lost by 1) and
  week 4 (Wilson 26 on the bench, projected 5).
* Tally: 5 misses from unexamined slots, −44 (weeks 2, 4, 5, 6, 8). Zero hits,
  because an unexamined slot cannot be a hit. Week 8: the TE call benched Fannin
  (10.7) and the flex stayed with Worthy or Harvey (9.0, 8.3). The user moved
  Fannin to flex, and he scored 23. The points are in the TE tally.

### 5. Check usage for every starter, not only the contested ones

Before scoring, pull the last two weeks of targets, carries and snap share for
every starter (ffopportunity xFP covers this). A starter whose volume has
collapsed is a swap candidate even when his projection has not moved.

* Origin: week 6 (Fannin 1 and 1 on 4 and 3 targets, no TE screened either
  week; Wilson 27 of 85 snaps). Week 7: Fannin's targets came back and the
  rule said hold. Right.
* Tally: 1 miss (−10, Fannin), 1 hold confirmed.

### 6. A lineup with a pending claim is conditional

Write the lineup as "if X clears, he starts at flex over Y". When a claim
clears or a status changes after the analysis, re-run the affected slots
before lock.

* Origin: week 2 (Worthy claim cleared Saturday, flex never re-examined,
  Dowdle 6 vs Worthy 13).
* Tally: 1 miss (−7), 1 confirmed. Week 8: the Robinson claim cleared and
  Harvey went on IR on Oct 31. The user re-ran the slots (Fannin to flex),
  +12 over the written plan. The re-run is not in the log.

### 7. Break ties toward ceiling when the projection says underdog by 10 or more

The default is no change, and gaps under 2 are noise. The exception is a week
where the projected margin is large: then a close loss and a big loss count the
same, so take the higher-variance side of a coin flip at the weakest slots.

* Origin: week 4 outlook, applied in weeks 6, 8 and 9.
* Tally: not yet graded as a rule. Week 8 cannot grade it: lost by 60, so no
  tiebreak mattered. Week 9: not applied, no coin flip was broken toward ceiling.

### 8. Stream DEF every week for ceiling (user decision, 2026-11-07)

Always screen free-agent DEFs. Rank by opponent implied total (18 or under is
the target), opposing QB (backup, rookie, turnover-prone), then home favorite.
Recommend the best one even inside the noise bar.

* Origin: add/drop review. Streams scored 47 in weeks 2–8 (6.7 a week) vs 55
  for holding the Steelers. About break-even.
* Tally vs the DEF replaced: wk2 −8, wk3 +3, wk4 +6, wk5 −9, wk6 −2, wk7 −1,
  wk8 +10. **Net −1 over 7 streams.** The implied-total signal was right in
  weeks 4, 8 and 9 and wrong in week 5. Week 9: Giants 13 vs Commanders 6, +7.
  **Net +6 over 8 streams.** Week 8 confirmed in the `After` section
  (Commanders 13, Browns 3).

### 9. Kicker churn is noise

Change kickers only for a bye, a dome-vs-wind gap, or a large implied-total gap.

* Origin: add/drop review. Five K moves, net about +11, all from the week 6 bye cover.
* Tally: wk2 −9 (1-point gap, variance), wk6 +16 (bye), wk7 0, wk8 −6
  (rest-of-season bet; Shrader 1, Bates 7). Confirmed week 8. Week 9: Shrader held, 16.

### 10. Judge RBs in full PPR on targets per game, not snap share

A passing-down back on 36% of snaps with 7 targets is a full-PPR starter. The
same back with 1 target scores 0. Check targets, and treat the floor as zero.

* Origin: week 3 (Harvey 7 targets on 36% snaps, benched for Worthy, −6).
  Week 4 Harvey 10 targets, 18. Week 5 Harvey 1 target, 0.
* Tally: 1 miss (−6), then rule 4 took over.

### 11. A lean that rests on a teammate being out is weak until he is ruled out

If the case for X is "his teammate is Q", re-check at the last status update.
If the teammate is active, drop the lean back to the projections.

* Origin: week 3 (Shakir over Sutton on BUF's Q receivers; DJ Moore played,
  10 targets, Shakir 1, Sutton 7).
* Tally: 1 miss (−6).

### 12. Separate what was read from what was recalled

Model knowledge of the 2026 season is unreliable. Say when a claim rests on
memory. Never invent a depth chart, snap share or injury.

* Origin: project rule from day one. No graded miss attributed to it yet.

## What the tally says

**Bench-tier WR3, TE and flex tiebreaks are coin flips.** Eighteen graded WR3
and flex calls in weeks 1–8 between players projected 8–11 netted −16: 5 right,
6 wrong, 7 noise. The week 8 TE tiebreak (Strange over Fannin, tied
projections) lost 16. The usage tiebreaker (targets) went 1–1 on Shakir vs Sutton, then 1–1
again. Spend the analysis on rules 1–5. Make the tiebreak call, state it as a
coin flip, and move on.

**The expensive misses were slots nobody looked at**, not tiebreaks that went
the wrong way: Harvey 0 (week 5, −14), Rodgers not added (week 6, −14), Lamar
locked (week 9, about −18). Weeks 5 and 6 were lost by 2 and 1.

**Availability calls are where the advice has earned its keep:** Brissett for
Lamar +29, Cooper for Egbuka +22, Harvey and Gordon for Achane +18. Those are
rules 1–3.

## Retired

* **Treat Sutton's projections skeptically** (week 4). Sutton was dropped in week 8.
* **DEF correlation with my own players as a tiebreaker** (weeks 1 and 7). It
  cost 5 in week 7 (Browns 5, Vikings 10) and nothing in week 1. Rule 8 ranks
  by matchup instead.
* **Hold DEF unless the gap beats 2 and a second signal agrees** (week 2).
  Replaced by rule 8 on 2026-11-07.

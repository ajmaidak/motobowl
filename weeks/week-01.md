# Week 1

**Opponent:** Orton's BloodyFinger (Brian) — not known at decision time
**Result:** **L** · **Final score:** 134 – 159 · Record 0-1-0, 7th

Team: Team Auto Pick · Source: hand-pasted snapshot (Yahoo API not yet approved)

Analysis by: **Claude Opus 5** (`claude-opus-5`) — Before section 2026-09-09, After section 2026-09-16.

## Before

### Recommended lineup

One change from the auto-drafted default: **bench Marvin Harrison Jr., start Rico
Dowdle at flex, slide Courtland Sutton up to WR3.**

| Slot | Player | Proj | Game | Change |
|---|---|---|---|---|
| QB | Lamar Jackson | 22 | @ IND, Sun 12:00 pm | — |
| WR | Chris Olave | 16 | @ DET, Sun 12:00 pm | — |
| WR | Emeka Egbuka | 11 | @ CIN, Sun 12:00 pm | — |
| WR | Courtland Sutton | 11 | @ KC, Mon 7:15 pm | moved from W/R/T |
| RB | Jonathan Taylor | 17 | vs BAL, Sun 12:00 pm | — |
| RB | De'Von Achane | 17 | @ LV, Sun 3:25 pm | — |
| TE | Harold Fannin Jr. | 10 | @ JAX, Sun 12:00 pm | — |
| W/R/T | Rico Dowdle | 11 | vs ATL, Sun 12:00 pm | **IN** (for Harrison) |
| K | Jake Bates | 8 | vs NO, Sun 12:00 pm | — |
| DEF | Steelers | 7 | vs ATL, Sun 12:00 pm | — |

**Projected total:** 130 (was 128 as auto-drafted)

### Bench

| Player | Pos | Proj | Game | % Started |
|---|---|---|---|---|
| Michael Pittman Jr. | WR | 10 | vs ATL, Sun 12:00 pm | 11% |
| Marvin Harrison Jr. | WR | 9 | @ LAC, Sun 3:25 pm | 29% |
| Khalil Shakir | WR | 9 | @ HOU, Sun 12:00 pm | 3% |
| RJ Harvey | RB | 8 | @ KC, Mon 7:15 pm | 10% |
| Tyler Allgeier | RB | 6 | @ LAC, Sun 3:25 pm | 3% |
| Jaylen Wright | RB | 2 | @ LV, Sun 3:25 pm | 0% |

### Recommendations made

| # | Recommendation | Reasoning at the time | Confidence | Followed? |
|---|---|---|---|---|
| 1 | **Start Rico Dowdle (flex) over Marvin Harrison Jr.; Sutton fills WR3** | Four signals lean Dowdle, none decisive: Yahoo proj 11 vs 9; % started 40% vs 29%; ceiling (proj_max) 17 vs 14 at nearly identical floors (5 vs 6); and Harrison draws @ LAC, which FantasyPros ranks **DST2** this week. The case *against* is real — nflverse depth chart (dated 2026-09-09) has Harrison as ARI **WR1** (alpha target share, the thing full PPR pays for) while Dowdle is PIT **RB2** behind Jaylen Warren, which is the classic low-floor committee profile. Tiebreaker: ARI's QB1 on today's depth chart is **Jacoby Brissett**, which caps what a WR1 target share is worth, and Dowdle correlates *positively* with my Steelers DEF (a PIT lead means run volume) where Pittman would correlate negatively. **Close to a coin flip — leaving Harrison in is defensible.** | Low–moderate | Yes |
| 2 | **No waiver move — including DEF.** | Nothing available clearly beats a starter. Best FA per position by % Ros: WR Deebo Samuel 47% (my WR3 candidates are 81–94%), RB Mike Washington Jr. 55%, TE Hunter Henry 56% (vs Fannin, FP **TE6**), K Will Reichard 65% (vs Bates, FP **K7**; Reichard unranked). **DEF was worked separately below** — Steelers stay. | High | Yes |
| 3 | **No move on Pittman → WR3.** | Yahoo proj 10 vs Harrison 9 is inside the no-fractional-points noise band, and the market disagrees with the projection (11% started vs 29%). Not a real edge. | High | Yes |

### DEF: Steelers vs. the wire (worked in detail)

FantasyPros returns **raw components** for DST, so these are **league-exact**
points computed from `data/league-settings.json` — not FP's prepackaged total,
which uses a generic points-allowed ladder rather than this league's
(0 pts→10, 1-6→7, 7-13→4, 14-20→1, 21-27→0, 28-34→-1, 35+→-4).

| DEF | League-exact EV | proj PA | sacks | TOs | Availability | Matchup |
|---|---|---|---|---|---|---|
| Chargers | **8.12** | 19.0 | 3.35 | 1.26 | FA, 67% Ros | vs ARI |
| Titans | 7.77 | 20.5 | 3.35 | 1.32 | FA, 20% Ros | vs NYJ |
| **Steelers (mine)** | **7.66** | 18.8 | 2.59 | 1.45 | rostered | vs ATL |
| Raiders | 7.45 | 19.0 | 2.87 | 1.26 | FA, 8% Ros | vs MIA |
| Packers | 6.71 | 22.7 | 2.68 | 1.32 | FA, 15% Ros | @ MIN |

**Verdict: keep the Steelers.** The best available alternative is **+0.46
points** — about a fifth of this league's noise threshold, and with no
fractional points a half-point edge usually cannot appear on the scoreboard at
all. Checked for robustness: the PA band is the only modelled quantity (FP gives
a *mean* points-allowed, so it was integrated over the bands with a normal), and
the LAC−PIT gap is **+0.45 to +0.47 across σ = 7, 9.5, 12 and 14** — the
conclusion does not depend on that assumption. FP's own total (7.90 vs 7.40) and
Yahoo's projection (7) agree.

**The matchup argument that looked decisive isn't.** ARI's QB1 is Jacoby
Brissett and their RB1 Jeremiyah Love is Questionable (Sleeper), while ATL rolls
out Tua Tagovailoa, Bijan Robinson (FP RB2), Drake London (FP WR9) and Kyle
Pitts (FP TE4) — so LAC plainly draws the softer offense. But FP still projects
**Pittsburgh to allow *fewer* points (18.8) than Los Angeles (19.0)**, because
the Steelers' defense is enough better to absorb the harder matchup. LAC's
entire edge is sacks (3.35 vs 2.59, +0.76), and PIT claws most of it back on
turnovers (1.45 vs 1.26, worth +0.38 at 2 pts each). Weekly ECR having them one
slot apart (DST2/DST3) was already telling me this; the components confirm it.

**Vikings are a trap.** Highest % Ros of any available DEF (82%) but **outside
FP's top-10 DST entirely**, so no projection exists for them and the market
number is reputation, not this week's matchup. They host a Jordan Love offense.
Not the play.

### Transactions

None recommended.

**Thursday deadline (SF @ LAR, Thu Sep 10 7:35 pm):** the only free agents whose
games lock before Sunday are Deebo Samuel Sr. (SF WR, 47% Ros), Terrance
Ferguson (LAR TE, 25%), Kaelon Black (SF RB, 25%), Eddy Pineiro (SF K, 57%),
49ers DEF (9%) and Ricky Pearsall (SF WR, **IR** — ineligible). None beats a
current starter, so **no action is needed before TNF.**

### What this was decided on

* **Roster snapshot:** `data/my-roster.json`, `meta.week` = 1 ✓ matches. Paste
  taken 2026-09-09 22:08 (hours old).
* **Free agents:** 147 players, six position pastes taken 2026-09-09 23:00–23:06.
  25 rows per position, sorted descending by % Ros; the TE/QB/RB/K/DEF lists
  reach 0% Ros, so those pools are fully characterized rather than truncated.
* **Injury/availability:** Sleeper (0.6h old) shows **all 16 roster players
  `Active` with `injury_status: None`** — no Q/D/O/IR anywhere. The Yahoo roster
  paste likewise carries no designations. nflverse `injuries_2026.csv` is still
  the known stub: **29 rows, four teams (SF/SEA/LA/NE), 24 blank statuses** — it
  covers none of my players and was not used.
* **FantasyPros:** free tier returned the top 10 *per position*, which covered
  Lamar Jackson (QB1), Taylor (RB4), Achane (RB5), Olave (WR7), Fannin (TE6),
  Bates (K7), Steelers (DST3) — i.e. every already-locked starter, and **not one
  of Harrison, Sutton, Pittman, Shakir, Dowdle or Harvey.** Exactly the coverage
  gap CLAUDE.md warns about; the flex/WR3 call ran on Yahoo projections instead.
* **Depth charts:** nflverse, dated **2026-09-09T12:06:21Z** (same day).
* **Free-agent pastes carry no `Proj Pts` column** — the waiver comparison used
  **% Ros, which is market consensus, not a projection.** Every waiver
  conclusion above is "the market doesn't rate these players above my starters,"
  not "these players project lower."

### Read, not recalled

The depth chart contradicted 2025-vintage recall in several places that actually
mattered. Recording these because they are the assumptions the week rests on:

* **Rico Dowdle and Michael Pittman Jr. are both Pittsburgh Steelers.** The
  Yahoo paste says `Pit`, and Sleeper independently confirms `team: PIT` for
  both. Not a column-shift bug.
* ARI QB1 is **Jacoby Brissett** (not Kyler Murray, who is a free agent on MIN
  at 76% Ros). ARI RB1 is **Jeremiyah Love**, with James Conner down at RB4.
* PIT QB1 is **Aaron Rodgers**; RB1 is **Jaylen Warren**, Dowdle RB2.
* DEN WR1 is **Jaylen Waddle**, Sutton WR2. DEN RB1 is **J.K. Dobbins**, Harvey RB2.
* BUF WR1 is **DJ Moore**, Shakir WR2.
* MIA QB1 is **Malik Willis**, and the MIA WR room is barren (Malik Washington
  WR1) — which is part of why Achane is an easy start in full PPR.
* NO QB1 is **Tyler Shough**; Olave is still the clear WR1 there.

Caveat on all of the above: nflverse depth charts are ESPN-sourced, and
`pos_rank` is a listed role, not a measured snap or target share. No 2026 usage
data exists yet — week 1 has not been played — so **there is no target-share
evidence behind any of this week's calls**, only projections, depth-chart role
and market consensus.

### Open questions / known unknowns

* **Opponent unknown.** `data/opponent-roster.txt` is empty, so none of this
  accounts for what I need to beat. With a 130-point projection and no
  opponent context, this lineup is set to maximize points rather than to
  leverage or hedge against a specific matchup.
* **Sutton is Monday night.** If the week is close going into MNF, the WR3 slot
  is where the variance lives — but the lineup locks long before that is known.
* **Trending adds are noise for this league.** Michael Mayer led league-wide adds
  by a wide margin (1.46M) but is rostered here; the highest-% Ros trending
  player actually available is Tre Tucker at 30%, far below any starter.

## After

Source: Yahoo My Team and Matchup pages, week 1, all games Final — pasted into
chat 2026-09-16.

**Lost 134–159 to Orton's BloodyFinger.** Yahoo's original projections had it
as a toss-up (131 vs 132). The opponent beat their projection by 27; I beat
mine by 3.

| Pos | Opponent starter | Proj | Actual |
|---|---|---|---|
| QB | Jalen Hurts | 22 | 30 |
| RB | Bijan Robinson | 19 | 31 |
| RB | Javonte Williams | 16 | 24 |
| WR | Ladd McConkey | 13 | 19 |
| WR | Jameson Williams | 13 | 8 |
| WR | Jayden Reed | 11 | 5 |
| TE | Jake Ferguson | 9 | 2 |
| W/R/T | Travis Etienne Jr. | 14 | 14 |
| K | Trey Smack | 7 | 13 |
| DEF | Jaguars | 8 | 13 |

### Actual results

| Slot | Player | Proj | Actual | Δ |
|---|---|---|---|---|
| QB | Lamar Jackson | 22 | 26 | +4 |
| WR | Chris Olave | 16 | 28 | +12 |
| WR | Emeka Egbuka | 11 | 11 | 0 |
| WR | Courtland Sutton | 11 | 3 | −8 |
| RB | Jonathan Taylor | 17 | 24 | +7 |
| RB | De'Von Achane | 17 | 10 | −7 |
| TE | Harold Fannin Jr. | 10 | 4 | −6 |
| W/R/T | Rico Dowdle | 11 | 3 | −8 |
| K | Jake Bates | 8 | 7 | −1 |
| DEF | Steelers | 7 | 18 | +11 |

**Actual total:** 134 vs projected 130

Bench: Shakir 9, Pittman 8, Allgeier 8, Harvey 7, Harrison 4, Wright 0 (36).

**Best possible lineup: 145** — Shakir at WR3 and Pittman or Allgeier at flex
instead of Sutton and Dowdle. **11 points left on the bench**, all of it in the
two slots the week's analysis focused on. **The optimal lineup still loses by
14**, so no start/sit decision cost this game. The loss came from the
opponent's QB and two RBs scoring 85 against a 57 projection (+28).

### Counterfactual

| Started | Pts | Alternative | Pts | Verdict |
|---|---|---|---|---|
| Rico Dowdle | 3 | Marvin Harrison Jr. | 4 | Lost by 1 — a wash inside the no-fractional-points noise. The auto-draft default would have scored 135. |
| Courtland Sutton | 3 | Michael Pittman Jr. | 8 | Lost by 5. |
| Courtland Sutton | 3 | Khalil Shakir | 9 | Lost by 6 — the best bench option was the one with the lowest % started (4%). |
| Steelers DEF | 18 | Chargers DEF (FA, league-exact EV +0.46) | ? | Keeping them was almost certainly right: 18 was DEF2 for the week, and LAC gave up 26 to ARI (0 points-allowed points in this league). LAC's exact total wasn't recovered. |
| Jake Bates | 7 | Will Reichard (FA) | ? | Not recovered from the pastes; Bates was 1 under projection, so the gap can't be meaningful. |

### What to learn

* **What the reasoning got right:** Standing pat at DEF (Steelers 18, +11 over
  projection) and at K. No waiver churn was needed. Keeping Jackson and Olave
  locked in paid off (+16 combined).
* **What it got wrong:** Both contested slots busted. Dowdle (RB2 behind Warren,
  8 carries for 15 yards) scored exactly what his committee role suggested. The
  "positive correlation with Steelers DEF" tiebreaker was right that PIT won and
  the defense scored, but Dowdle still got nothing from it. Sutton caught 2 of 5
  targets on MNF in a 10–31 blowout.
* **Can't be graded on one week:** Harrison (WR1 by depth chart) scored only 4,
  so "depth-chart role vs projection+market" came out a 1-point tie and settles
  nothing. The flex/WR3 pool (Sutton, Dowdle, Harrison, Pittman, Harvey,
  Allgeier, Shakir) scored 3–9, a 6-point spread among players projected 6–11.
  A normal week produces that much randomness, so don't overcorrect from it.
* **Worth tracking going forward:** Real week 1 usage data now exists, which the
  week 1 analysis lacked. Targets: Shakir 6, Egbuka 6, Sutton 5, Dowdle 5,
  Harvey 4, Harrison 3, Pittman 3. Carries: Allgeier 17 (behind/alongside Love
  at ARI), Dowdle 8, Harvey 3. **Allgeier's 17 carries is the most notable
  bench signal.** Week 2 calls should use target/carry share rather than
  depth-chart order alone.
* **New designations in this paste:** Pittman **Q**, Harvey **Q**. Check before
  week 2.
* **Process change:** Let 2026 usage data (snaps, targets, carries) take over
  from depth-chart role as the tiebreaker for bench-slot calls once it exists.

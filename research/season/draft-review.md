---
source: Yahoo draft results page (/draftresults?drafttab=round, 160 picks), Yahoo week 4 rosters (all teams), Sleeper league-scored stats wks 1-3 and projections wks 5-14
fetched: 2026-10-01T01:32Z
topic: draft review at 0-3 (picks chosen by Claude Fable, drafting from slot 8 of 10; not Yahoo autodraft despite the team name)
week: 4
---

# Draft review after week 3

"vs slot" = a pick's league points in weeks 1-3 minus the average of the picks within ±5 of it (K/DEF compared only with K/DEF). Three weeks is a small sample: this measures outcomes, and some of it is variance.

## Findings

* **Rounds 1-5 were fine: +21 vs slot.** Taylor +12, Olave +28, Lamar +25. Achane -27 (ACL in week 3; 11 and 12 pts before that). Egbuka -17.
* **Rounds 6-16 were the worst in the league: -158 vs slot.** The next worst was Pipefitters at -56, and the league best was We Stinks at +75. Every pick from round 6 to 14 except Fannin (+11) finished below slot.
  * Rounds 6, 7, 10: **Harrison (-35), Sutton (-11), Pittman (-27)**. All three are full-time WRs with low target counts (Harrison 3/1/5, Sutton 5/4/7, Pittman 3/-/5). Their floors are safe but their ceilings are low.
  * Round 9: **Dowdle (-28)**, a committee RB who lost the job to Warren and then got hurt.
  * Rounds 11-13: **three backup RBs (Harvey, Allgeier, Wright)**. Two have been dropped, and only Harvey has a role.
* **Shape:** RRWWQWWTRWRRRWKD, i.e. 6 RBs and 6 WRs. Lots of RBs were drafted, but only Taylor and Achane were lead backs.
* **Post-draft adds** (Worthy, Gordon) are worth 169 ROS, mid-pack. Most of the waiver value other teams found was QBs (Stafford, Young, Shough, Stroud).
* **Total:** 441 pts from drafted players in weeks 1-3, last in the league (the range was 496-732).

## Raw

```
MY DRAFT  (pts = league pts wks 1-3; ROS = Sleeper proj wks 5-14 total)
rd ovr player                   pos   pts  ROS  now               | best pts wk1-3 taken before my next pick (same pos / any pos)
 1   8 Jonathan Taylor          RB     64  167  Team Auto Pick         | James Cook III RB 50 / CeeDee Lamb WR 71
 2  13 De'Von Achane            RB     25    0  FA/waivers       IR    | Kenneth Walker III RB 79 / Kenneth Walker III RB 79
 3  28 Chris Olave              WR     70  165  Team Auto Pick         | DeVonta Smith WR 48 / Josh Allen QB 104
 4  33 Emeka Egbuka             WR     33   98  Team Auto Pick         | Davante Adams WR 66 / Davante Adams WR 66
 5  48 Lamar Jackson            QB     68  227  Team Auto Pick   Quest | - / Christian Watson WR 69
 6  53 Marvin Harrison Jr.      WR     11   58  Team Auto Pick         | Parker Washington WR 49 / Joe Burrow QB 65
 7  68 Courtland Sutton         WR     16   91  Team Auto Pick         | Mike Evans WR 38 / Jaylen Warren RB 41
 8  73 Harold Fannin Jr.        TE     39  105  Team Auto Pick         | George Kittle TE 47 / Caleb Williams QB 49
 9  88 Rico Dowdle              RB     10   90  Team Auto Pick   Out   | Chuba Hubbard RB 53 / Dak Prescott QB 77
10  93 Michael Pittman Jr.      WR     12   89  Team Auto Pick         | Michael Wilson WR 40 / Brock Purdy QB 99
11 108 RJ Harvey                RB     19   88  Team Auto Pick         | Jordan Mason RB 12 / Matthew Golden WR 46
12 113 Tyler Allgeier           RB     18   53  FA/waivers             | Aaron Jones Sr. RB 35 / Matthew Stafford QB 64
13 128 Jaylen Wright            RB      1   71  FA/waivers       Quest | Chris Rodriguez Jr RB 13 / Jared Goff QB 82
14 133 Khalil Shakir            WR     17   84  Team Auto Pick         | Xavier Worthy WR 22 / Patrick Mahomes QB 81
15 148 Jake Bates               K      21   75  Team Auto Pick         | Cameron Dicker K 14 / Juwan Johnson TE 48
16 153 Steelers                 DEF    16   69  FA/waivers             | Ravens DEF 16 / Jordan Love QB 64

TEAM DRAFT VALUE: pts wks1-3 from drafted players (all, whether started or not), ROS of drafted players still rostered, kept count
  We Stinks              pts   732  ROS-kept  1976  kept 15/16  order RWWQRTWWRQWWDKRT
  Let go of my Johnson   pts   604  ROS-kept  1596  kept 13/16  order WRWWRWRTWQWTRWDK
  Dak to the Future      pts   585  ROS-kept  1492  kept 10/16  order RWWWWRTRQWWRRQDK
  Pipefitters 309        pts   557  ROS-kept  1340  kept 11/16  order RRRWWRWQTRWWQDKR
  Team Turf Toe          pts   547  ROS-kept  1426  kept 11/16  order WWTWRQRWWRRDTWKQ
  Cougar Slayers         pts   542  ROS-kept  1712  kept 15/16  order RWRWTWRQWRWQTRDK
  Hay Ho                 pts   533  ROS-kept  1740  kept 14/16  order WRWRWWRQRWTRTRKD
  Orton's BloodyFinger   pts   519  ROS-kept  1563  kept 13/16  order RTRRWWQWRTQWWRDK
  Six Axis               pts   496  ROS-kept  1702  kept 14/16  order WRWRWQTRRWKWWQDW
  Team Auto Pick         pts   441  ROS-kept  1337  kept 12/16  order RRWWQWWTRWRRRWKD
```

## Was it an AI drafting from stale knowledge? (checked 2026-09-30)

Hypothesis: a model drafting from recall would overvalue veterans' past seasons
and miss rookies. **The data doesn't support it.**

* League-wide, rookies drafted underperformed their slot the most (avg −14.6 vs
  slot, n=9). Players in years 2–3 averaged −9.9, years 4–6 −0.6, and 7+ −2.9.
  Skipping rookies was not the mistake.
* This roster's rounds 6–16 average age (25.8) is mid-pack. 7 of 10 teams took 0–1
  rookies there.
* The misses are role misreads plus variance: low-target WRs (Harrison, Pittman),
  a committee RB (Dowdle, behind Warren), and three backup RBs. Whether those
  roles were knowable at draft time (Sep 7) depends on what information the
  drafting model had, and that isn't recorded here.

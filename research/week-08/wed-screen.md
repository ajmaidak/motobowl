---
source: Yahoo web sync 8 (fetched 2026-10-29T03:37Z); Sleeper players, injury_status, wk8 projections (league-scored), refreshed 2026-10-29T03:20Z; nflverse injuries (wk8 = 16 rows, stub); ffopportunity expected points wk1-7; ESPN lines (DraftKings) + Open-Meteo, refreshed ~03:20Z; web search 2026-10-29 ~03:40Z (ESPN, NBC Sports, CBS Sports, Draft Sharks, Rotowire, Hogs Haven, Baltimore Sun)
fetched: 2026-10-29T03:44Z
topic: week 8 byes, Wednesday practice reports (Lamar, Egbuka, Diggs), WR/flex usage, DEF stream
week: 8
---

# Week 8 screen (Wed evening)

## Data notes

* `yahoo_web.py check` returned **400 Bad Request** from Yahoo's edge server
  (ATS). The cookie was valid. The `uids` (3.8 KB) and `eids` (2.2 KB) tracking
  cookies made the request header too large. A request with only the auth
  cookies (`Y`, `T`, `A1`, `A3`, ...) returned 200. Sync ran with that subset
  through `YAHOO_COOKIE`.
* FantasyPros not used: no `.credentials.json` in this checkout. Free tier is
  top 10 per position in any case.
* Sleeper `gsis_id` is blank for many players (for example, Jonathan Taylor).
  Join expected points through the DynastyProcess crosswalk
  (`ff_player_ids()` sleeper_id -> gsis_id).

## Byes

HOU (Stroud, Harrison) and NO (Olave).

## Availability

* **Lamar Jackson (Yahoo Q, Sleeper Q, ankle sprain):** **full practice
  Wednesday**, his first full session since the week 4 sprain (24 days).
  Rapoport (Tue) expected him to play at BUF. Minter has not confirmed.
  He missed weeks 5–7. Sources: ESPN, NBC Sports, CBS Sports, Baltimore Sun,
  Draft Sharks (Oct 28).
* **Emeka Egbuka (Yahoo Q, Sleeper Q, concussion/foot):** **limited
  Wednesday**, in a non-contact jersey. One Yahoo Sports report lists DNP.
  He is still in the protocol and needs independent neurologist clearance.
  Bowles: he must increase activity Thursday. Missed week 7. Sources: Rotowire,
  CBS Sports, NBC Sports, Draft Sharks (Oct 28).
* **Stefon Diggs (Yahoo Q, Sleeper Q, hand):** **DNP Wednesday**, listed
  "hand/hamstring/rest." Quinn: a veteran rest day, not related to the hand.
  Quinn expects him at full practice Thursday. Sources: Hogs Haven, NBC Sports,
  CBS Sports (Oct 28).
* Everyone else on my roster: no Yahoo or Sleeper designation.

## Projections (Yahoo / Sleeper league_pts)

| Player | Y | S | Opp | Implied | Last 3 wks actual/xFP, targets |
|---|---|---|---|---|---|
| Lamar Jackson | 22 | 22.9 | @ BUF | 25.75 | out wk5–7 |
| Jonathan Taylor | 15 | 16.4 | @ JAX | 18.25 | 21/21, 19/13; 18–21 carries |
| Ollie Gordon II | 11 | 12.9 | vs NE | 18.25 | wk7 17/27, 25 carries |
| Stefon Diggs | 12 | 11.9 | vs PHI | 23.25 | 7, 9, 7 targets |
| Emeka Egbuka | 12 | 11.5 | vs ATL | 23.5 | wk6 16 targets, xFP 25 |
| Omar Cooper Jr. | 9 | 9.8 | vs LV | 23.5 | 7 and 5 targets; 22/11, 22/9 |
| Khalil Shakir | 9 | 9.3 | vs BAL | 28.75 | 8, 3, 6 targets |
| Xavier Worthy | 8 | 9.0 | @ DEN | 21.0 | 7, 7, 6 targets; wk7 4/8 |
| RJ Harvey | 8 | 8.3 | vs KC | 19.5 | wk7 14/4 on 3 carries, 2 targets |
| Courtland Sutton | 9 | 7.3 | vs KC | 19.5 | 3, 3, 5 targets |
| Harold Fannin Jr. | 10 | 10.7 | @ PIT | 18.0 | wk7 9 targets, 13/11 |
| Jake Bates | 8 | 8.5 | vs MIN (indoor) | 24.75 | |
| Browns DEF | 6 | 5.3 | @ PIT | PIT 21.5 | |

## Free agents worth a look

* **QB:** Geno Smith (NYJ vs LV, 19.4 / 19, FA, noon), Kyler Murray (19.4 / 19,
  `W (Oct 31)`), Sam Darnold (17.5 / 19, Mon night, FA). All below Lamar.
* **DEF:** **Commanders** (vs PHI, 7.7 / 7, FA). PHI implied **17.25**, the
  lowest on the slate. Jalen Hurts is on IR (Sleeper, calf) and Tanner McKee
  starts. Chiefs 7.3 / 6 (`W (Oct 31)`). Browns face PIT at 21.5.
* **K:** Shrader 9.2 / 8, Stevens 8.8 / 9. Within 1 of Bates: noise.
* **TE:** Brenton Strange 10.5 / 10 (FA). Equal to Fannin: noise.
* **WR/RB:** nothing above Shakir/Worthy. Wan'Dale Robinson 11.1 / 10 is on
  waivers until Oct 31 and TEN is implied 18.25.

## Lines and weather (ESPN, Open-Meteo)

BAL @ BUF total 54.5 (BAL 25.75, BUF 28.75), 63F, wind 7. NE @ MIA: wind 12,
rain 67%. ATL @ TB: wind 12, rain 53%. PHI @ WAS: wind 5, gusts 15.

# Yahoo Fantasy Sports API — Access Application

Draft answers for https://sports.yahoo.com/developer/access/

> The form is worded for companies, but Yahoo explicitly accepts personal /
> single-league use. Answer as an individual — do **not** invent a company,
> product, or website. A truthful "individual developer, personal tool" is a
> normal approval; a fabricated business is what gets scrutiny.

---

## Business Title

```
Individual Developer
```

Not a corporate title — this is the honest answer for a personal project. If you
would rather use your actual day-job title, that's fine too, but keep the notes
field clear that the app itself is personal and unaffiliated with your employer.

## Business Name

```
<your legal name> (individual — no company)
```

Fill in your own name. The field is required and there's no company behind this,
so your name *is* the entity. "N/A" reads as an incomplete submission, which
Yahoo says they close without correspondence.

## Consumer-Facing Product or App Name

```
Motobowl (personal CLI tool — not publicly distributed)
```

The parenthetical is doing deliberate work: it sets expectations before a
reviewer goes looking for a consumer app that doesn't exist.

## Brief Company Description

```
Not a company. I am an individual developer building a personal command-line
tool for my own use in a single Yahoo fantasy football league. There is no
business entity, no revenue, no customers, and no public distribution — the
tool runs locally on my own laptop, authenticated with my own Yahoo account.
```

## Website or App Store Link

```
https://github.com/ajmaidak
```

You have no public site and `github.com/ajmaidak/motobowl` doesn't exist yet, so
your GitHub profile is the honest, verifiable option — it shows a real developer
behind the request.

**Better, if you're willing:** push the repo public and link it directly
(`https://github.com/ajmaidak/motobowl`). A reviewer who can see a small,
obviously-personal fantasy football script has their answer immediately. Make
sure `.credentials.json` and `.tokens.json` stay gitignored first — they already
are.

---

## Expected Users

```
Small (< 1,000 users)
```

## Client ID

Leave blank. You don't have a YDN app yet; access is provisioned after approval.

## Notes / Details

This is the field the decision actually turns on.

```
Product: Motobowl — a personal command-line tool I am building for my own use
in a single Yahoo fantasy football league (league ID 130450, my team ID 9). It
reads my league's data and generates start/sit and waiver-wire suggestions,
which I then act on by hand in the Yahoo Fantasy app.

Fantasy Sports data required (read-only):
- team/{team_key}/roster — my roster, plus other teams' rosters in the same
  league, for weekly lineup decisions
- league/{league_key}/players;status=FA — free agents and waiver-wire players
- league/{league_key}/settings and /scoreboard — scoring rules and weekly
  matchups, so recommendations reflect my league's actual scoring
- league/{league_key}/transactions — recent adds/drops for league context

Intended user base: Personal, single-league use. I am the only user. The tool
runs locally on my own laptop and authenticates against my own Yahoo account.
It is not distributed, has no public website or hosted service, and does not
redistribute or display Yahoo data to anyone else.

Write access: Not required. Read-only fully covers this use case — every roster
move is made manually in the Yahoo Fantasy app.

Expected request volume: Very low. Roughly a few dozen requests per week during
the NFL season.
```

---

## Before submitting

- [ ] Replace `<your legal name>` in Business Name
- [ ] Confirm team ID 9 matches https://football.fantasysports.yahoo.com/f1/130450/9
- [ ] Decide whether to publish the repo and link it instead of the profile
- [ ] Keep the endpoint list accurate — it's the strongest part of the
      application, and it's easier to have described the real shape up front

## After approval

Create the app on the Yahoo Developer Network with:
- Application Type: **Installed Application**
- Redirect URI: anything URL-shaped (unused — this project uses the `oob` flow)
- API Permissions: **Fantasy Sports → Read**

Then follow the setup steps in README.md.

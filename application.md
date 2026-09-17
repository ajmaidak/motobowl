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
https://github.com/ajmaidak/motobowl
```

The repo is public, so link it directly rather than your profile. A reviewer who
can see a small, obviously-personal fantasy football script has their answer
immediately — this is the single strongest supporting detail in the application.
Verified clean: no credential or token files are committed.

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
Product: Motobowl — a personal command-line tool for my own use in a single
Yahoo fantasy football league (league ID 130450, team ID 9). It reads my
league's data and suggests weekly lineups and waiver pickups, which I then act
on by hand in the Yahoo Fantasy app. Source: github.com/ajmaidak/motobowl

Data required (read-only): rosters for my team and the other teams in my
league, free agents and waivers, league settings and scoreboard, and league
transactions.

Users: Just me — personal, single-league use. It runs locally on my laptop
with my own Yahoo account, is not distributed or hosted, and redistributes no
Yahoo data. Read-only is sufficient; I make every roster move by hand.
Expected volume is a few dozen requests per week during the season.
```

---

## Before submitting

- [ ] Replace `<your legal name>` in Business Name
- [ ] Confirm team ID 9 matches https://football.fantasysports.yahoo.com/f1/130450/9
- [x] Repo published at https://github.com/ajmaidak/motobowl

## After approval

Create the app on the Yahoo Developer Network with:
- OAuth Client Type: **Confidential Client** (Yahoo removed "Installed Application")
- Redirect URI: `https://localhost:8080/callback` (Yahoo rejects `oob`; must match `REDIRECT_URI` in `yahoo_api.py`)
- API Permissions: **Fantasy Sports → Read**

Then follow the setup steps in README.md.

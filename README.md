# Claude Motobowl

League URL: https://football.fantasysports.yahoo.com/f1/130450

Team: https://football.fantasysports.yahoo.com/f1/130450/9

Goals:

* Claude can scrape the Yahoo Fantasy Football API to discover
  * my roster
  * free agents
  * other teams rosters
* Claude can fetch research to recommend
  * Free Agent Pickups
  * Starting Lineups

## Setup

The Yahoo Fantasy Sports API is **read-only** — good enough for recommendations,
but adds/drops and lineup changes still get clicked in Yahoo by hand.

1. **Request API access** at https://sports.yahoo.com/developer/access/ — each
   application is reviewed by the Yahoo Fantasy Sports team, so describe the
   project and note that it's personal / single-league use.
2. **Create the app** on the Yahoo Developer Network:
   * Application Type: **Installed Application**
   * Redirect URI: anything URL-shaped (unused — this script uses the `oob` flow)
   * API Permissions: **Fantasy Sports → Read**
3. **Save the credentials**, either as environment variables:
   ```bash
   export YAHOO_CLIENT_ID=...
   export YAHOO_CLIENT_SECRET=...
   ```
   or in `.credentials.json` (gitignored):
   ```json
   {"client_id": "...", "client_secret": "..."}
   ```
4. **Install deps:**
   ```bash
   python3 -m venv .venv && .venv/bin/pip install -r requirements.txt
   ```

## Usage

```bash
.venv/bin/python roster.py              # my roster, current week
.venv/bin/python roster.py --week 3     # a specific week
.venv/bin/python roster.py --team nfl.l.130450.t.4   # someone else's roster
```

The first run opens Yahoo's consent page and asks you to paste back the code it
displays. Tokens are cached in `.tokens.json` (gitignored) and auto-refresh, so
this only happens once.

## Layout

* `yahoo_api.py` — OAuth2 + token caching, plus helpers for unpacking Yahoo's
  awkward nested JSON
* `roster.py` — lists a team's roster

## Key formats

* League key: `nfl.l.130450`
* Team key: `nfl.l.130450.t.9` (mine)

# Yahoo Fantasy API access, history

Moved out of `CLAUDE.md` on 2026-11-07. The short status lives there. This
file keeps the sequence of events, for when Yahoo support asks.

* **2026-09-16** Access approved: agreement signed, app created (Confidential
  Client), confirmation form submitted. Credentials went into
  `.credentials.json`.
* **2026-09-23** Yahoo's countersigned copy of the Personal Use Agreement
  arrived ("all parties have completed").
* **2026-09-25** Yahoo emailed that access was live, but the original app
  still rejected `fspt-r`. Apps created before Fantasy access is turned on
  cannot be fixed by editing. A **new app** is required. Created one (Fantasy
  Sports: Read only, no OpenID) and put its credentials in `.credentials.json`.
  On the new app `fspt-r` is granted and OAuth login completed (`.tokens.json`
  saved), but every API call, even public `game/nfl`, returns
  **403 "This application is not authorized to perform this action."** That is
  the app not yet enabled on the Fantasy API side. The new Client ID was
  submitted through the application-confirmation form the same day.
* **2026-11-07** Still waiting. No change from Yahoo since 2026-09-25.

## How to test

```bash
.venv/bin/python yahoo_api.py check    # is fspt-r granted? (no login needed)
.venv/bin/python roster.py             # the real test: a live call
```

`check` passing is **not** proof the API works. It passed while every call
still 403'd. Only a successful `roster.py` call is. No re-login is needed once
Yahoo enables the app; the saved token refreshes itself.

`roster.py` is written and its parsing is verified against a mock payload, but
it has **never run against the live API**. Treat its response handling as
unproven. When access lands, the first real call may need fixes to the JSON
shape assumptions in `yahoo_api.py`.

## Why the web session exists

Until the API works, league data comes from Yahoo's web pages through a
logged-in session (`yahoo_web.py`). Scraping is against Yahoo's ToS, so the
web session is a stopgap. Retire it once the API works.

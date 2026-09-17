# data/

Ground truth about the league: parsed Yahoo data for the Moto Bowl.

| File | Contents | Made by |
|---|---|---|
| `my-roster.json` | My roster: slots, projections, injury status, matchups | `yahoo_web.py sync WEEK` |
| `opponent-roster.json` | This week's opponent, with projected total | `yahoo_web.py sync WEEK` |
| `free-agents.json` | Top 50 available per position (free agents + waivers), weekly projections | `yahoo_web.py sync WEEK` |
| `league-settings.json` | Scoring rules, roster slots, waiver config | `parse_settings.py league-settings.txt` |
| `league-settings.txt` | Pasted Scoring & Settings page — the one remaining paste | by hand, rarely |

Refresh everything for a week:

```bash
.venv/bin/python yahoo_web.py sync 2
```

It needs a logged-in Yahoo session cookie in `.yahoo-cookie` — see the docstring
at the top of `yahoo_web.py`. Each file records `meta.week` and `meta.fetched`;
everything here is a point-in-time snapshot, so check both before trusting it.

The per-position roster and free-agent pastes were retired on 2026-09-16 in favor
of the web sync. Once Yahoo API access lands, the sync gets replaced by live API
calls.

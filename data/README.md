# data/

Hand-pasted Yahoo data, used until the API is approved. Paste raw — don't bother
formatting or cleaning it up, the parsing is handled in code.

| File | Paste from | Notes |
|---|---|---|
| `league-settings.txt` | League → Settings | Scoring rules + roster slots. The important part. |
| `my-roster.txt` | My Team | Whole roster incl. bench, with positions and status. |
| `opponent-roster.txt` | Matchups → this week's opponent | Optional, but sharpens start/sit calls. |
| `free-agents.txt` | Players → Free Agents | Optional for now. Sort by rank and grab the top ~40. |

Everything here is a point-in-time snapshot — regenerate before each week's
decisions. Once API access lands, these get replaced by live calls.

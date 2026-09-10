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

## Free agents: one file per position

Yahoo paginates player lists at 25 rows with no page-size control, and it uses a
**different column set per position group** (offense, kickers, defense each get
their own stat columns). So free agents are split by position:

```
data/free-agent-qb.txt    data/free-agent-te.txt    data/free-agent-def.txt
data/free-agent-rb.txt    data/free-agent-k.txt
data/free-agent-wr.txt
```

Any file matching `data/free-agent*.txt` is picked up, so adding a position is
just adding a file.

**Workflow per position:**

1. Players → Free Agents, filter to the position, sort by the column you care
   about.
2. Copy the table. If you want more than the top 25, step pages with the
   `&count=0/25/50/75` URL parameter and paste each page into the **same file**,
   back to back — repeated headers are fine, and de-duplication is by name+team.
3. Merge everything:

   ```bash
   .venv/bin/python free_agents.py
   ```

   Writes `data/free-agents.json` and prints a per-position summary.

**Re-pasting is safe.** On conflict the **most recently modified file wins**, so
re-copying a position picks up the fresher data. This matters because pastes are
taken at different times — a game showing `Q4 1:21, 13-10` in one paste and
`Final W 13-10` in a later one is the same game, and the newer row must win.

Top ~25 per position is plenty for waiver decisions; the tail is players you'd
never start.

**Pick the right stat view before copying.** The default Players view shows
season columns (`GP*`, `Fan Pts`, `Pos Rank`, `Pre-Season`, `Actual`, `% Ros`)
and **no `Proj Pts` column at all**. Weekly projections are what waiver and
start/sit calls actually need, so switch the stat filter to the week's
projections before copying — otherwise the parsed data has no projection to rank
on and falls back to `% Ros` as a crude proxy.

**This goes away once the Yahoo API is approved** — `league/{key}/players;
status=FA;count=25;start=N` paginates in code, no pasting required.

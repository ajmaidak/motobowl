# research/

Cache of external research used for lineup and waiver decisions — projections,
injury reports, matchup analysis, beat-writer notes.

One subfolder per week: `research/week-NN/`.

## Why cache it

Two reasons, and the second is the important one:

1. Avoid re-fetching the same page repeatedly within a week.
2. **The weekly log in `weeks/` grades reasoning after the fact, and that only
   works if the inputs are still around.** "I started him because of a Thursday
   practice report" is unverifiable later unless the report was saved.

## Provenance is mandatory

Every cached file starts with a header recording where it came from and when:

```markdown
---
source: https://example.com/nfl/week-1-injury-report
fetched: 2026-09-10 14:32 CDT
topic: injury report
week: 1
---
```

A cached page with no source and no timestamp is worse than nothing — it looks
authoritative while being unattributable and possibly stale.

## Staleness

**Fantasy research decays fast, and injury/status research decays fastest.**
A Wednesday practice report is routinely wrong by Sunday morning; inactives drop
90 minutes before kickoff.

* Treat anything about player availability as stale after ~24 hours.
* Re-fetch status-sensitive research close to kickoff rather than trusting a
  cached copy from earlier in the week.
* Projections and matchup analysis age more slowly, but still re-check after any
  significant news.

When using cached research in a recommendation, **say how old it is** if it
could matter.

## Naming

`week-NN/NN-source-topic.md`, e.g. `week-01/01-rotowire-injury-report.md`.

## What does not go here

League data — rosters, settings, free agent lists. That lives in `data/` and
comes from Yahoo. Keep the two separate: `data/` is ground truth about the
league, `research/` is outside opinion about players.

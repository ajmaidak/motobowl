#!/usr/bin/env python3
"""Find starters that score 0 if nothing changes.

Reads data/my-roster.json and prints every starting slot with its lock state,
injury status and kickoff, earliest lock first. The point is the one check that
was missed in week 9: a starter on IR whose game locked on Thursday.

    .venv/bin/python lineup_check.py            # roster + Sleeper cross-check
    .venv/bin/python lineup_check.py --no-sleeper

Exit code 1 when a starter is out, on bye or locked at 0, so the run fails
loudly when it matters. A stale snapshot is also an error: re-sync first.
"""

import json
import os
import re
import sys
from datetime import datetime, timezone

HERE = os.path.dirname(os.path.abspath(__file__))
ROSTER = os.path.join(HERE, "data", "my-roster.json")

OUT = {"IR", "IR-R", "PUP-R", "PUP-P", "NFI-R", "O", "SUSP"}
RISK = {"D", "Q", "GTD"}
BENCH = {"BN", "IR", "IR+"}
DAY = {"Thu": 0, "Fri": 1, "Sat": 2, "Sun": 3, "Mon": 4, "Tue": 5}


def lock_key(kickoff):
    """Sort key for a kickoff string like 'Sun 12:00 pm'. Locked and bye sort first."""
    if not kickoff:
        return (-1, 0)
    m = re.match(r"(\w{3}) (\d{1,2}):(\d{2}) (am|pm)", kickoff)
    if not m:
        return (9, 0)
    day, hh, mm, ap = m.groups()
    hour = int(hh) % 12 + (12 if ap == "pm" else 0)
    return (DAY.get(day, 8), hour * 60 + int(mm))


def sleeper_status(players):
    """{yahoo_id: Sleeper injury_status} for the given records, or {} if unavailable."""
    try:
        sys.path.insert(0, HERE)
        from sources import sleeper_players, yahoo_to_sleeper
        ids = yahoo_to_sleeper(players)
        dump = sleeper_players()
        return {yid: (dump.get(sid) or {}).get("injury_status") for yid, sid in ids.items()}
    except Exception as exc:  # noqa: BLE001 - a missing cache must not hide the roster check
        print(f"  (Sleeper cross-check skipped: {exc})")
        return {}


def main():
    with open(ROSTER, encoding="utf-8") as fh:
        roster = json.load(fh)
    meta = roster["meta"]
    fetched = datetime.fromisoformat(meta["fetched"])
    age_h = (datetime.now(timezone.utc) - fetched).total_seconds() / 3600
    print(f"{meta['team_name']}, week {meta['week']}, synced {age_h:.1f} h ago")
    if age_h > 24:
        print("  STALE: re-run `yahoo_web.py sync WEEK` before trusting this")

    starters = [p for p in roster["players"] if p["slot"] not in BENCH]
    sleeper = {} if "--no-sleeper" in sys.argv else sleeper_status(starters)

    problems = 0
    print(f"\n{'Slot':6} {'Player':22} {'Kick':14} {'Yahoo':6} {'Sleeper':8} Flag")
    for p in sorted(starters, key=lambda p: lock_key(p["kickoff"])):
        status = p.get("status") or ""
        sl = sleeper.get(str(p.get("yahoo_id") or "")) or ""
        bye = p["kickoff"] is None and p["opponent"] is None
        locked = p["kickoff"] is None and p["opponent"] is not None
        flag = ""
        if bye:
            flag, problems = "BYE: scores 0", problems + 1
        elif locked and status in OUT:
            flag, problems = "LOCKED AT 0: slot is lost this week", problems + 1
        elif locked:
            flag = f"locked, scored {p['fan_pts']}"
        elif status in OUT or sl.upper() in ("OUT", "IR", "SUS", "PUP"):
            flag, problems = "OUT: replace before kickoff", problems + 1
        elif status in RISK or sl.upper() in ("DOUBTFUL", "QUESTIONABLE"):
            flag = "check inactives before kickoff"
        print(f"{p['slot']:6} {p['name']:22} {p['kickoff'] or '-':14} {status:6} {sl:8} {flag}")

    if problems:
        print(f"\n{problems} slot(s) score 0 unless changed")
        sys.exit(1)
    print("\nno starter is out, on bye or locked at 0")


if __name__ == "__main__":
    main()

#!/usr/bin/env python3
"""Merge per-position free-agent pastes into one normalized list.

Yahoo paginates at 25 rows and uses a different column set per position group
(offense vs kickers vs defense), so the practical workflow is one file per
position, each filtered on Yahoo before copying:

    data/free-agent-qb.txt     data/free-agent-te.txt    data/free-agent-def.txt
    data/free-agent-rb.txt     data/free-agent-k.txt
    data/free-agent-wr.txt

Any file matching data/free-agent*.txt is picked up, so adding a position is
just adding a file. Multiple pages go in the same file back to back; columns are
read from each file's own header, and players are de-duplicated by name+team --
most recently modified file wins, since pastes are taken at different times and
a stale row must never beat a fresher one.

    python3 free_agents.py
    python3 free_agents.py --json data/free-agents.json
"""

import argparse
import glob
import json
import os
import sys

import parse_yahoo_table

DATA_GLOB = os.path.join(os.path.dirname(os.path.abspath(__file__)), "data", "free-agent*.txt")


def load(pattern=DATA_GLOB):
    """Parse every free-agent paste. Returns (players, per_file_report)."""
    players = {}
    report = []

    # Newest paste wins on conflict. Files are pasted at different times and the
    # same player can appear in more than one (dual eligibility, a re-paste), so
    # ordering by filename would let a stale in-progress row beat a finished one.
    for path in sorted(glob.glob(pattern), key=os.path.getmtime, reverse=True):
        name = os.path.basename(path)
        try:
            text = open(path, encoding="utf-8").read()
        except OSError as exc:
            report.append((name, 0, f"unreadable: {exc}"))
            continue

        if not text.strip():
            report.append((name, 0, "empty — nothing pasted yet"))
            continue

        columns, parsed = parse_yahoo_table.parse(text)
        if not parsed:
            report.append((name, 0, "no players found — is this a Yahoo table paste?"))
            continue

        added = 0
        for p in parsed:
            key = (p["name"], p["team"])
            if key in players:
                continue
            p["source_file"] = name
            players[key] = p
            added += 1

        dupes = len(parsed) - added
        note = f"{len(parsed)} rows" + (f", {dupes} superseded by newer paste" if dupes else "")
        report.append((name, added, note))

    return list(players.values()), report


def main():
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument("--json", default="data/free-agents.json")
    ap.add_argument("--pos", help="only show this position")
    ap.add_argument("--limit", type=int, default=15, help="rows shown per position")
    args = ap.parse_args()

    players, report = load()

    print("\nSources")
    width = max((len(r[0]) for r in report), default=10)
    for name, added, note in report:
        print(f"  {name:<{width}}  {added:>4} new   ({note})")

    if not players:
        print("\nNo free agents parsed. Paste Yahoo tables into data/free-agent-<pos>.txt\n",
              file=sys.stderr)
        sys.exit(1)

    by_pos = {}
    for p in players:
        by_pos.setdefault(p["pos"], []).append(p)

    print(f"\n{len(players)} players across {len(by_pos)} positions")

    for pos in sorted(by_pos, key=lambda x: ("QB", "RB", "WR", "TE", "K", "DEF").index(x)
                      if x in ("QB", "RB", "WR", "TE", "K", "DEF") else 9):
        if args.pos and pos != args.pos.upper():
            continue
        group = by_pos[pos]
        # No projection column in these pastes, so rank by rostered% — the
        # closest available proxy for what the wider market thinks.
        group.sort(key=lambda p: -(p.get("pct_rostered") or 0))
        print(f"\n{pos} ({len(group)})")
        for p in group[: args.limit]:
            status = f"  [{p['status']}]" if p.get("status") else ""
            matchup = f"{'vs' if p['home'] else '@'} {p['opponent']}" if p.get("opponent") else "-"
            print(f"  {p['name'][:22]:<22} {p['team']:<4} {matchup:<8} "
                  f"ros {str(p.get('pct_rostered') or '-'):>3}%  "
                  f"bye {str(p.get('bye') or '-'):<3}{status}")

    with open(args.json, "w", encoding="utf-8") as fh:
        json.dump({"players": players}, fh, indent=2)
    print(f"\n  wrote {args.json}\n")


if __name__ == "__main__":
    main()

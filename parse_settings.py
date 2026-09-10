#!/usr/bin/env python3
"""Parse Yahoo league Scoring & Settings copy-paste into structured JSON.

This paste is tab-delimited key/value, but scoring rules that differ from
Yahoo's defaults break across three lines:

    Passing Touchdowns
    Yahoo Default
    <tab>6<tab>4

...where the trailing 4 is Yahoo's default and 6 is what this league uses.
Those overrides are exactly the rules worth surfacing, so they get tracked.

Usage:
    python3 parse_settings.py data/league-settings.txt --json data/league-settings.json
"""

import argparse
import json
import re
import sys

SECTION_HEADERS = {
    "Offense": "offense",
    "Kickers": "kickers",
    "Defense/Special Teams": "dst",
}

# "25 yards per point" -> points are earned per N yards, not per yard.
PER_POINT_RE = re.compile(r"^(\d+(?:\.\d+)?)\s+yards? per point$", re.I)


def to_value(raw):
    if raw in ("", "-", "–"):
        return None
    per_point = PER_POINT_RE.match(raw)
    if per_point:
        return {"yards_per_point": float(per_point.group(1))}
    try:
        return float(raw) if "." in raw else int(raw)
    except ValueError:
        return raw


def parse(text):
    league = {}
    scoring = {"offense": {}, "kickers": {}, "dst": {}}
    overrides = []
    section = None
    pending = None  # a rule name awaiting its values on a later line

    for raw_line in text.splitlines():
        if not raw_line.strip():
            continue

        parts = [p.strip() for p in raw_line.split("\t")]
        head = parts[0]

        # Section header row, e.g. "Offense | League Value | Yahoo Default Value"
        if head in SECTION_HEADERS and len(parts) > 1 and "League Value" in parts[1]:
            section = SECTION_HEADERS[head]
            pending = None
            continue

        # A lone "Yahoo Default" marker just flags that an override follows.
        if head == "Yahoo Default" and len(parts) == 1:
            continue

        # Line starting with a tab: values belonging to the pending rule name.
        if head == "" and pending and len(parts) > 1:
            value = to_value(parts[1])
            default = to_value(parts[2]) if len(parts) > 2 else None
            if section:
                scoring[section][pending] = value
                if default is not None:
                    overrides.append(
                        {"rule": pending, "league": value, "yahoo_default": default}
                    )
            pending = None
            continue

        # A bare name with no values yet.
        if len(parts) == 1:
            if section:
                pending = head
            continue

        # Normal "Key \t Value [\t Default]" row.
        key = head.rstrip(":")
        value = to_value(parts[1])

        if section:
            default = to_value(parts[2]) if len(parts) > 2 else None
            scoring[section][key] = value
            if default is not None:
                overrides.append({"rule": key, "league": value, "yahoo_default": default})
        else:
            league[key] = value
        pending = None

    return league, scoring, overrides


def roster_slots(league):
    raw = league.get("Roster Positions") or ""
    return [s.strip() for s in str(raw).split(",") if s.strip()]


def describe_ppr(scoring):
    rec = scoring["offense"].get("Receptions")
    if rec == 1:
        return "Full PPR (1.0 per reception)"
    if rec == 0.5:
        return "Half PPR (0.5 per reception)"
    if not rec:
        return "Standard (no PPR)"
    return f"{rec} per reception"


def print_summary(league, scoring, overrides):
    name = league.get("League Name", "League")
    print(f"\n{name} (ID {league.get('League ID#')})")
    print("=" * (len(str(name)) + 16))

    slots = roster_slots(league)
    starters = [s for s in slots if s not in ("BN", "IR", "IR+")]
    bench = [s for s in slots if s == "BN"]

    print("\nFORMAT")
    rows = [
        ("Scoring type", f"{league.get('Scoring Type')}, max {league.get('Max Teams')} teams"),
        ("Reception scoring", describe_ppr(scoring)),
        ("Fractional points", league.get("Fractional Points")),
        ("Negative points", league.get("Negative Points")),
        ("Starters", ", ".join(starters)),
        ("Bench", f"{len(bench)} spots"),
    ]
    for label, value in rows:
        print(f"  {label:<18} {value}")

    print("\nDIFFERS FROM YAHOO DEFAULT")
    if overrides:
        width = max(len(o["rule"]) for o in overrides)
        for o in overrides:
            print(f"  {o['rule']:<{width}}  {o['league']:>5}   (default {o['yahoo_default']})")
    else:
        print("  (none — standard Yahoo scoring)")

    print("\nWAIVERS & TRADES")
    print(f"  Waiver type      {league.get('Waiver Type')}")
    print(f"  Waiver period    {league.get('Waiver Time')}")
    print(f"  Weekly waivers   {league.get('Weekly Waivers')}")
    print(f"  Acquisitions     {league.get('Max Acquisitions per Week')} per week, "
          f"{league.get('Max Acquisitions for Entire Season')} per season")
    print(f"  Trade deadline   {league.get('Trade End Date')}")

    print("\nPLAYOFFS")
    print(f"  {league.get('Playoffs')}")
    print()


def main():
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument("path")
    ap.add_argument("--json")
    args = ap.parse_args()

    with open(args.path, encoding="utf-8") as fh:
        league, scoring, overrides = parse(fh.read())

    if not league:
        print("error: no settings parsed", file=sys.stderr)
        sys.exit(1)

    print_summary(league, scoring, overrides)

    if args.json:
        payload = {
            "league": league,
            "roster_positions": roster_slots(league),
            "scoring": scoring,
            "non_default_rules": overrides,
        }
        with open(args.json, "w", encoding="utf-8") as fh:
            json.dump(payload, fh, indent=2)
        print(f"  wrote {args.json}\n")


if __name__ == "__main__":
    main()

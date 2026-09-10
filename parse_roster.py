#!/usr/bin/env python3
"""Parse a roster copy-pasted from the Yahoo Fantasy web UI into structured JSON.

Yahoo's table copies one cell per line with tab-only separator lines between
them, so a roster arrives as ~965 lines of noise. The underlying record is
strictly ordered, though: a lineup-slot token, a three-line player block, then
ten value columns, then a run of per-position stat columns we don't need.

Usage:
    python3 parse_roster.py data/my-roster.txt
    python3 parse_roster.py data/my-roster.txt --json data/my-roster.json
"""

import argparse
import json
import re
import sys

# Lineup slots Yahoo emits in the Pos column. Anything else starting a record
# means the layout changed and we should notice rather than silently skip.
SLOTS = {
    "QB", "RB", "WR", "TE", "K", "DEF",
    "W/R", "W/T", "W/R/T", "Q/W/R/T",
    "BN", "IR", "IR+", "NA",
}

STARTING_SLOTS = ["QB", "RB", "WR", "TE", "W/R", "W/T", "W/R/T", "Q/W/R/T", "K", "DEF"]

# " Bal - QB" / " Pit - DEF" at the end of the second player line.
TEAM_POS_RE = re.compile(r"\s([A-Za-z]{2,3})\s-\s(QB|RB|WR|TE|K|DEF)\s*$")
# "Sun 12:00 pm @ Ind" / "Mon 7:15 pm vs Atl"
GAME_RE = re.compile(r"^(\w{3})\s+(\d{1,2}:\d{2}\s*[ap]m)\s+(@|vs)\s+([A-Za-z]{2,3})", re.I)
# "Team Auto Pick's Kickers roster for week 1."
WEEK_RE = re.compile(r"^(.*?)'s .* roster for week (\d+)", re.I)

# The ten value columns that follow the player block, in order.
VALUE_FIELDS = [
    "bye", "fan_pts", "proj_pts", "proj_max", "proj_min",
    "pos_rank", "pct_start", "pct_start_top", "pct_rostered", "pct_rostered_top",
]


def clean_lines(text):
    """Drop blank and tab-only lines; strip the rest."""
    return [ln.strip() for ln in text.splitlines() if ln.strip()]


def to_number(raw):
    """Yahoo uses '-' and en-dash '–' for empty, and '%' suffixes."""
    if raw in ("-", "–", "—", ""):
        return None
    value = raw.replace("%", "").replace(",", "")
    try:
        return float(value) if "." in value else int(value)
    except ValueError:
        return raw


def parse(text):
    lines = clean_lines(text)
    players = []
    meta = {}
    i = 0

    while i < len(lines):
        line = lines[i]

        week_match = WEEK_RE.match(line)
        if week_match:
            meta.setdefault("team_name", week_match.group(1))
            meta.setdefault("week", int(week_match.group(2)))
            i += 1
            continue

        if line not in SLOTS:
            i += 1
            continue

        # A slot token starts a player record. Need at least the 3-line block.
        if i + 3 >= len(lines):
            break

        slot = line
        name = lines[i + 1]
        detail = lines[i + 2]

        team_pos = TEAM_POS_RE.search(detail)
        if not team_pos:
            # Not actually a player record (a stat column that collided with a
            # slot name, say). Skip the token and carry on.
            i += 1
            continue

        player = {
            "slot": slot,
            "name": name,
            "team": team_pos.group(1).upper(),
            "pos": team_pos.group(2),
            "opponent": None,
            "home": None,
            "kickoff": None,
        }

        cursor = i + 3
        game = GAME_RE.match(lines[cursor]) if cursor < len(lines) else None
        if game:
            player["kickoff"] = f"{game.group(1)} {game.group(2)}"
            player["home"] = game.group(3).lower() == "vs"
            player["opponent"] = game.group(4).upper()
            cursor += 1

        # Ten value columns, then stat columns we ignore.
        for field in VALUE_FIELDS:
            if cursor >= len(lines) or lines[cursor] in SLOTS:
                break
            player[field] = to_number(lines[cursor])
            cursor += 1

        players.append(player)
        i = cursor

    return meta, players


def slot_key(player):
    slot = player["slot"]
    rank = STARTING_SLOTS.index(slot) if slot in STARTING_SLOTS else 90
    return (rank, -(player.get("proj_pts") or 0))


def print_roster(meta, players):
    title = meta.get("team_name", "Roster")
    if meta.get("week"):
        title += f" — week {meta['week']}"
    print(f"\n{title}")
    print("=" * len(title))

    starters = [p for p in players if p["slot"] in STARTING_SLOTS]
    bench = [p for p in players if p["slot"] not in STARTING_SLOTS]

    name_w = max(len(p["name"]) for p in players)
    for group, label in ((starters, "STARTERS"), (bench, "BENCH")):
        if not group:
            continue
        print(f"\n{label}")
        for p in sorted(group, key=slot_key):
            matchup = ""
            if p["opponent"]:
                matchup = f"{'vs' if p['home'] else '@'} {p['opponent']:<4}"
            proj = p.get("proj_pts")
            rng = ""
            if p.get("proj_min") is not None and p.get("proj_max") is not None:
                rng = f"({p['proj_min']}–{p['proj_max']})"
            print(
                f"  {p['slot']:<6} {p['name']:<{name_w}}  {p['pos']:<3} {p['team']:<4} "
                f"{matchup:<9} bye {str(p.get('bye') or '-'):<3} "
                f"proj {str(proj if proj is not None else '-'):>4} {rng:<8} "
                f"start {str(p.get('pct_start') or 0):>3}%"
            )

    total = sum(p.get("proj_pts") or 0 for p in starters)
    print(f"\n  {len(players)} players parsed — {len(starters)} starting, {len(bench)} bench")
    print(f"  Projected starter total: {total}\n")


def main():
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument("path", help="pasted Yahoo roster text file")
    ap.add_argument("--json", help="also write structured JSON here")
    args = ap.parse_args()

    with open(args.path, encoding="utf-8") as fh:
        meta, players = parse(fh.read())

    if not players:
        print("error: no players parsed — the paste layout may have changed", file=sys.stderr)
        sys.exit(1)

    print_roster(meta, players)

    if args.json:
        with open(args.json, "w", encoding="utf-8") as fh:
            json.dump({"meta": meta, "players": players}, fh, indent=2)
        print(f"  wrote {args.json}\n")


if __name__ == "__main__":
    main()

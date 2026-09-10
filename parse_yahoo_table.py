#!/usr/bin/env python3
"""Generic parser for any Yahoo Fantasy table copy-paste.

The roster page, the free-agent page and the player-search page all copy in the
same shape: a header block of column labels, then one cell per line with
tab-only separators. The columns differ per page and per stat filter, so this
derives them from the header rather than hardcoding positions.

Each player row looks like:

    <lineup slot, only on roster pages>
    Player Name
    Player NameVideo ForecastPlayer Note Buf - WR     <- team/pos anchor
    Sun 12:00 pm @ Hou                                <- or "Bye"/blank
    <value cells, one per remaining column>

Free-agent exports paginate at 25 players. Paste each page into the same file
one after another — repeated header blocks are handled, and players are
de-duplicated by name+team.

Usage:
    python3 parse_yahoo_table.py data/free-agents.txt --json data/free-agents.json
"""

import argparse
import json
import re
import sys

TEAM_POS_RE = re.compile(r"\s([A-Za-z]{2,3})\s-\s(QB|RB|WR|TE|K|DEF)\s*$")
# Yahoo writes the game cell several ways depending on game state:
#   scheduled    "Sun 3:25 pm vs GB"
#   in progress  "Q4 1:21, 13-10 vs NE"
#   final        "W 20-17 @ NE"
# Anchoring on the trailing "vs TEAM" / "@ TEAM" catches all of them; anchoring
# on the leading day-and-time silently mis-columns live and finished games.
GAME_RE = re.compile(r"^(.*?)(@|vs)\s+([A-Za-z]{2,3})\s*$", re.I)
SCHEDULED_RE = re.compile(r"^(\w{3})\s+(\d{1,2}:\d{2}\s*[ap]m)\s*$", re.I)
# Injury/roster designations sit between the name and the note markers, e.g.
# "Zach CharbonnetPUP-RPlayer Note Sea - RB".
STATUS_RE = re.compile(r"^(PUP-R|PUP-P|NFI-R|IR-R|IR|SUSP|GTD|Q|D|O|NA)(?=Video|Player|New|No )")
SLOTS = {"QB", "RB", "WR", "TE", "K", "DEF", "W/R", "W/T", "W/R/T", "Q/W/R/T", "BN", "IR", "IR+", "NA"}

# Header labels that mark the start of a column block, in the order Yahoo emits.
KNOWN_HEADERS = {
    "Pos", "Offense", "Kickers", "Defense/Special Teams", "Players", "Player",
    "Owner", "Action", "Bye", "Fan Pts", "Proj Pts", "Proj Max", "Proj Min",
    "Pos Rank", "% Start", "% Ros", "Pre-Season", "Current", "% Owned",
}

# Column labels we care about, normalized to snake_case keys.
COLUMN_ALIASES = {
    "Bye": "bye",
    "Fan Pts": "fan_pts",
    "Proj Pts": "proj_pts",
    "Proj Max": "proj_max",
    "Proj Min": "proj_min",
    "Pos Rank": "pos_rank",
    "% Start": "pct_start",
    "% Ros": "pct_rostered",
    "% Owned": "pct_rostered",
    "Owner": "owner",
}


# Yahoo's copy embeds private-use glyphs (icons for video, notes, sort arrows)
# that survive the paste, e.g. "Sun 3:25 pm vs GB\ue231". They break any regex
# anchored to end-of-line, so strip them before anything else looks at the text.
JUNK_RE = re.compile(r"[\ue000-\uf8ff\u200b-\u200f\ufeff]")


def clean_lines(text):
    lines = (JUNK_RE.sub("", ln).strip() for ln in text.splitlines())
    return [ln for ln in lines if ln]


def to_number(raw):
    if raw in ("-", "–", "—", ""):
        return None
    value = raw.replace("%", "").replace(",", "")
    try:
        return float(value) if "." in value else int(value)
    except ValueError:
        return raw


def find_player_rows(lines):
    """Index of every line that is a team/pos anchor — one per player."""
    return [i for i, ln in enumerate(lines) if TEAM_POS_RE.search(ln)]


def extract_headers(lines, first_player_idx):
    """Column labels appearing before the first player row.

    Yahoo repeats a '% Start' style label with a diamond suffix for its premium
    column; both are kept so positional alignment with the value cells holds.
    """
    headers = []
    # first_player_idx is the team/pos anchor; the line before it is the player
    # name, which is not a column label.
    for ln in lines[: max(0, first_player_idx - 1)]:
        if ln in SLOTS:
            continue
        headers.append(ln)
    return headers


def value_columns(headers):
    """Header labels that correspond to value cells, i.e. everything after the
    player-name column."""
    out = []
    seen_name_col = False
    for h in headers:
        if h in ("Offense", "Kickers", "Defense/Special Teams", "Players", "Player"):
            seen_name_col = True
            continue
        if h == "Pos":
            continue
        if seen_name_col:
            out.append(h)
    return out


def parse(text):
    lines = clean_lines(text)
    anchors = find_player_rows(lines)
    if not anchors:
        return [], []

    headers = value_columns(extract_headers(lines, anchors[0]))
    players = []

    for n, idx in enumerate(anchors):
        team_pos = TEAM_POS_RE.search(lines[idx])
        name = lines[idx - 1] if idx > 0 else "?"

        slot = None
        if idx >= 2 and lines[idx - 2] in SLOTS:
            slot = lines[idx - 2]

        player = {
            "name": name,
            "team": team_pos.group(1).upper(),
            "pos": team_pos.group(2),
            "slot": slot,
            "opponent": None,
            "home": None,
            "kickoff": None,
            "status": None,
        }

        cursor = idx + 1
        stop = anchors[n + 1] - 1 if n + 1 < len(anchors) else len(lines)

        # Injury/roster designation, if Yahoo emitted one.
        remainder = lines[idx][len(name):] if lines[idx].startswith(name) else lines[idx]
        status = STATUS_RE.match(remainder)
        player["status"] = status.group(1) if status else None

        if cursor < stop:
            game = GAME_RE.match(lines[cursor])
            if game:
                prefix = game.group(1).strip().rstrip(",").strip()
                player["home"] = game.group(2).lower() == "vs"
                player["opponent"] = game.group(3).upper()
                scheduled = SCHEDULED_RE.match(prefix)
                player["kickoff"] = prefix if scheduled else None
                # "Q4 1:21, 13-10" or "W 20-17" — game already under way.
                player["game_state"] = None if scheduled else (prefix or None)
                cursor += 1
            elif lines[cursor].lower().startswith("bye"):
                player["on_bye"] = True
                cursor += 1

        values = []
        while cursor < stop:
            cell = lines[cursor]
            if cell in KNOWN_HEADERS or cell in SLOTS:
                break  # a repeated header block from the next pasted page
            values.append(cell)
            cursor += 1

        for label, raw in zip(headers, values):
            key = COLUMN_ALIASES.get(label)
            if key and key not in player:
                player[key] = to_number(raw)
        player["_raw_values"] = values

        players.append(player)

    # De-duplicate across pasted pages, keeping the first occurrence.
    seen = set()
    unique = []
    for p in players:
        key = (p["name"], p["team"])
        if key in seen:
            continue
        seen.add(key)
        unique.append(p)

    return headers, unique


def main():
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument("path")
    ap.add_argument("--json")
    ap.add_argument("--limit", type=int, default=40)
    args = ap.parse_args()

    with open(args.path, encoding="utf-8") as fh:
        text = fh.read()

    if not text.strip():
        print(f"error: {args.path} is empty — paste the Yahoo table into it first",
              file=sys.stderr)
        sys.exit(1)

    headers, players = parse(text)
    if not players:
        print("error: no players found — is this a Yahoo table paste?", file=sys.stderr)
        sys.exit(1)

    print(f"\ncolumns detected: {', '.join(headers) if headers else '(none)'}")
    print(f"players parsed:   {len(players)}\n")

    name_w = min(24, max(len(p["name"]) for p in players))
    for p in sorted(players, key=lambda x: -(x.get("proj_pts") or 0))[: args.limit]:
        matchup = f"{'vs' if p['home'] else '@'} {p['opponent']}" if p["opponent"] else "-"
        print(f"  {p['name'][:name_w]:<{name_w}} {p['pos']:<3} {p['team']:<4} "
              f"{matchup:<8} proj {str(p.get('proj_pts') or '-'):>4}  "
              f"ros {str(p.get('pct_rostered') or '-'):>4}%")

    if args.json:
        with open(args.json, "w", encoding="utf-8") as fh:
            json.dump({"columns": headers, "players": players}, fh, indent=2)
        print(f"\n  wrote {args.json}\n")


if __name__ == "__main__":
    main()

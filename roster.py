#!/usr/bin/env python3
"""List my Yahoo fantasy football roster.

Usage:
    python3 roster.py                 # current week, my team
    python3 roster.py --week 3
    python3 roster.py --team nfl.l.130450.t.4
"""

import argparse

import yahoo_api

# From the league/team URLs in README.md.
LEAGUE_KEY = "nfl.l.130450"
MY_TEAM_KEY = "nfl.l.130450.t.9"

# Starters first in the usual lineup order, then the bench and inactives.
POSITION_ORDER = [
    "QB", "WR", "RB", "TE", "W/R", "W/R/T", "W/T", "Q/W/R/T",
    "K", "DEF", "BN", "IR", "IR+", "NA",
]


def position_sort_key(slot):
    return (POSITION_ORDER.index(slot) if slot in POSITION_ORDER else 99, slot)


def fetch_roster(team_key, week=None):
    path = f"team/{team_key}/roster"
    if week:
        path += f";week={week}"
    payload = yahoo_api.get(path)

    team = yahoo_api.find_key(payload, "team")
    if team is None:
        yahoo_api.die("no team in response — check the team key")
    team_meta = yahoo_api.flatten(team)

    roster = yahoo_api.find_key(team, "roster") or {}
    players_node = yahoo_api.find_key(roster, "players") or {}

    players = []
    for raw in yahoo_api.numbered_items(players_node, "player"):
        p = yahoo_api.flatten(raw)
        slot = (p.get("selected_position") or {}).get("position", "?")
        players.append(
            {
                "slot": slot,
                "name": (p.get("name") or {}).get("full", "?"),
                "team": p.get("editorial_team_abbr", "").upper(),
                "pos": p.get("display_position", ""),
                "bye": (p.get("bye_weeks") or {}).get("week", ""),
                "status": p.get("status", ""),
            }
        )

    players.sort(key=lambda p: position_sort_key(p["slot"]))
    return team_meta, roster, players


def print_roster(team_meta, roster, players):
    name = team_meta.get("name", "My team")
    week = roster.get("week")
    header = f"{name}"
    if week:
        header += f" — week {week}"
    print(f"\n{header}")
    print("=" * len(header))

    if not players:
        print("(no players returned)")
        return

    widths = {
        "slot": max(4, max(len(p["slot"]) for p in players)),
        "name": max(6, max(len(p["name"]) for p in players)),
        "pos": max(3, max(len(p["pos"]) for p in players)),
    }

    bench_seen = False
    for p in players:
        # Blank line between the starting lineup and everyone else.
        if not bench_seen and p["slot"] in ("BN", "IR", "IR+", "NA"):
            print()
            bench_seen = True
        status = f"  [{p['status']}]" if p["status"] else ""
        bye = f"bye {p['bye']}" if p["bye"] else ""
        print(
            f"{p['slot']:<{widths['slot']}}  "
            f"{p['name']:<{widths['name']}}  "
            f"{p['pos']:<{widths['pos']}}  "
            f"{p['team']:<4} {bye}{status}"
        )
    print()


def main():
    parser = argparse.ArgumentParser(description="List a Yahoo fantasy football roster.")
    parser.add_argument("--team", default=MY_TEAM_KEY, help=f"team key (default {MY_TEAM_KEY})")
    parser.add_argument("--week", type=int, help="week number (default: current)")
    args = parser.parse_args()

    try:
        team_meta, roster, players = fetch_roster(args.team, args.week)
    except yahoo_api.AuthError as exc:
        yahoo_api.die(str(exc))
    except RuntimeError as exc:
        yahoo_api.die(str(exc))

    print_roster(team_meta, roster, players)


if __name__ == "__main__":
    main()

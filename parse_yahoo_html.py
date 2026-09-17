#!/usr/bin/env python3
"""Parse Yahoo Fantasy web pages (as fetched by yahoo_web.py) into player records.

Replaces the paste parsers. The HTML is far more reliable than a paste:

* Columns come from each header's `title` attribute ("Projected Points",
  "Rushing Yards"), which is unambiguous where the visible labels repeat
  ("Yds", "TD").
* Players carry Yahoo's player id (`data-ys-playerid`). Sleeper's `yahoo_id` is
  sparse (5 of 16 roster players on 2026-09-16), so it is not yet a reliable
  join to Sleeper on its own.
* Injury designations are their own element, not glued onto the name.

Records are normalized to (slot, name,
team, pos, opponent, home, kickoff, status, bye, fan_pts, proj_pts, ...), plus
`yahoo_id`, `opp_rank` (where the opponent ranks in points allowed to this
position, 1 = gives up the most) and `stats` (every other column, by title).

    python3 parse_yahoo_html.py cache/yahoo/roster_w2.html
"""

import json
import re
import sys

from bs4 import BeautifulSoup

# Yahoo writes the game cell differently depending on game state:
#   scheduled    "Sun 3:25 pm vs GB"
#   in progress  "Q4 1:21, 13-10 vs NE"
#   final        "W 20-17 @ NE"
# Anchor on the trailing "vs TEAM" / "@ TEAM", which all three share.
GAME_RE = re.compile(r"^(.*?)(@|vs)\s+([A-Za-z]{2,3})\s*$", re.I)
SCHEDULED_RE = re.compile(r"^(\w{3})\s+(\d{1,2}:\d{2}\s*[ap]m)\s*$", re.I)
JUNK_RE = re.compile(r"[\ue000-\uf8ff\u200b-\u200f\ufeff]")  # Yahoo icon glyphs, zero-width chars

# Header title -> normalized field. Anything not listed goes into `stats`.
COLUMNS = {
    "Bye Week": "bye",
    "Fantasy Points": "fan_pts",
    "Projected Points": "proj_pts",
    "Projected Max": "proj_max",
    "Projected Min": "proj_min",
    "Position Rank": "pos_rank",
    "Percent Started": "pct_start",
    "Percent player is rostered in Yahoo leagues": "pct_rostered",
    "Roster Status": "roster_status",
    "Games Played": "games_played",
}
# Columns that are layout, not data.
SKIP = {"", "Position", "Edit", "Offense", "Kickers", "Defense/Special Teams",
        "% Started by Yahoo Diamond level users",
        "Percent Rostered vs. Yahoo Diamond level users"}

OPP_RANK_RE = re.compile(r"gives up the (\d+)\w{2} (most|fewest)")
CAPTION_RE = re.compile(r"^(.*)'s .+ roster for week (\d+)")


class ParseError(Exception):
    pass


def text(el):
    if el is None:
        return ""
    raw = JUNK_RE.sub("", el.get_text(" ", strip=True)).replace("\xa0", " ")
    return re.sub(r"\s+", " ", raw).strip()


def to_value(raw):
    raw = raw.strip()
    if raw in ("", "-", "–", "—"):
        return None
    num = raw.replace(",", "").rstrip("%")
    try:
        return int(num)
    except ValueError:
        try:
            return float(num)
        except ValueError:
            return raw


def parse_player_cell(td):
    """Identity, injury status and game from a player <td>."""
    link = td.select_one("a.name")
    if link is None:
        return None  # empty lineup slot
    team_pos = text(td.select_one("span.D-b span.Fz-xxs"))
    m = re.match(r"^([A-Za-z]{2,3}) - (QB|RB|WR|TE|K|DEF)$", team_pos)
    if not m:
        raise ParseError(f"no team/position for {text(link)!r}: {team_pos!r}")

    player = {
        "name": text(link),
        "yahoo_id": link.get("data-ys-playerid"),
        "team": m.group(1).upper(),
        "pos": m.group(2),
        "status": text(td.select_one(".F-injury")) or None,
        "opponent": None,
        "home": None,
        "kickoff": None,
        "game_state": None,
        "opp_rank": None,
    }

    game = text(td.select_one(".ysf-game-status"))
    g = GAME_RE.match(game)
    if g:
        prefix = g.group(1).strip().rstrip(",").strip()
        player["home"] = g.group(2).lower() == "vs"
        player["opponent"] = g.group(3).upper()
        if SCHEDULED_RE.match(prefix):
            player["kickoff"] = prefix
        else:
            player["game_state"] = prefix or None
    elif game.lower().startswith("bye"):
        player["on_bye"] = True

    rank = td.select_one(".ysf-game-status a[title*='gives up']")
    if rank:
        r = OPP_RANK_RE.search(rank["title"])
        if r:
            n = int(r.group(1))
            player["opp_rank"] = n if r.group(2) == "most" else 33 - n
    return player


def header_titles(table):
    rows = table.select("thead tr")
    if not rows:
        raise ParseError("table has no header")
    return [JUNK_RE.sub("", th.get("title") or text(th)).strip()
            for th in rows[-1].find_all("th")]


def parse_stat_table(table):
    """Roster and player-list tables: one player per row, columns by title."""
    titles = header_titles(table)
    players = []
    for tr in table.select("tbody > tr"):
        cells = tr.find_all("td", recursive=False)
        if len(cells) != len(titles):
            raise ParseError(f"row has {len(cells)} cells, header has {len(titles)}")
        player_td = tr.select_one("td.player") or next(
            (td for td in cells if td.select_one("a.name")), None)
        player = parse_player_cell(player_td) if player_td else None
        if player is None:
            continue
        slot = tr.select_one("td.pos .pos-label")
        player["slot"] = text(slot) or None if slot else None
        stats = {}
        for title, td in zip(titles, cells):
            if td is player_td or title in SKIP:
                continue
            value = to_value(text(td))
            if title in COLUMNS:
                player[COLUMNS[title]] = value
            else:
                stats[title] = value
        player["stats"] = stats
        players.append(player)
    return players


def parse_roster(html):
    soup = BeautifulSoup(html, "html.parser")
    tables = soup.select("table[id^=statTable].ysf-rosterswapper")
    if not tables:
        raise ParseError("no roster tables — not a My Team page, or the layout changed")
    cap = CAPTION_RE.match(text(tables[0].find("caption")))
    if not cap:
        raise ParseError("roster caption missing team name / week")
    players = [p for t in tables for p in parse_stat_table(t)]
    if not players:
        raise ParseError("roster tables contained no players")
    return {"meta": {"team_name": cap.group(1), "week": int(cap.group(2))},
            "players": players}


def selected_stat_view(soup):
    opt = soup.select_one("select[name=stat1] option[selected]")
    return (opt.get("value"), text(opt)) if opt else (None, None)


def parse_players(html):
    """Players page (free agents). In a projected view (e.g. 'Week 2 (proj)'),
    the 'Fantasy Points' column is the projection, so it is moved to proj_pts."""
    soup = BeautifulSoup(html, "html.parser")
    table = soup.select_one("table.Table-interactive")
    if table is None:
        raise ParseError("no player list table — not a Players page, or the layout changed")
    code, label = selected_stat_view(soup)
    players = parse_stat_table(table)
    projected = bool(code and code.startswith("S_P"))
    for p in players:
        if projected:
            p["proj_pts"], p["fan_pts"] = p.get("fan_pts"), None
    return {"meta": {"stat_view": code, "stat_view_label": label,
                     "projected": projected},
            "players": players}


def parse_matchup(html):
    """Matchup page: two lineups side by side. Returns {'me': ..., 'opponent': ...}."""
    soup = BeautifulSoup(html, "html.parser")
    tables = soup.select("table.Datatable[id^=statTable]")
    if not tables:
        raise ParseError("no matchup tables — not a Matchup page, or the layout changed")

    # The matchup header links both teams by absolute URL, mine first; the
    # nav's relative "/f1/<league>/<team>" link is labelled "My Team".
    teams = []
    for a in soup.select("a[href^='https://'][href*='/f1/']"):
        m = re.search(r"/f1/\d+/(\d+)$", a["href"])
        name = text(a)
        if m and name and m.group(1) not in [t[0] for t in teams]:
            teams.append((m.group(1), name))
    if len(teams) != 2:
        raise ParseError("could not find both team names on the matchup page")

    sides = {0: [], 1: []}
    for table in tables:
        titles = header_titles(table)
        if titles.count("Player") != 2:
            raise ParseError(f"unexpected matchup header: {titles}")
        left, right = [i for i, t in enumerate(titles) if t == "Player"]
        for tr in table.select("tbody > tr"):
            cells = tr.find_all("td", recursive=False)
            if len(cells) != len(titles):
                raise ParseError(f"row has {len(cells)} cells, header has {len(titles)}")
            slot = text(cells[len(titles) // 2]) or None
            for side, idx, step in ((0, left, 1), (1, right, -1)):
                player = parse_player_cell(cells[idx])
                if player is None:
                    continue
                player["slot"] = slot
                player["proj_pts"] = to_value(text(cells[idx + step]))
                player["fan_pts"] = to_value(text(cells[idx + 2 * step]))
                sides[side].append(player)

    def side(n):
        starters = [p for p in sides[n] if p["slot"] not in ("BN", "IR", "IR+")]
        return {"meta": {"team_id": int(teams[n][0]), "team_name": teams[n][1],
                         "proj_total": sum(p["proj_pts"] or 0 for p in starters),
                         "fan_total": sum(p["fan_pts"] or 0 for p in starters)},
                "players": sides[n]}

    return {"me": side(0), "opponent": side(1)}


def main():
    if len(sys.argv) != 2:
        sys.exit(__doc__)
    html = open(sys.argv[1], encoding="utf-8").read()
    if "matchup" in sys.argv[1]:
        out = parse_matchup(html)
    elif "roster" in sys.argv[1]:
        out = parse_roster(html)
    else:
        out = parse_players(html)
    print(json.dumps(out, indent=2, ensure_ascii=False))


if __name__ == "__main__":
    main()

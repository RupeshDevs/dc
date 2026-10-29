"""
This code is only made for educational and practice purposes. 
Author and Async Development are not responsible for misuse.

GhoSty Discord Game Badges Spoofer

GitHub: https://github.com/WannaBeGhoSt
Discord: https://discord.gg/asMJGgDA7u
"""

from __future__ import annotations

import json
import urllib.request
from dataclasses import dataclass
from pathlib import Path

GHOSTY_GAMES_CDN_URL = "https://cdn.discordapp.com/detectables/games.json"
GAMES_CDN_URL = GHOSTY_GAMES_CDN_URL


@dataclass(frozen=True)
class GhoStyGame:
    id: str
    name: str
    exe: str


Game = GhoStyGame


def ghosty_win_exe(game: dict) -> str:
    for entry in game.get("executables", []):
        if entry.get("os") == "win32" and entry.get("name"):
            return entry["name"]
    return "game.exe"


def ghosty_download_games(file_path: Path) -> str:
    req = urllib.request.Request(GHOSTY_GAMES_CDN_URL, headers={"User-Agent": "Mozilla/5.0"})
    with urllib.request.urlopen(req, timeout=30) as response:
        raw = response.read().decode("utf-8")
    try:
        file_path.parent.mkdir(parents=True, exist_ok=True)
        file_path.write_text(raw, encoding="utf-8")
    except OSError:
        pass
    return raw


def ghosty_parse_games(raw: str) -> list[GhoStyGame]:
    data = json.loads(raw)
    games: list[GhoStyGame] = []
    seen: set[str] = set()
    for entry in data:
        gid = str(entry.get("id", ""))
        if not gid.isdigit() or gid in seen:
            continue
        if not any(e.get("os") == "win32" and e.get("name") for e in entry.get("executables", [])):
            continue
        seen.add(gid)
        games.append(GhoStyGame(gid, entry.get("name", "Unknown"), ghosty_win_exe(entry)))
    return games


def ghosty_load_games(file_path: Path) -> list[GhoStyGame]:
    raw = ""
    if file_path.exists():
        try:
            raw = file_path.read_text(encoding="utf-8").strip()
        except OSError:
            pass
    if raw:
        try:
            games = ghosty_parse_games(raw)
            if games:
                return games
        except (json.JSONDecodeError, ValueError):
            pass

    try:
        return ghosty_parse_games(ghosty_download_games(file_path))
    except Exception:
        return []


def ghosty_select_games(
    all_games: list[GhoStyGame], used_ids: list[str], count: int
) -> tuple[list[GhoStyGame], list[str]]:
    available_ids = {g.id for g in all_games}
    unused_ids = [g.id for g in all_games if g.id not in used_ids]
    valid_used_ids = [gid for gid in used_ids if gid in available_ids]

    if len(unused_ids) >= count:
        selected_ids = unused_ids[:count]
    else:
        selected_ids = list(unused_ids)
        if valid_used_ids:
            remaining = count - len(selected_ids)
            rotated = valid_used_ids[remaining:] + valid_used_ids[:remaining]
            selected_ids.extend(rotated[:remaining])

    new_used_ids = [gid for gid in used_ids if gid not in selected_ids] + selected_ids
    id_map = {g.id: g for g in all_games}
    selected_games = [id_map[gid] for gid in selected_ids if gid in id_map]
    return selected_games, new_used_ids


load_games = ghosty_load_games
select_games = ghosty_select_games

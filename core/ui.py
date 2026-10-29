"""
This code is only made for educational and practice purposes. 
Author and Async Development are not responsible for misuse.

GhoSty Discord Game Badges Spoofer

GitHub: https://github.com/WannaBeGhoSt
Discord: https://discord.gg/asMJGgDA7u
"""

from __future__ import annotations

import os
import re
import shutil
import sys
import time


def _enable_windows_vt() -> None:
    if os.name == "nt":
        try:
            import ctypes
            if hasattr(ctypes, "windll") and hasattr(ctypes.windll, "kernel32"):
                kernel32 = ctypes.windll.kernel32
                handle = kernel32.GetStdHandle(-11)
                mode = ctypes.c_ulong()
                if kernel32.GetConsoleMode(handle, ctypes.byref(mode)):
                    mode.value |= 0x0004
                    kernel32.SetConsoleMode(handle, mode)
        except Exception:
            pass


_enable_windows_vt()

if hasattr(sys.stdout, "reconfigure"):
    try:
        sys.stdout.reconfigure(encoding="utf-8")
    except Exception:
        pass
if hasattr(sys.stderr, "reconfigure"):
    try:
        sys.stderr.reconfigure(encoding="utf-8")
    except Exception:
        pass

RESET = "\033[0m"
BOLD = "\033[1m"
DIM = "\033[2m"
ITALIC = "\033[3m"

CYAN_ELECTRIC = (0, 245, 255)
CYAN_MID      = (0, 195, 255)
BLUE_ELECTRIC = (30, 144, 255)
BLUE_NEON     = (59, 130, 246)
PURPLE_NEON   = (168, 85, 247)
PURPLE_LIGHT  = (192, 132, 252)
GREEN_NEON    = (52, 211, 153)
GREEN_EMERALD = (16, 185, 129)
YELLOW_GOLD   = (250, 204, 21)
RED_CRIMSON   = (248, 113, 113)
RED_BRIGHT    = (239, 68, 68)
GRAY_TEXT     = (148, 163, 184)
GRAY_MUTED    = (100, 116, 139)
GRAY_BORDER   = (51, 65, 85)
WHITE_BRIGHT  = (248, 250, 252)


def fg_rgb(r: int, g: int, b: int) -> str:
    return f"\033[38;2;{r};{g};{b}m"


def bg_rgb(r: int, g: int, b: int) -> str:
    return f"\033[48;2;{r};{g};{b}m"


def strip_ansi(text: str) -> str:
    return re.sub(r"\033\[[0-9;]*[a-zA-Z]", "", text)


def ghosty_get_term_width(default: int = 86) -> int:
    try:
        w = shutil.get_terminal_size((default, 24)).columns
        return max(w, 55)
    except Exception:
        return default

get_term_width = ghosty_get_term_width


def ghosty_clear_screen() -> None:
    if os.name == "nt":
        os.system("cls")
    else:
        sys.stdout.write("\033[2J\033[H\033[3J")
        sys.stdout.flush()

clear_screen = ghosty_clear_screen


def center(text: str, width: int | None = None) -> str:
    if width is None:
        width = ghosty_get_term_width()
    plain_len = len(strip_ansi(text))
    if plain_len >= width:
        return text
    pad = (width - plain_len) // 2
    return " " * pad + text


def center_block(lines: list[str], width: int | None = None) -> list[str]:
    if width is None:
        width = ghosty_get_term_width()
    clean_lines = [strip_ansi(l) for l in lines]
    non_empty = [l for l in clean_lines if l.strip()]
    if not non_empty:
        return lines
    max_len = max(len(l) for l in non_empty)
    pad = max(0, (width - max_len) // 2)
    return [(" " * pad + line) if line.strip() else "" for line in lines]


def lerp_color(c1: tuple[int, int, int], c2: tuple[int, int, int], t: float) -> tuple[int, int, int]:
    return (
        int(c1[0] + (c2[0] - c1[0]) * t),
        int(c1[1] + (c2[1] - c1[1]) * t),
        int(c1[2] + (c2[2] - c1[2]) * t),
    )


def multi_gradient_color(colors: list[tuple[int, int, int]], t: float) -> tuple[int, int, int]:
    if not colors:
        return (255, 255, 255)
    if len(colors) == 1 or t <= 0.0:
        return colors[0]
    if t >= 1.0:
        return colors[-1]

    seg_len = 1.0 / (len(colors) - 1)
    seg_idx = min(int(t / seg_len), len(colors) - 2)
    local_t = (t - (seg_idx * seg_len)) / seg_len
    return lerp_color(colors[seg_idx], colors[seg_idx + 1], local_t)


def ghosty_colorize_gradient(text: str, colors: list[tuple[int, int, int]] | None = None) -> str:
    if colors is None:
        colors = [CYAN_ELECTRIC, CYAN_MID, BLUE_ELECTRIC, PURPLE_NEON]

    clean = strip_ansi(text)
    if not clean:
        return text

    n = len(clean)
    result = []
    clean_idx = 0
    in_ansi = False
    ansi_buf = []

    for ch in text:
        if ch == "\033":
            in_ansi = True
            ansi_buf.append(ch)
            continue
        if in_ansi:
            ansi_buf.append(ch)
            if ch.isalpha():
                in_ansi = False
                result.append("".join(ansi_buf))
                ansi_buf = []
            continue

        t = clean_idx / max(n - 1, 1)
        r, g, b = multi_gradient_color(colors, t)
        result.append(f"{fg_rgb(r, g, b)}{ch}")
        clean_idx += 1

    result.append(RESET)
    return "".join(result)

colorize_gradient = ghosty_colorize_gradient


def ghosty_make_badge(text: str, bg_tuple: tuple[int, int, int], fg_tuple: tuple[int, int, int] = (0, 0, 0), width: int = 10) -> str:
    padded = f" {text} ".center(width)
    return f"{bg_rgb(*bg_tuple)}{fg_rgb(*fg_tuple)}{BOLD}{padded}{RESET}"

make_badge = ghosty_make_badge


GHOSTY_LOGO_WIDE = [
    '   ▄▄▄▄▄▄ ▄▄▄            ▄▄▄▄▄            ▄▄▄▄▄                            ▄██▀                 ',
    ' ██▀▀  ▀█  ██           ▄██ ▀█  ▄█       ▄██ ▀█                            ██                   ',
    '███        ██▀██  ██▀█▄  ▀██▄▄ ▀██▀▀██▀▀█▀    ▀██▄▄  ▄██▀█▄   ██▀█▄   ██▀█▄   ████▀   ▄███▄  ▄██▀█▄ ',
    '▀██   ▀██▀ ██ ██ ███ ██ ▄  ▀▀██ ██  ▀███     ▄  ▀▀██ ███ ██  ███ ██  ███ ██    ██    ████▀▀  ███ ▀▀ ',
    ' ▀▀█▄▄▄█▀ ▄██▄██▄ ██▄█▀ █▀█▄▄█▀ ██▄  ▀█      █▀█▄▄█▀ ███▄█▀   ██▄█▀   ██▄█▀   ▄██▄    ▀███▀  ██     ',
    '                                   ▄▄▄▀              ██                                             ',
    '                                   ▀▀▀               ▀▀                                             ',
]

GHOSTY_LOGO_STACKED = [
    '   ▄▄▄▄▄▄ ▄▄▄            ▄▄▄▄▄        ',
    ' ██▀▀  ▀█  ██           ▄██ ▀█  ▄█    ',
    '███        ██▀██  ██▀█▄  ▀██▄▄ ▀██▀▀██▀▀█▀',
    '▀██   ▀██▀ ██ ██ ███ ██ ▄  ▀▀██ ██  ▀███  ',
    ' ▀▀█▄▄▄█▀ ▄██▄██▄ ██▄█▀ █▀█▄▄█▀ ██▄  ▀█   ',
    '                                   ▄▄▄▀   ',
    '                                   ▀▀▀    ',
    ' ▄▄▄▄▄                            ▄██▀                 ',
    '▄██ ▀█                            ██                   ',
    ' ▀██▄▄  ▄██▀█▄   ██▀█▄   ██▀█▄   ████▀   ▄███▄  ▄██▀█▄ ',
    '▄  ▀▀██ ███ ██  ███ ██  ███ ██    ██    ████▀▀  ███ ▀▀ ',
    '█▀█▄▄█▀ ███▄█▀   ██▄█▀   ██▄█▀   ▄██▄    ▀███▀  ██     ',
    '        ██                                             ',
    '        ▀▀                                             ',
]

LOGO_SPOOFER = GHOSTY_LOGO_WIDE
GHOSTY_LOGO_SPOOFER = GHOSTY_LOGO_WIDE


def ghosty_render_header(games_count: int, claimed_games: int, claimed_hours: float, user_id: str = "", width: int | None = None) -> str:
    if width is None:
        width = ghosty_get_term_width()

    lines_out = [""]
    grad_colors = [CYAN_ELECTRIC, (45, 190, 255), BLUE_ELECTRIC, PURPLE_NEON]
    raw_logo = GHOSTY_LOGO_WIDE if width >= 104 else GHOSTY_LOGO_STACKED
    banner_grad = [ghosty_colorize_gradient(l, grad_colors) for l in raw_logo]
    lines_out.extend(center_block(banner_grad, width))
    lines_out.append("")

    v_tag = (
        f"{fg_rgb(*CYAN_MID)}{BOLD}GhoSty Spoofer V4.1{RESET} "
        f"{fg_rgb(*GRAY_MUTED)}•{RESET} {fg_rgb(*PURPLE_LIGHT)}Universalist & Eternal Edition{RESET} "
        f"{fg_rgb(*GRAY_MUTED)}•{RESET} {fg_rgb(*GREEN_NEON)}{BOLD}Free Forever{RESET}"
    )
    lines_out.append(center(v_tag, width))
    lines_out.append("")

    acc_display = f"{fg_rgb(*CYAN_ELECTRIC)}{user_id}{RESET}" if user_id else f"{fg_rgb(*YELLOW_GOLD)}NOT SET{RESET}"
    meta_line = (
        f"{fg_rgb(*GRAY_TEXT)}USER: {RESET}{acc_display}  "
        f"{fg_rgb(*GRAY_BORDER)}│{RESET}  {fg_rgb(*GRAY_TEXT)}DATABASE: {RESET}{fg_rgb(*CYAN_ELECTRIC)}{games_count} games{RESET}  "
        f"{fg_rgb(*GRAY_BORDER)}│{RESET}  {fg_rgb(*GRAY_TEXT)}CLAIMED: {RESET}{fg_rgb(*GREEN_NEON)}{claimed_games} games{RESET}  "
        f"{fg_rgb(*GRAY_BORDER)}│{RESET}  {fg_rgb(*GRAY_TEXT)}HOURS: {RESET}{fg_rgb(*PURPLE_LIGHT)}{claimed_hours:,.0f}h{RESET}"
    )
    lines_out.append(center(meta_line, width))

    author_line = (
        f"{fg_rgb(*GRAY_MUTED)}< Made With {RESET}{fg_rgb(*RED_CRIMSON)}♥{RESET}{fg_rgb(*GRAY_MUTED)} in India By {RESET}"
        f"{fg_rgb(*CYAN_MID)}{BOLD}@jijaghosty{RESET}{fg_rgb(*GRAY_MUTED)} • {RESET}"
        f"{fg_rgb(*PURPLE_NEON)}Async Development{RESET}{fg_rgb(*GRAY_MUTED)} >{RESET}"
    )
    lines_out.append(center(author_line, width))
    lines_out.append("")

    box_lines = ghosty_render_command_matrix(width=width)
    lines_out.extend(box_lines)
    lines_out.append("")

    div_title = f" {BOLD}{fg_rgb(*CYAN_ELECTRIC)}[ LIVE TELEMETRY LOGS ]{RESET} "
    div_plain_len = len(strip_ansi(div_title))
    box_w = min(width - 4, 82)
    left_line_len = 4
    right_line_len = max(0, box_w - left_line_len - div_plain_len)
    section_div = f"{fg_rgb(*GRAY_BORDER)}{'─' * left_line_len}{RESET}{div_title}{fg_rgb(*GRAY_BORDER)}{'─' * right_line_len}{RESET}"
    lines_out.append(center(section_div, width))
    lines_out.append("")

    return "\n".join(lines_out)

render_header = ghosty_render_header


def ghosty_render_command_matrix(width: int | None = None) -> list[str]:
    if width is None:
        width = ghosty_get_term_width()

    box_w = min(width - 4, 82)
    if box_w < 55:
        box_w = 55

    b_col = fg_rgb(*CYAN_MID)
    tag_col = fg_rgb(*CYAN_ELECTRIC)

    commands = [
        ("<01>", "Claim Playtime & Games", "Farms 5k hours & 100+ games"),
        ("<02>", "Refresh Auth Token",     "Refetches Discord analytics token"),
        ("<03>", "Regenerate Fingerprint",  "Pure Python cross-platform hash"),
        ("<04>", "View Account Status",     "Inspect current session credentials"),
        ("<05>", "Exit GhoSty Spoofer",     "Safely disconnects & saves state"),
    ]

    lines = []
    top_border = f"{b_col}╭{'─' * (box_w - 2)}╮{RESET}"
    lines.append(center(top_border, width))

    title_text = f"{BOLD}{fg_rgb(*WHITE_BRIGHT)}GHOSTY COMMAND MATRIX{RESET}"
    inner_pad = (box_w - 2 - len(strip_ansi(title_text))) // 2
    right_pad = box_w - 2 - len(strip_ansi(title_text)) - inner_pad
    lines.append(center(f"{b_col}│{RESET}{' ' * inner_pad}{title_text}{' ' * right_pad}{b_col}│{RESET}", width))

    sep_border = f"{b_col}├{'─' * (box_w - 2)}┤{RESET}"
    lines.append(center(sep_border, width))

    for num, action, desc in commands:
        line_content = (
            f" {tag_col}{num}{RESET} {fg_rgb(*WHITE_BRIGHT)}{BOLD}{action:<26}{RESET} "
            f"{fg_rgb(*GRAY_MUTED)}│{RESET} {fg_rgb(*GRAY_TEXT)}{desc}{RESET}"
        )
        plain_len = len(strip_ansi(line_content))
        r_pad = max(0, box_w - 2 - plain_len)
        lines.append(center(f"{b_col}│{RESET}{line_content}{' ' * r_pad}{b_col}│{RESET}", width))

    bottom_border = f"{b_col}╰{'─' * (box_w - 2)}╯{RESET}"
    lines.append(center(bottom_border, width))
    return lines

render_command_matrix = ghosty_render_command_matrix


def ghosty_log_info(msg: str) -> None:
    badge = ghosty_make_badge("INFO", (14, 165, 233), (0, 0, 0), width=10)
    arrow = f"{fg_rgb(*CYAN_MID)}──>{RESET}"
    print(f"   {badge} {arrow} {fg_rgb(*WHITE_BRIGHT)}{msg}{RESET}")

log_info = ghosty_log_info


def ghosty_log_success(msg: str) -> None:
    badge = ghosty_make_badge("READY", (16, 185, 129), (0, 0, 0), width=10)
    arrow = f"{fg_rgb(*GREEN_NEON)}──>{RESET}"
    print(f"   {badge} {arrow} {fg_rgb(*GREEN_NEON)}{msg}{RESET}")

log_success = ghosty_log_success


def ghosty_log_sent(target: str, detail: str) -> None:
    badge = ghosty_make_badge("SENT", (16, 185, 129), (0, 0, 0), width=10)
    arrow = f"{fg_rgb(*CYAN_ELECTRIC)}──>{RESET}"
    timestamp = f"{fg_rgb(*GRAY_MUTED)}{time.strftime('%H:%M:%S')}{RESET}"
    print(f"   {badge} {arrow} {timestamp} {fg_rgb(*WHITE_BRIGHT)}{target:<15}{RESET} {fg_rgb(*GREEN_NEON)}{detail}{RESET}")

log_sent = ghosty_log_sent


def ghosty_log_warn(msg: str) -> None:
    badge = ghosty_make_badge("WARNING", (217, 119, 6), (0, 0, 0), width=10)
    arrow = f"{fg_rgb(*YELLOW_GOLD)}──>{RESET}"
    print(f"   {badge} {arrow} {fg_rgb(*YELLOW_GOLD)}{msg}{RESET}")

log_warn = ghosty_log_warn


def ghosty_log_error(msg: str) -> None:
    badge = ghosty_make_badge("ERROR", (220, 38, 38), (255, 255, 255), width=10)
    arrow = f"{fg_rgb(*RED_BRIGHT)}──>{RESET}"
    print(f"   {badge} {arrow} {fg_rgb(248, 113, 113)}{msg}{RESET}")

log_error = ghosty_log_error


def ghosty_log_divider(title: str | None = None) -> None:
    w = min(ghosty_get_term_width() - 4, 82)
    b_col = fg_rgb(*GRAY_BORDER)
    if title:
        badge = f" {fg_rgb(*CYAN_MID)}{BOLD}[ {title} ]{RESET} "
        clean_len = len(strip_ansi(badge))
        left = 4
        right = max(0, w - left - clean_len)
        print(center(f"{b_col}{'─' * left}{RESET}{badge}{b_col}{'─' * right}{RESET}"))
    else:
        print(center(f"{b_col}{'─' * w}{RESET}"))

log_divider = ghosty_log_divider


def ghosty_prompt_input(label: str) -> str:
    arrow = f"{fg_rgb(*CYAN_ELECTRIC)}❯{RESET}"
    return input(f"   {arrow} {fg_rgb(*WHITE_BRIGHT)}{label}{RESET} ").strip()

prompt_input = ghosty_prompt_input

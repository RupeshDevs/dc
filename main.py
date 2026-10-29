"""
This code is only made for educational and practice purposes. 
Author and Async Development are not responsible for misuse.

GhoSty Discord Game Badges Spoofer

GitHub: https://github.com/WannaBeGhoSt
Discord: https://discord.gg/asMJGgDA7u
"""

from __future__ import annotations

import sys
import time
from pathlib import Path

GHOSTY_ROOT = Path(__file__).resolve().parent
GHOSTY_GAMES_FILE = GHOSTY_ROOT / "games.json"
GHOSTY_STATE_FILE = GHOSTY_ROOT / "science_state.json"

ROOT = GHOSTY_ROOT
GAMES_FILE = GHOSTY_GAMES_FILE
STATE_FILE = GHOSTY_STATE_FILE

from core import (
    GhoStyGame,
    GhoStyScienceClient,
    GhoStySession,
    GhoStySpoofer,
    GhoStyState,
    ghosty_ensure_token,
    ghosty_generate_fingerprint,
    ghosty_load_games,
    ghosty_select_games,
    ui,
)


class GhoStyApp:
    def __init__(self) -> None:
        self.ghosty_state = GhoStyState.ghosty_load(GHOSTY_STATE_FILE)
        self.ghosty_session: GhoStySession | None = None
        self.ghosty_client: GhoStyScienceClient | None = None
        self.ghosty_games: list[GhoStyGame] = []

    def ghosty_new_session(self) -> None:
        self.ghosty_session = GhoStySession.ghosty_new()
        self.ghosty_client = GhoStyScienceClient(self.ghosty_state, self.ghosty_session)

    _new_session = ghosty_new_session

    def ghosty_start(self) -> None:
        ui.ghosty_clear_screen()
        print(ui.ghosty_render_header(
            games_count=len(self.ghosty_games),
            claimed_games=self.ghosty_state.total_games_claimed,
            claimed_hours=self.ghosty_state.total_hours_claimed,
            user_id=self.ghosty_state.user_id,
        ))

        if not self.ghosty_state.has_token:
            ui.ghosty_log_info("Discord account token is required.")
            token = ui.ghosty_prompt_input("Paste your Discord token:")
            if not token:
                ui.ghosty_log_error("Token is required to proceed. Exiting GhoSty Spoofer.")
                return
            self.ghosty_state.token = token
            uid = self.ghosty_state.user_id
            if uid:
                self.ghosty_state.fingerprint = ghosty_generate_fingerprint(uid)
            self.ghosty_state.ghosty_save(GHOSTY_STATE_FILE)
            ui.ghosty_log_success(f"Token saved. User ID identified: {uid}")
            time.sleep(0.5)
        else:
            ui.ghosty_log_success(f"Token loaded for User ID: {self.ghosty_state.user_id}")
            time.sleep(0.3)

        if not self.ghosty_state.has_cookie:
            ui.ghosty_log_info("Cloudflare clearance cookie (cf_clearance) is optional.")
            cookie = ui.ghosty_prompt_input("Paste cf_clearance cookie [Optional - press Enter to skip]:")
            if cookie and cookie.strip():
                self.ghosty_state.cookie = cookie.strip()
                self.ghosty_state.ghosty_save(GHOSTY_STATE_FILE)
                ui.ghosty_log_success("cf_clearance cookie saved [Optional].")
            else:
                self.ghosty_state.cookie = ""
                ui.ghosty_log_info("No cf_clearance cookie provided [Optional - direct mode enabled].")
            time.sleep(0.3)
        else:
            ui.ghosty_log_success("cf_clearance cookie loaded [Optional].")
            time.sleep(0.3)

        ui.ghosty_log_info("Loading detectable games database...")
        self.ghosty_games = ghosty_load_games(GHOSTY_GAMES_FILE)
        if not self.ghosty_games:
            ui.ghosty_log_error("Failed to load games. Check connection or place games.json next to main.py.")
            return
        ui.ghosty_log_success(f"Loaded {len(self.ghosty_games):,} detectable Windows games.")
        time.sleep(0.4)

        if not self.ghosty_state.fingerprint:
            uid = self.ghosty_state.user_id
            if uid:
                self.ghosty_state.fingerprint = ghosty_generate_fingerprint(uid)
                self.ghosty_state.ghosty_save(GHOSTY_STATE_FILE)
                ui.ghosty_log_success(f"Executable fingerprint auto-generated for {uid}.")
            else:
                ui.ghosty_log_warn("Could not parse User ID from token to generate fingerprint.")
            time.sleep(0.4)
        else:
            ui.ghosty_log_success("Executable fingerprint loaded (cross-platform).")
            time.sleep(0.3)

        ui.ghosty_log_info("Validating Discord session & analytics token...")
        self.ghosty_new_session()
        try:
            ghosty_ensure_token(self.ghosty_state, self.ghosty_session.super_props, GHOSTY_STATE_FILE)
            ui.ghosty_log_success("Discord session validated. GhoSty telemetry engine ready.")
        except Exception as exc:
            ui.ghosty_log_error(f"Authentication error: {exc}")
            return
        time.sleep(0.8)

        self.ghosty_menu()

    start = ghosty_start

    def ghosty_claim_games(self) -> None:
        ui.ghosty_log_divider("CLAIM PLAYTIME & GAMES")
        ui.ghosty_log_info(f"Available games database: {len(self.ghosty_games):,} titles.")

        raw_count = ui.ghosty_prompt_input(f"How many games to spoof? [all / 1-{len(self.ghosty_games)}]:")
        try:
            count = int(raw_count) if raw_count else len(self.ghosty_games)
        except ValueError:
            ui.ghosty_log_error("Invalid game count entered.")
            time.sleep(1)
            return
        count = max(1, min(count, len(self.ghosty_games)))

        raw_hours = ui.ghosty_prompt_input("Hours per game? [Default: 1.0]:")
        try:
            hours = float(raw_hours) if raw_hours else 1.0
        except ValueError:
            ui.ghosty_log_error("Invalid hours entered.")
            time.sleep(1)
            return
        hours = max(0.1, hours)

        selected, new_used = ghosty_select_games(self.ghosty_games, self.ghosty_state.used_games, count)
        if not selected:
            ui.ghosty_log_error("No games could be selected.")
            time.sleep(1)
            return

        self.ghosty_state.used_games = new_used
        duration_ms = int(hours * 3600 * 1000)
        total_hours = len(selected) * hours

        ui.ghosty_log_info(f"Targeting: {len(selected):,} games × {hours:g}h = {total_hours:,.0f} hours total.")
        ui.ghosty_log_divider("DISPATCHING BATCHES")

        def on_batch(batch_no: int, sent_ok: int, total: int, status: int) -> None:
            if status == 204:
                ui.ghosty_log_sent(f"Batch {batch_no}", f"{sent_ok}/{total} games credited [HTTP 204]")
            elif status in (401, 403):
                ui.ghosty_log_error(f"Batch {batch_no} rejected [HTTP {status}]. Check token or cookie.")
            else:
                ui.ghosty_log_warn(f"Batch {batch_no} returned [HTTP {status}].")

        spoofer = GhoStySpoofer(self.ghosty_client)
        credited = spoofer.ghosty_run(
            selected,
            lambda g: self.ghosty_client.ghosty_build_session(g, duration_ms),
            on_batch=on_batch,
        )

        ui.ghosty_log_divider("SUMMARY")
        claimed_h = credited * hours
        ui.ghosty_log_success(f"Completed! Credited {credited:,}/{len(selected):,} games ({claimed_h:,.0f} hours).")

        self.ghosty_state.total_games_claimed += credited
        self.ghosty_state.total_hours_claimed += claimed_h
        self.ghosty_state.ghosty_save(GHOSTY_STATE_FILE)

        print()
        ui.ghosty_prompt_input("Press Enter to return to main menu...")

    claim_games = ghosty_claim_games

    def ghosty_refresh_auth(self) -> None:
        ui.ghosty_log_divider("REFRESH CREDENTIALS")
        choice = ui.ghosty_prompt_input("Update cf_clearance cookie? [Optional] [y/N]:").lower()
        if choice in ("y", "yes"):
            new_cookie = ui.ghosty_prompt_input("Paste new cf_clearance cookie [Optional - press Enter to clear]:")
            if new_cookie.strip():
                self.ghosty_state.cookie = new_cookie.strip()
                ui.ghosty_log_success("cf_clearance cookie updated [Optional].")
            else:
                self.ghosty_state.cookie = ""
                ui.ghosty_log_info("cf_clearance cookie cleared [Optional - direct mode enabled].")
            self.ghosty_state.ghosty_save(GHOSTY_STATE_FILE)

        token_choice = ui.ghosty_prompt_input("Update account token? [y/N]:").lower()
        if token_choice in ("y", "yes"):
            new_token = ui.ghosty_prompt_input("Paste new Discord token:")
            if new_token:
                self.ghosty_state.token = new_token
                uid = self.ghosty_state.user_id
                if uid:
                    self.ghosty_state.fingerprint = ghosty_generate_fingerprint(uid)
                ui.ghosty_log_success(f"Token updated. User ID: {uid}")

        ui.ghosty_log_info("Fetching fresh analytics token from Discord...")
        try:
            self.ghosty_state.fetched_at = 0
            self.ghosty_new_session()
            ghosty_ensure_token(self.ghosty_state, self.ghosty_session.super_props, GHOSTY_STATE_FILE)
            self.ghosty_state.ghosty_save(GHOSTY_STATE_FILE)
            ui.ghosty_log_success("Session credentials successfully refreshed.")
        except Exception as exc:
            ui.ghosty_log_error(f"Failed to refresh session: {exc}")
        time.sleep(1.5)

    refresh_auth = ghosty_refresh_auth

    def ghosty_regen_fingerprint(self) -> None:
        ui.ghosty_log_divider("REGENERATE FINGERPRINT")
        uid = self.ghosty_state.user_id
        if not uid:
            ui.ghosty_log_error("No valid user ID available. Please set token first.")
            time.sleep(1.5)
            return

        ui.ghosty_log_info(f"Generating fresh fingerprint for Account: {uid}...")
        self.ghosty_state.fingerprint = ghosty_generate_fingerprint(uid)
        self.ghosty_state.ghosty_save(GHOSTY_STATE_FILE)
        ui.ghosty_log_success(f"New fingerprint saved ({len(self.ghosty_state.fingerprint)} chars).")
        time.sleep(1.5)

    regen_fingerprint = ghosty_regen_fingerprint

    def ghosty_view_status(self) -> None:
        ui.ghosty_log_divider("GHOSTY ACCOUNT STATUS & DIAGNOSTICS")
        uid = self.ghosty_state.user_id or "Unknown"
        token_preview = (
            f"{self.ghosty_state.token[:12]}...{self.ghosty_state.token[-6:]}"
            if len(self.ghosty_state.token) > 20
            else "Not set"
        )
        cookie_status = f"Valid ({len(self.ghosty_state.cookie)} chars) [Optional]" if self.ghosty_state.has_cookie else "None [Optional - Direct Mode]"
        fp_status = f"Valid ({len(self.ghosty_state.fingerprint)} chars)" if self.ghosty_state.fingerprint else "Not generated"

        ui.ghosty_log_info(f"Account User ID   : {uid}")
        ui.ghosty_log_info(f"Account Token     : {token_preview}")
        ui.ghosty_log_info(f"cf_clearance Cookie: {cookie_status}")
        ui.ghosty_log_info(f"Fingerprint       : {fp_status}")
        ui.ghosty_log_info(
            f"Total Claimed     : {self.ghosty_state.total_games_claimed:,} games | {self.ghosty_state.total_hours_claimed:,.0f} hours"
        )
        ui.ghosty_log_info(f"Games Catalog     : {len(self.ghosty_games):,} titles loaded from {GHOSTY_GAMES_FILE.name}")
        ui.ghosty_log_info(f"Config File Path  : {GHOSTY_STATE_FILE}")
        print()
        ui.ghosty_prompt_input("Press Enter to return to main menu...")

    view_status = ghosty_view_status

    def ghosty_menu(self) -> None:
        while True:
            ui.ghosty_clear_screen()
            print(ui.ghosty_render_header(
                games_count=len(self.ghosty_games),
                claimed_games=self.ghosty_state.total_games_claimed,
                claimed_hours=self.ghosty_state.total_hours_claimed,
                user_id=self.ghosty_state.user_id,
            ))

            choice = ui.ghosty_prompt_input("Select an option [1-5]:")
            if choice in ("1", "01"):
                self.ghosty_claim_games()
            elif choice in ("2", "02"):
                self.ghosty_refresh_auth()
            elif choice in ("3", "03"):
                self.ghosty_regen_fingerprint()
            elif choice in ("4", "04"):
                self.ghosty_view_status()
            elif choice in ("5", "05", "exit", "q"):
                ui.ghosty_log_info("Exiting GhoSty Science Spoofer. Happy badge hunting!")
                break
            else:
                ui.ghosty_log_warn("Invalid option chosen. Please select 1 through 5.")
                time.sleep(1)

    menu = ghosty_menu


App = GhoStyApp


def ghosty_main() -> None:
    try:
        GhoStyApp().ghosty_start()
    except KeyboardInterrupt:
        print()
        ui.ghosty_log_warn("Session interrupted by user (SIGINT). Exiting GhoSty Spoofer safely.")
        sys.exit(0)

main = ghosty_main


if __name__ == "__main__":
    ghosty_main()
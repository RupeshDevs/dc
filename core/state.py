"""
This code is only made for educational and practice purposes. 
Author and Async Development are not responsible for misuse.

GhoSty Discord Game Badges Spoofer

GitHub: https://github.com/WannaBeGhoSt
Discord: https://discord.gg/asMJGgDA7u
"""

from __future__ import annotations

import base64
import json
import time
from dataclasses import dataclass, field, asdict
from pathlib import Path

GHOSTY_AUTH_MAX_AGE = 12 * 3600


def ghosty_user_id_from_token(token: str) -> str:
    try:
        first = token.split(".", 1)[0]
        pad = "=" * (-len(first) % 4)
        return base64.b64decode(first + pad).decode("utf-8")
    except Exception:
        return ""


@dataclass
class GhoStyState:
    token: str = ""
    cookie: str = ""
    fingerprint: str = ""
    analytics_token: str = ""
    fetched_at: int = 0
    used_games: list[str] = field(default_factory=list)
    total_games_claimed: int = 0
    total_hours_claimed: float = 0.0

    @classmethod
    def ghosty_load(cls, file_path: Path) -> GhoStyState:
        if file_path.exists():
            try:
                data = json.loads(file_path.read_text(encoding="utf-8"))
                state = cls()
                for key in cls().__dict__:
                    if key in data:
                        setattr(state, key, data[key])
                return state
            except Exception:
                pass
        return cls()

    load = ghosty_load

    def ghosty_save(self, file_path: Path) -> None:
        try:
            file_path.write_text(json.dumps(asdict(self), indent=2), encoding="utf-8")
        except Exception:
            pass

    save = ghosty_save

    @property
    def user_id(self) -> str:
        return ghosty_user_id_from_token(self.token)

    @property
    def is_stale(self) -> bool:
        return not self.analytics_token or (time.time() - self.fetched_at) > GHOSTY_AUTH_MAX_AGE

    @property
    def has_cookie(self) -> bool:
        return bool(self.cookie and self.cookie.strip())

    @property
    def has_token(self) -> bool:
        return bool(self.token.strip())


State = GhoStyState
user_id_from_token = ghosty_user_id_from_token
AUTH_MAX_AGE = GHOSTY_AUTH_MAX_AGE

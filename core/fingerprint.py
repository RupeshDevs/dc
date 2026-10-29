"""
This code is only made for educational and practice purposes. 
Author and Async Development are not responsible for misuse.

GhoSty Discord Game Badges Spoofer

GitHub: https://github.com/WannaBeGhoSt
Discord: https://discord.gg/asMJGgDA7u
"""

from __future__ import annotations

import base64
import hashlib
import struct
import time
import uuid


def ghosty_generate_fingerprint(ghosty_user_id: str) -> str:
    ghosty_flags = 2
    ghosty_file_size = 45_214_720
    ghosty_timestamp = int(time.time()) - 86400 * 30
    ghosty_size_of_image = 48_500_000
    ghosty_header_hash = hashlib.sha256(b"discord_game_header_hash").digest()
    ghosty_machine_guid = str(uuid.uuid4())
    ghosty_machine_user_hash = hashlib.sha256(f"{ghosty_machine_guid}{ghosty_user_id}".encode("utf-8")).digest()
    ghosty_section_hash = hashlib.sha256(b"discord_game_section_hash").digest()
    ghosty_cert_hash = bytes(32)

    ghosty_buf = bytearray()
    ghosty_buf.append(1)
    ghosty_buf.append(ghosty_flags)
    ghosty_buf.extend(struct.pack("<Q", ghosty_file_size))
    ghosty_buf.extend(struct.pack("<I", ghosty_timestamp))
    ghosty_buf.extend(struct.pack("<I", ghosty_size_of_image))
    ghosty_buf.extend(ghosty_header_hash)
    ghosty_buf.extend(ghosty_machine_user_hash)
    ghosty_buf.extend(ghosty_section_hash)
    ghosty_buf.extend(ghosty_cert_hash)

    ghosty_key = hashlib.sha256(f"{ghosty_user_id}https://discord.com/careers".encode("utf-8")).digest()
    for i in range(1, len(ghosty_buf)):
        ghosty_buf[i] ^= ghosty_key[(i - 1) & 31]

    return base64.b64encode(ghosty_buf).decode("ascii")


generate_fingerprint = ghosty_generate_fingerprint

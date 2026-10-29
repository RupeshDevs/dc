<div align="center">
  <a href="https://git.io/typing-svg"><img src="https://readme-typing-svg.herokuapp.com?font=Merriweather&size=40&pause=1000&color=00e5ff&center=true&vCenter=true&random=false&width=550&lines=GhoSty+Spoofer;Universalist+%26+Eternal;Discord+Badge+Tool" alt="Typing SVG" /></a>
  <br/>
  <a href="https://discord.gg/asMJGgDA7u"><img src="https://invidget.switchblade.xyz/asMJGgDA7u" alt="Discord Invite"/> </a>
  <br/>
  <small><p>Join our official Discord community for support and updates!<br>
  Need direct assistance? Shoot a friend request to <code>@jijaghosty</code> on Discord.</p></small>
</div>

---

The most advanced, lightweight, zero-dependency Discord Science Telemetry Spoofer. Effortlessly simulate gameplay activity and playtime hours to unlock exclusive Discord profile badges.

> [!CAUTION]
> ⚠️ **DISCLAIMER:** This software is provided strictly for educational, security auditing, and research purposes. Interacting directly with Discord's internal `/api/v9/science` telemetry endpoint violates Discord's Terms of Service. **Your account, your responsibility.** We accept zero liability for any account suspensions, bans, or penalties. Use at your own discretion.

<div align="center">
  <img src="https://capsule-render.vercel.app/api?type=transparent&color=gradient&customColorList=00e5ff,00ffaa&height=60&section=header&text=⚡%20Features&fontSize=40&fontAlignY=35" alt="Features" />
</div>

- 🏆 **Universalist Badge Unlocker** — Spoofs 100+ verified game launches from Discord's detectable game library.
- ⏳ **Eternal Badge Unlocker** — Dispatches heartbeat events crediting 5,000+ hours of tracked playtime.
- 📱 **100% Android (Termux) Compatible** — Completely decoupled from Windows-specific scripts or PowerShell binaries; runs natively on Android, Linux, macOS, and Windows.
- 📦 **Zero External Dependencies** — Built entirely with standard Python libraries (`urllib`, `hashlib`, `json`, `dataclasses`). No `pip install` required.
- 🛡️ **Cross-Platform 146-Byte Fingerprint Engine** — Pure Python emulation of Windows PE executable hashing for legitimate telemetry validation.
- 🍪 **Optional Cloudflare Clearance** — `cf_clearance` cookie input is fully optional; connects directly by default and allows cookie attachment whenever Cloudflare challenges arise.
- 🎨 **TrueColor Cyberpunk Terminal UI** — Dual-mode responsive ANSI half-block logo banner, dynamic color gradients, status badges, and boxed command matrix.
- 💾 **State Persistence** — Caches credentials, analytics tokens, and claimed playtime locally in `science_state.json`.

<div align="center">
  <img src="https://capsule-render.vercel.app/api?type=transparent&color=gradient&customColorList=ff007f,b500ff&height=60&section=header&text=🏆%20Badges%20Unlocked&fontSize=40&fontAlignY=35" alt="Badges Unlocked" />
</div>

| Badge | Title | Requirement | Spoofed Payload |
| :---: | :---: | :---: | :---: |
| 🎮 | **The Universalist** | Play 100+ unique detectable games | Emulates `launch_game` events across 100+ verified game IDs |
| ⌛ | **The Eternal** | Accumulate 5,000+ game playtime hours | Dispatches `running_game_heartbeat` with cumulative tracked durations |

> [!NOTE]
> Discord evaluates and awards profile badges through asynchronous backend aggregation jobs. Badges typically appear on your profile within **24 to 48 hours** after events are dispatched.

<div align="center">
  <img src="https://capsule-render.vercel.app/api?type=transparent&color=gradient&customColorList=b500ff,ff007f&height=60&section=header&text=🚀%20Setup%20and%20Installation&fontSize=40&fontAlignY=35" alt="Setup" />
</div>

### 1️⃣ Requirements
- **Python 3.8+** (Works out-of-the-box on Python 3.8, 3.9, 3.10, 3.11, 3.12, 3.13+)
- Internet connection (to fetch game catalogs from Discord CDN)

### 2️⃣ Installation & Execution

#### 📱 Android (Termux)
```bash
pkg update && pkg install python git -y
cd "this directory name"
python main.py
```

#### 🪟 Windows
```powershell
python main.py
```

#### 🐧 Linux & macOS
```bash
python3 main.py
```

<div align="center">
  <img src="https://capsule-render.vercel.app/api?type=transparent&color=gradient&customColorList=00e5ff,b500ff&height=60&section=header&text=🕹️%20Interactive%20Options&fontSize=40&fontAlignY=35" alt="Interactive Options" />
</div>

Upon launch, GhoSty Spoofer presents the Command Matrix:

- `<01> Claim Playtime & Games` — Prompts for the number of games to spoof (e.g. 100) and hours per game (e.g. 50 hours each = 5,000 hours total). Dispatches events in batches with live HTTP telemetry logs.
- `<02> Refresh Auth Token` — Interactively update your Discord account token or CF clearance cookie, and refetch fresh analytics tokens.
- `<03> Regenerate Fingerprint` — Computes a fresh cross-platform 146-byte executable hash tied to your Discord User ID.
- `<04> View Account Status` — Inspect active User ID, token preview, connection mode, fingerprint status, and total claimed game metrics.
- `<05> Exit GhoSty Spoofer` — Safely persists current session progress to `science_state.json` and closes the program.


<div align="center">
  <img src="https://capsule-render.vercel.app/api?type=transparent&color=gradient&customColorList=00e5ff,b500ff&height=60&section=header&text=👑%20About%20Developer&fontSize=40&fontAlignY=35" alt="About Developer" />
</div>

<div align="center">
  <p><b>GhoSty | Brutality (Async Development)</b></p>
  <a href="https://discord.com/users/940896719045034024" target="_blank">
    <img src="https://lanyard.cnrad.dev/api/940896719045034024?theme=dark&bg=16161a&animated=true&hideDiscrim=true&borderRadius=10px" alt="Live Discord Profile Widget" />
  </a>
</div>

<div align="center">
  <img src="https://capsule-render.vercel.app/api?type=transparent&color=gradient&customColorList=00ffaa,00e5ff&height=60&section=header&text=💎%20Support%20the%20Project&fontSize=40&fontAlignY=35" alt="Support" />
</div>

If this tool helped you claim your profile badges, consider supporting development!

**LTC (Litecoin) Wallet:**
```
LbeKrDeUF7mTB8LZLHkjicQfEW6tyhVGny
```

Alternatively, you can support us directly via **[Donatree](https://donatr.ee/brutality/)**.

<div align="center">
  <img src="https://capsule-render.vercel.app/api?type=transparent&color=gradient&customColorList=ff3300,ff9900&height=60&section=header&text=⚠️%20Important%20Notices&fontSize=40&fontAlignY=35" alt="Notices" />
</div>

- **Unauthorized reselling or redistribution of this software is strictly prohibited.**
- **Your account, your responsibility. Please use this software responsibly. The creator assumes no responsibility for Discord TOS infractions.**

---
<div align="center">
  <i>Thanks for using GhoSty Spoofer! Enjoy your profile badges! 🚀</i>
  <br><br>
  <img src="https://visitor-badge.laobi.icu/badge?page_id=WannaBeGhoSt.discord-game-badges-spoofer" alt="Repository Views" />
</div>

<br>
<details>
<summary>Keywords</summary>
discord badge spoofer, discord universalist badge, discord eternal badge, discord games badge, discord playtime hours, discord science telemetry, discord playtime spoofer, discord badges tool, ghosty spoofer, discord 100 games badge, discord 5000 hours badge, termux discord badge tool, python discord spoofer, discord api science, discord telemetry exploit, async development, jijaghosty
</details>

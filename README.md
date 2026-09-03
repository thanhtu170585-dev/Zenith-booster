# SNEERYBOOSTER MOBILE

Premium Android Game Booster — White Frosted Gaming Control Center — Python + Kivy.

## Overview
SNEERYBOOSTER MOBILE manages gaming sessions, game profiles, performance monitoring, overlay HUD, DND, brightness/rotation, AI analysis — lightweight, no fake boost numbers.

## Features
- **Home**: Device stats (RAM/CPU/Temp/Battery), BOOST NOW, gaming session
- **Games**: Installed game detection via PackageManager, ADD GAME, per-game profile
- **Game Profile**: Performance mode, graphics, network, thermal, DND, overlay
- **Boost**: Real booster engine via ActivityManager where allowed, steps reflect real actions (skipped if permission missing)
- **Gaming Session**: Timer, stats, history
- **Performance Monitor**: 1.5s interval, battery-aware
- **Overlay HUD**: SYSTEM_ALERT_WINDOW, draggable, frosted, FPS/CPU/RAM
- **DND/Brightness/Rotation**: Real Android APIs with permission checks
- **AI**: Local rule-based SNEERY AI, context-aware, provider-agnostic
- **Settings**: Appearance, Gaming, Monitoring, Permissions, Storage, About
- **Permissions Center**: Overlay, Usage, DND, Battery — real checks, OPEN SETTINGS
- **Storage**: Documents/SNEERY/{Videos,Recordings,Replays,Moments,Screenshots,Clips,Sessions}

## Architecture
```
SneeryBoosterMobile/
  main.py
  core/ (booster, game_detector, performance, device, permissions, android_api, overlay, dnd, brightness, rotation, ai_engine, profiles, storage, gaming_session)
  ui/screens/ (home, games, boost, ai, settings)
  ui/components/ (cards)
  ui/theme/
  services/
  data/
  utils/
  tests/
  assets/
  buildozer.spec
```

## Installation (Windows + WSL)
```bash
# Windows: install Python 3.10-3.11 recommended for Kivy
pip install -r requirements.txt

# For Android build, use WSL2 Ubuntu:
wsl --install
# In WSL:
sudo apt update && sudo apt install -y python3-pip openjdk-17-jdk unzip
pip install buildozer cython
buildozer android debug
```

## Running Locally (Desktop for UI test)
```bash
pip install kivy kivymd pillow psutil
python main.py
```

## Android Build
```bash
# In WSL, from project root:
buildozer android debug
# APK at bin/SneeryBooster-1.0-debug.apk
# Or: buildozer android release
```

If WSL not available, buildozer will fail on Windows — this is expected. Code is still complete and can be built on any Linux/WSL.

## APK Output
- Debug: `bin/SneeryBooster-1.0-debug.apk`
- Release: `bin/SneeryBooster-1.0-release.apk` (needs keystore)

Check: `ls bin/*.apk` after build.

## Permissions (requested only if needed)
- INTERNET, PACKAGE_USAGE_STATS, SYSTEM_ALERT_WINDOW, REQUEST_IGNORE_BATTERY_OPTIMIZATIONS, POST_NOTIFICATIONS, WAKE_LOCK, WRITE_SETTINGS
- All special permissions show permission screen with OPEN SETTINGS, never fake Granted.

## Limitations (Android reality)
- Cannot directly control CPU governor/hardware overclock without root/vendor
- OEM may restrict background kills
- FPS not exposed without game integration → shows Unavailable
- Some permissions require manual user grant

## Troubleshooting
- `kivy` fails on Python 3.12+ → use 3.10/3.11
- `jnius` not found on desktop → fallback to psutil/desktop mode, logs warning
- Overlay not showing → check permission screen
- Build fails: ensure JDK 17, NDK 25b, SDK 33, accept licenses

## Roadmap
- Cloud sync, account, real AI API (OpenAI), more encoders, plugin system

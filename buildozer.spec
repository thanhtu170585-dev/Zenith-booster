[app]
title = SNEERYBOOSTER MOBILE
package.name = SneeryBooster
package.domain = com.sneery.booster
source.dir = .
source.include_exts = py,png,jpg,jpeg,webp,json,ttf,atlas
version = 1.0
version.regex = __version__ = ['"]([^'"]*)['"]
version.filename = %(source.dir)s/main.py
requirements = python3,kivy==2.3.1,kivymd==1.2.0,pillow,psutil,pyjnius,android
orientation = portrait
fullscreen = 0
android.permissions = INTERNET, PACKAGE_USAGE_STATS, SYSTEM_ALERT_WINDOW, REQUEST_IGNORE_BATTERY_OPTIMIZATIONS, POST_NOTIFICATIONS, WAKE_LOCK, WRITE_SETTINGS, WRITE_EXTERNAL_STORAGE, READ_EXTERNAL_STORAGE
android.api = 33
android.minapi = 21
android.ndk = 25b
android.sdk = 33
android.accept_sdk_license_agreements = True
android.ant = auto
p4a.branch = master
p4a.bootstrap = sdl2
android.archs = arm64-v8a, armeabi-v7a
icon.filename = %(source.dir)s/assets/images/icon.png
presplash.filename = %(source.dir)s/assets/images/presplash.png

[buildozer]
log_level = 2
warn_on_root = 1

# For Windows, build via WSL - user must run wsl buildozer android debug

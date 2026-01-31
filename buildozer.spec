[app]
# (str) Title of your application
title = FjordReceipts

# (str) Package name (lowercase, no spaces)
package.name = fjordreceipts

# (str) Package domain (reverse DNS)
package.domain = com.fjord

# (str) Source code where the main.py is located
source.dir = .

# (list) List of inclusions using pattern matching
source.include_exts = py,kv,png,jpg,kvlang

# (str) Application versioning
version = 0.1.0

# (list) Application requirements
# include kivy and pyjnius for Android Java interop
requirements = python3,kivy==2.1.0,pyjnius

# (str) Supported orientation (one of landscape, sensorLandscape, portrait, all)
orientation = portrait

# Android API settings
android.api = 31
android.minapi = 21
android.target = 31

# (str) Android architectures to build for
android.archs = armeabi-v7a, arm64-v8a

# (str) Android NDK version suggestion (p4a may override if incompatible)
# If build fails you can try `android.ndk = 23b` or other supported NDK
# android.ndk = 23b

# Permissions required for Bluetooth printing and networking
android.permissions = BLUETOOTH,BLUETOOTH_ADMIN,ACCESS_FINE_LOCATION,BLUETOOTH_CONNECT,BLUETOOTH_SCAN,INTERNET

# (bool) If 1, build a debug APK
debug = 1

# (str) Icon and presplash (place your `icon.png` in the project root)
icon.filename = %(source.dir)s/icon.png
# Use the same image for presplash as the icon to avoid duplicating files
presplash.filename = %(source.dir)s/icon.png

[buildozer]
log_level = 2
warn_on_root = 1

[app:android]
# (str) Additional Android SDK packages to install
# android.sdk_dependencies = extra-google-m2repository

# (int) Android entrypoint (default = org.kivy.android.PythonActivity)
#android.entrypoint = org.kivy.android.PythonActivity

# (str) Additional java classes to add
#android.add_jars = libs/some-lib.jar

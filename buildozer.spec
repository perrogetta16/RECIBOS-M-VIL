[app]
title = FjordReceipts
package.name = fjordreceipts
package.domain = com.fjord
source.dir = .
source.include_exts = py,png,jpg

version = 0.1.0

requirements = python3,kivy==2.1.0,pyjnius

orientation = portrait
fullscreen = 0

android.api = 30
android.minapi = 21
android.ndk = 25b
android.target = 30
android.archs = arm64-v8a

# Permissions for Bluetooth and location
android.permissions = BLUETOOTH,BLUETOOTH_ADMIN,ACCESS_FINE_LOCATION,BLUETOOTH_CONNECT,BLUETOOTH_SCAN,INTERNET

debug = 1

# Icon (will use default if missing)
# icon.filename = %(source.dir)s/icon.png

# Presplash (optional)
# presplash.filename = %(source.dir)s/presplash.png

# Java/Android specific options
android.accept_sdk_license = True
android.gradle_dependencies = 

[buildozer]
log_level = 2
warn_on_root = 1

[app:android]
# Additional gradle options to avoid build errors
android.gradle_options = org.gradle.jvmargs=-Xmx4096m

# (str) Additional java classes to add
#android.add_jars = libs/some-lib.jar

[app]

# (str) Title of your application
title = PreTools

# (str) Package name
package.name = pretools

# (str) Package domain (needed for android/ios packaging)
package.domain = com.pretools

# (str) Source code where the main.py live
source.dir = .

# (list) Source files to include (let empty to include all the files)
source.include_exts = py,png,jpg,kv,atlas,json

# (str) Application versioning (method 1)
version = 1.0

# (list) Application requirements
# comma separated e.g. requirements = sqlite3,kivy
requirements = python3,kivy==2.1.0,android,pyjnius,plyer,pillow

# (str) Supported orientation (landscape, sensorLandscape, portrait or sensorPortrait)
orientation = portrait

# (bool) Indicate if the application should be fullscreen or not
fullscreen = 0

# (list) Permissions
android.permissions = WRITE_EXTERNAL_STORAGE,READ_EXTERNAL_STORAGE,INTERNET,SYSTEM_ALERT_WINDOW

# (int) Target Android API, should be as high as possible.
android.api = 30

# (int) Minimum API your APK will support.
android.minapi = 21

# (str) Android NDK version to use
android.ndk = 20b

# (int) Android SDK version to use
android.sdk = 28

# (str) Android app theme, default is ok for Kivy-based app
android.theme = "@android:style/Theme.NoTitleBar.Fullscreen"

# (str) Gradle dependencies
android.gradle_dependencies = 

# (str) Icon of the application
icon.filename = %(source.dir)s/icon.png

# (str) Presplash of the application  
presplash.filename = %(source.dir)s/icon.png

# (str) The main python file to use
source.main = overlay_style_app.py

[buildozer]

# (int) Log level (0 = error only, 1 = info, 2 = debug (with command output))
log_level = 2

# (int) Display warning if buildozer is run as root (0 = False, 1 = True)
warn_on_root = 1

# (str) Path to build artifact storage, absolute or relative to spec file
# build_dir = ./.buildozer

# (str) Path to build output (i.e. .apk, .ipa) storage
# bin_dir = ./bin
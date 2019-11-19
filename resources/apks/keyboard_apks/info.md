#get apk(s) of each keyboard:
adb shell pm path <package> | cut -f2 -d: | xargs -I{} adb pull {} .

#get keyboard version:
adb shell dumpsys package <package> | grep versionName


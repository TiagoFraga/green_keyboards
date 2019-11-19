statJson=$1
 soft_version=$(adb shell getprop ro.build.software.version | sed "s/Android//g" | cut -f1 -d_)
 ismi=$(test -z $(adb shell getprop ro.miui.cust_variant) && echo "true")
if [ -z "$ismi"  ]; then
	 mi_version=$(adb shell getprop ro.miui.ui.version.name)
else
	 mi_version=""
fi
 sdk_version=$(adb shell getprop ro.build.version.sdk)
# device_keyboard=$(adb shell dumpsys  input_method | grep "mCurMethodId" | cut -f2 -d= )
 operator=$(adb shell getprop gsm.sim.operator.alpha)
 operator_country=$(adb shell getprop gsm.operator.iso-country)
 conn_type=$(adb shell getprop gsm.network.type )
 kernel_version=$(adb shell cat /proc/version)
 device_id=$(adb shell getprop ro.serialno )
 nr_installed_apps=$( adb shell pm list packages | wc -l | sed 's/ //g')
 device_lang=$( adb shell getprop persist.sys.locale)
echo "
{
	\"state_device_id\": \"$device_id\",
	\"state_os_version\": \"$soft_version\",
	\"state_miui_version\": \"$mi_version\", 
	\"state_api_version\": \"$sdk_version\", 
	\"state_kernel_version\": \"$kernel_version\", 
	\"state_operator\": \"$operator\", 
	\"state_operator_country\": \"$operator_country\",
	\"state_nr_installed_apps\": \"$nr_installed_apps\"
	\"state_current_lang\": \"$device_lang\"

}" > "$statJson"
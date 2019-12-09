statJson=$1
device_serial_nr=$2
 soft_version=$(adb -s $device_serial_nr shell getprop ro.build.software.version | sed "s/Android//g" | cut -f1 -d_)
 ismi=$(test -z $(adb  -s $device_serial_nr shell getprop ro.miui.cust_variant) && echo "true")
if [ -z "$ismi"  ]; then
	 mi_version=$(adb -s $device_serial_nr  shell getprop ro.miui.ui.version.name)
else
	 mi_version=""
fi
 sdk_version=$(adb  -s $device_serial_nr shell getprop ro.build.version.sdk)
# device_keyboard=$(adb shell dumpsys  input_method | grep "mCurMethodId" | cut -f2 -d= )
 operator=$(adb  -s $device_serial_nr shell getprop gsm.sim.operator.alpha)
 operator_country=$(adb  -s $device_serial_nr shell getprop gsm.operator.iso-country)
 conn_type=$(adb  -s $device_serial_nr shell getprop gsm.network.type )
 kernel_version=$(adb  -s $device_serial_nr shell cat /proc/version)
 device_id=$(adb  -s $device_serial_nr shell getprop ro.serialno )
 nr_installed_apps=$( adb  -s $device_serial_nr shell pm list packages | wc -l | sed 's/ //g')
 device_lang=$( adb  -s $device_serial_nr shell getprop persist.sys.locale)
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
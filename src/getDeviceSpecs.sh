devJson=$1
DEVICE=$(adb devices -l  2>&1 | tail -2)
has_devices_conected=$(adb shell echo "" 2>&1 | grep "devices/emulators found")
if [[ -n "$has_devices_conected" ]]; then
	e_echo " No Conected Devices found. Conect the device to the development machine and try again. Aborting..."
	#exit -1
fi
# device_model=$(   echo  $DEVICE  | grep -o "model.*" | cut -f2 -d: | cut -f1 -d\ )
 device_model=$(adb shell getprop ro.product.model)
 device_serial=$(   echo  $DEVICE | tail -n 2 | grep "model" | cut -f1 -d\ )
 device_ram=$(adb shell cat /proc/meminfo | grep "MemTotal"| cut -f2 -d: | sed 's/ //g')
 device_cores=$( adb shell cat /proc/cpuinfo | grep processor| wc -l | sed 's/ //g')
 device_max_cpu_freq=$(adb shell cat /proc/cpumaxfreq )
 device_brand=$(adb shell getprop ro.product.brand)
# device_brand=$(  echo  $DEVICE | grep -o "device:.*" | cut -f2 -d: )
echo "
{
	\"device_serial_number\": \"$device_serial\",
	 \"device_model\": \"$device_model\",
	 \"device_brand\": \"$device_brand\",
	 \"device_ram\": \"$device_ram\",
	 \"device_cores\": \"$device_cores\",
	 \"device_max_cpu_freq\": \"$device_max_cpu_freq\"
}" > "$devJson"
#i_echo "📲  Attached device ($device_model) recognized "
#deviceDir="$deviceExternal/trepn"
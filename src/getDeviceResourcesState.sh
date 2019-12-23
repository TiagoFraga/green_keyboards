


resState=$1
device_serial_nr=$2
# hree numbers represent averages over progressively longer periods of time (one, five, and fifteen minute averages),
used_cpu=$(adb  -s $device_serial_nr shell dumpsys cpuinfo | grep  "Load" | cut -f2 -d: | sed 's/ //g' )
#used_mem=$(adb shell dumpsys meminfo | grep "Free RAM.*" | cut -f2 -d: | cut -f1 -d\( | tr -d ' '| sed "s/K//g" | sed "s/,//g")
mem=$(adb  -s $device_serial_nr shell dumpsys meminfo | grep "Used RAM.*" ) #| cut -f2 -d: | cut -f1 -d\( | tr -d ' ' ) #| sed "s/K//g" | sed "s/,//g")
used_mem_pss=$( echo "$mem" |  cut -f2 -d\(   | cut -f1 -d+ | cut -f1 -d\   )
used_mem_kernel=$(echo "$mem" |  cut -f2 -d\(   | cut -f2 -d+     |  sed 's/kernel)//g' | sed 's/ //g' )
#nprocesses=$(adb shell top -n 1 |  wc -l) #take the K/M and -4
#nr_procceses=$(($nprocesses -6))
nr_processes=$( adb  -s $device_serial_nr shell ps -o STAT  | egrep "^R|L" | wc -l | sed 's/ //g') # get processes running or with pages in memory
#sdk_level=$(adb shell getprop ro.build.version.release)
battery=$(adb  -s $device_serial_nr shell dumpsys battery)
#echo "battery -> $battery"
ischarging=$( echo $battery | grep "powered" |  grep "true" | wc -l | sed 's/ //g')
battery_level=$(echo "$battery" | grep "level:" | cut -f2 -d\: | sed "s/ //g")
keyboard=$(adb  -s $device_serial_nr shell dumpsys  input_method | grep "mCurMethodId" | cut -f2 -d= )
battery_temperature=$(echo "$battery" | grep "temperature:" | cut -f2 -d\: | sed "s/ //g")
battery_voltage=$(echo "$battery" | grep "voltage:" | tail -1 | cut -f2 -d\: | sed "s/ //g")
main_cpu_freq=$( adb -s $device_serial_nr  shell cat "/sys/devices/system/cpu/cpu0/cpufreq/scaling_cur_freq" )
wifi_on=$(adb  -s $device_serial_nr shell settings get global wifi_on)
mobile_data_on=$(adb  -s $device_serial_nr shell settings get global mobile_data0)
adb -s $device_serial_nr shell dumpsys  input_method | grep "mCurMethodId" | cut -f2 -d= | cut -f1 -d/ | xargs -I{} adb -s $device_serial_nr shell 'su -c find /data/data/{}' > "$resState.keyboard_files"
nr_files_keyboard_folder=$(adb -s $device_serial_nr shell dumpsys  input_method | grep "mCurMethodId" | cut -f2 -d= | cut -f1 -d/ | xargs -I{} adb -s $device_serial_nr shell 'su -c find /data/data/{} | wc -l')
timestamp=$(date +%s)
echo "
    {	\"timestamp\": \"$timestamp\",
		\"used_cpu\": \"$used_cpu\",
		\"used_mem_pss\": \"$used_mem_pss\", 
		\"used_mem_kernel\": \"$used_mem_kernel\", 
		\"nr_processes\": \"$nr_processes\", 
		\"ischarging\": \"$ischarging\", 
		\"battery_level\": \"$battery_level\", 
		\"battery_temperature\": \"$battery_temperature\",
		\"keyboard\": \"$keyboard\", 
		\"battery_voltage\": \"$battery_voltage\"
		\"nr_files_keyboard_folder\": \"$nr_files_keyboard_folder\",
		\"main_cpu_freq\": \"$main_cpu_freq\"
	}" > "$resState"
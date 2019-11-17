resState=$1
# hree numbers represent averages over progressively longer periods of time (one, five, and fifteen minute averages),
used_cpu=$(adb shell dumpsys cpuinfo | grep  "Load" | cut -f2 -d: | sed 's/ //g' )
#used_mem=$(adb shell dumpsys meminfo | grep "Free RAM.*" | cut -f2 -d: | cut -f1 -d\( | tr -d ' '| sed "s/K//g" | sed "s/,//g")
mem=$(adb shell dumpsys meminfo | grep "Used RAM.*" ) #| cut -f2 -d: | cut -f1 -d\( | tr -d ' ' ) #| sed "s/K//g" | sed "s/,//g")
used_mem_pss=$( echo "$mem" |  cut -f2 -d\(   | cut -f1 -d+ | cut -f1 -d\   )
used_mem_kernel=$(echo "$mem" |  cut -f2 -d\(   | cut -f2 -d+     |  sed 's/kernel)//g' | sed 's/ //g' )
#nprocesses=$(adb shell top -n 1 |  wc -l) #take the K/M and -4
#nr_procceses=$(($nprocesses -6))
nr_processes=$( adb shell ps -o STAT  | egrep "^R|L" | wc -l | sed 's/ //g') # get processes running or with pages in memory
#sdk_level=$(adb shell getprop ro.build.version.release)
battery=$(adb shell dumpsys battery)
#echo "battery -> $battery"
ischarging=$( echo $battery | grep "powered" |  grep "true" | wc -l | sed 's/ //g')
battery_level=$(echo "$battery" | grep "level:" | cut -f2 -d\: | sed "s/ //g")
keyboard=$(adb shell dumpsys  input_method | grep "mCurMethodId" | cut -f2 -d= )
battery_temperature=$(echo "$battery" | grep "temperature:" | cut -f2 -d\: | sed "s/ //g")
battery_voltage=$(echo "$battery" | grep "voltage:" | tail -1 | cut -f2 -d\: | sed "s/ //g")
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
	}" > "$resState"
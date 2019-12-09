#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os
import time
from termcolor import colored

def getDeviceState(serialno,arg):
    os.system("./src/getDeviceState.sh %s %s" %(arg,serialno) )
    time.sleep(1)

def getDeviceSpecs(serialno,arg):
    os.system("./src/getDeviceSpecs.sh  %s %s" %(arg,serialno) )
    time.sleep(1)


def getDeviceResourcesState(serialno,arg):
    os.system("./src/getDeviceResourcesState.sh %s %s" %(arg,serialno) )
    time.sleep(1)

def setBrightness(adbcl,level):
    if level>0:
        adbcl.shell (" settings put system screen_brightness_mode 1")
    else:
        adbcl.shell (" settings put system screen_brightness_mode 0")
    adbcl.shell(" settings put system screen_brightness " + str(level))

def assureTestExecutionConditions(adbcl):
    expected_wifi_state = 0
    expected_screen_awake = "Awake" #unlocked
    #expected_mobile_data_state = 0
    #expected_flashlight_state = 0
    expected_bluetooth_state = 0
    #expected_hotspot_state = 0
    expected_sound_state = 0
    expected_gps_state = 0
    
    # check if wifi is off
    current_wifi_state = int(adbcl.shell("settings get global wifi_on ").strip())
    if not current_wifi_state == expected_wifi_state :
         print(colored("[Device Status Check] Please turn off wifi interface before executing the test","red"))
         exit()

    # check if the screen is ON and unlocked !!! 
    current_screen_state = adbcl.shell("dumpsys power | grep \"mWakefulness=\" | cut -f2 -d=").strip()
    is_current_screen_lock = len(adbcl.shell("dumpsys window | grep \"mShowingLockscreen=true\" "))>0
    is_current_screen_lock2 =len(adbcl.shell("dumpsys window | grep \"mDreamingLockscreen=true\" "))>0
    #print("-%s-%s-%s-" % (current_screen_state , is_current_screen_lock , is_current_screen_lock2) )
    if not current_screen_state == expected_screen_awake or  is_current_screen_lock or is_current_screen_lock2 :
        print(colored("[Device Status Check] Please unlock screen before executing the test","red"))
        exit()
    
    current_bluetooth_state = int(adbcl.shell("settings get global bluetooth_on").strip())
    if not current_bluetooth_state == expected_bluetooth_state :
         print(colored("[Device Status Check] Please turn off bluetooth  before executing the test","red"))
         exit()

    is_hotspot_on = len(adbcl.shell("dumpsys wifi | grep \"curState=TetheredState\"")+ adbcl.shell(" dumpsys wifi | grep \"curState=ApEnabledState\"") ) >0
    if is_hotspot_on:
         print(colored("[Device Status Check] Please turn off Wi-fi Tethering  before executing the test","red"))
         exit()

    is_speaker_on = len( adbcl.shell("dumpsys audio | grep \"STREAM_SYSTEM:\" -A 1 | grep \"false\""))>0
    if is_speaker_on:
         print(colored("[Device Status Check] Please turn off Audio Speakers before executing the test","red"))
         exit()

    is_gps_on = len (adbcl.shell( "settings get secure location_providers_allowed | grep \"gps\"" )) >0
    if is_gps_on:
         print(colored("[Device Status Check] Please turn off GPS before executing the test","red"))
         exit()

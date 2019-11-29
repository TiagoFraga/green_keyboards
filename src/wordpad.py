#!/usr/bin/env python
# -*- coding: utf-8 -*-
import re
import sys
import os
import io
import time
import datetime
import json
import shutil
import keyboard_functions as keyboard
from profiler import TrepnProfiler
sys.path.append(os.getcwd()+"src/")
from com.dtmilano.android.viewclient import ViewClient
from com.dtmilano.android.adb import adbclient
from termcolor import colored
import changeKeyboards as change

###################
## Global Variables 
###################

SED_COMMAND = ''
MKDIR_COMMAND = ''
MV_COMMAND = ''


nr_tests = 1
output_dir='/outputs/'
deviceDir='/sdcard/trepn/'
trace="-TestOriented"
package = "blackcarbon.wordpad"
edit_text = "blackcarbon.wordpad:id/et_document"
#keyboardsPaths = {1:"com.touchtype.swiftkey/com.touchtype.KeyboardService",2:"com.google.android.inputmethod.latin/com.android.inputmethod.latin.LatinIME",3:"panda.keyboard.emoji.theme/com.android.inputmethod.latin.LatinIME", 4:"com.jb.emoji.gokeyboard/com.jb.gokeyboard.GoKeyboard",5:"com.pinssible.fancykey/.FancyService", 6:"com.sec.android.inputmethod/.SamsungKeypad"}
#keyboardsPaths = {2:"com.google.android.inputmethod.latin/com.android.inputmethod.latin.LatinIME",6:"com.sec.android.inputmethod/.SamsungKeypad"}

########################
## OS Auxiliar Functions 
########################




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


def getOS():
    global SED_COMMAND
    global MKDIR_COMMAND
    global MV_COMMAND
    os = sys.platform
    if os == 'darwin':
        # macOS
        SED_COMMAND = "gsed"
        MKDIR_COMMAND ="gmkdir"
        MV_COMMAND="gmv"
    elif os == 'linux2' or os == 'linux':
        # linux
        SED_COMMAND ="sed" 
        MKDIR_COMMAND ="mkdir"
        MV_COMMAND="mv"




#######################################################################################
## Main Functions 
#######################################################################################

def setBrightness(adbcl, level ):
    if level>0:
        adbcl.shell (" settings put system screen_brightness_mode 1")
    else:
        adbcl.shell (" settings put system screen_brightness_mode 0")
    adbcl.shell(" settings put system screen_brightness " + str(level))


def analyzeResults(results_path):
        os.system( "java -jar ./resources/jars/AnaDroidAnalyzer.jar -TestOriented "+ results_path + " -none NONE" )
        trimmed_date = str(datetime.datetime.now()).replace(":","").replace(" ","").replace(".","")
        new_dir= results_path + "/" + trimmed_date
        os.mkdir(new_dir)
        for file in os.listdir(results_path):
            full_file_name = os.path.join(results_path, file)
            if os.path.isfile(full_file_name):
                shutil.copy(full_file_name, new_dir)


def initLocalResultsDir(keyboard_name, android_version):
    output_dir_1 =  os.getcwd() + output_dir +"/"
    if not os.path.exists( output_dir_1 ):
        os.mkdir(output_dir_1)
    output_dir_android = output_dir_1 +"/" + android_version + "/" 
    if not os.path.exists( output_dir_android ):
        os.mkdir(output_dir_android)
    model_dir = output_dir_android + "/" + change.detect_device_model()
    if not os.path.exists( model_dir ):
        os.mkdir(model_dir)
    target_dir = model_dir + "/" + keyboard_name
    if not os.path.exists( target_dir ):
        os.mkdir(target_dir)
    else: 
        #already exists, wipe files of folder
        for file in os.listdir(target_dir):
            full_file_name = os.path.join(target_dir, file)
            if os.path.isfile(full_file_name):
                os.remove(full_file_name)
    return target_dir

def alert():
    timex = 30
    while(timex > 0):
        os.system("say -v diego 'se nao mudares o teclado, o benfica vai ser campeao!!!' ")
        timex = timex -1
        time.sleep(10)


def calculateExtraSleep(begin, end, fmt):

    d1 = datetime.datetime.strptime(str(begin),fmt)
    d2 = datetime.datetime.strptime(str(end),fmt)
    diff = d2-d1
    return diff.seconds/60

def keyboard_test(adbcl, input_text, keyboard_name, test_index, local_results_dir):
    fmt = '%Y-%m-%d %H:%M:%S'
    android_version = change.detect_android_version()
    keyboard.getDeviceSpecs(local_results_dir + "/device.json")
    keyboard.getDeviceState(local_results_dir + "/deviceState.json")
    print("input text -> " + input_text)
    print("keyboard name-> " + keyboard_name)
    print("test index" + str(test_index))
    
    time.sleep(2)
   
    vc = ViewClient(*ViewClient.connectToDeviceOrExit())
    print(colored("[Testing: "+ str(script_index) + "] " + str(datetime.datetime.now()),"yellow"))
    keyboard.cleaningAppCache(adbcl,package) 
    setBrightness(adbcl, 0)
    # initialize app
    getOS()
    profiler = TrepnProfiler(deviceDir )
    profiler.initProfiler(adbcl)
    #keyboard.initProfiler(adbcl,deviceDir)
    #keyboard.activateFlags(adbcl,deviceDir)
    
    #extract file
    print(colored("Extracting text file...","white"))
    text_to_insert = keyboard.read_file(input_text)
    lines_to_insert = keyboard.split_lines(input_text)
    words_to_insert = keyboard.split_words(input_text)
    chars_to_insert = keyboard.split_chars(input_text)
    #print(len(words_to_insert))
    
    #open App
    keyboard.setImmersiveMode(adbcl,package)
    keyboard.openApp(adbcl,package)  #wordpad  
    box_to_insert = keyboard.getEditText(vc, edit_text)
    keyboard.openKeyboard(box_to_insert)
    
    begin_time =  datetime.datetime.now().strftime(fmt)
    begin_state = local_results_dir + "/begin_state" + str(script_index) + ".json"
    keyboard.getDeviceResourcesState(begin_state)
    profiler.startProfiler(adbcl)    #keyboard.writeLines(box_to_insert,lines_to_insert)
    keyboard.writeWords(box_to_insert,words_to_insert)
    profiler.stopProfiler(adbcl)
    end_state = local_results_dir + "/end_state" + str(script_index) + ".json"
    end_time =  datetime.datetime.now().strftime(fmt)
    keyboard.getDeviceResourcesState(end_state)
    
    keyboard.closeApp(adbcl,package)
    #time.sleep(2* calculateExtraSleep(begin_time, end_time, fmt))
    profiler.exportResults(local_results_dir,script_index,SED_COMMAND,MV_COMMAND,assure=True)
    profiler.shutdownProfiler(adbcl)

if __name__== "__main__":
    if len(sys.argv) > 1:
        bol = False
        keyboard_dict =  change.loadkeyboardInfo()
        installed_keyboards = change.get_installed_keyboards(keyboard_dict.values())    
        installed_keyboard_names = list(map( lambda it : str(it['name'])  ,filter(lambda it : str(it['package']) in installed_keyboards  , keyboard_dict.values() )))
        all_considered_keyboards = list(map(lambda it : str(it['name']), keyboard_dict.values()))
        input_text = sys.argv[1]
        sys.argv.pop(1)
        adbcl = adbclient.AdbClient('.*', settransport=True)
        android_version = change.detect_android_version()
        assureTestExecutionConditions(adbcl)
        print(colored("***** [KEYBOARD TEST] *****","blue"))
        current_keyboard = change.get_current_keyboard()
        local_results_dir = initLocalResultsDir(current_keyboard,android_version)
        print("using keyboard " + current_keyboard)
        #change.installKeyboard(android_version, str(option), keyboardsPaths, all_keyboards )
        #print(keyboardsPackages[str(option)])
        #keyboard.setKeyboard(adbcl,keyboardsPackages[str(option)])
        script_index = 0
        while script_index < nr_tests:
            script_index+=1
            #output_filename = str(key) + str(++script_index)
            #keyboard_test(adbcl, input_text , all_keyboards[keyboardsPaths[str(option)]]  ,script_index)
            keyboard_test(adbcl, input_text , current_keyboard ,script_index,local_results_dir)   
        change.uninstallKeyboard(current_keyboard)
        print(colored("***** [KEYBOARD TEST - The End] *****","blue"))
        analyzeResults(local_results_dir)
        alert()
        
    else:
        print (colored("at least 2 args required (text file to insert)","red"))

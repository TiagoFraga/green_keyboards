#!/usr/bin/env python
# -*- coding: utf-8 -*-
import sys
import os
import time
import datetime
from com.dtmilano.android.viewclient import ViewClient
from com.dtmilano.android.adb import adbclient
from termcolor import colored
import changeKeyboards as change
import data
import analyzer
import deviceState
import app
from profiler import TrepnProfiler
sys.path.append(os.getcwd()+"src/")

###################
## Global Variables 
###################

SED_COMMAND = ''
MKDIR_COMMAND = ''
MV_COMMAND = ''


nr_tests = 1
test_type = "suggested"
output_dir='/outputs/'
deviceDir='/sdcard/trepn/'
package = "blackcarbon.wordpad"
edit_text = "blackcarbon.wordpad:id/et_document"
coords_file = './resources/input_files/coords.json'


########################
## OS Auxiliar Functions 
########################


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

def keyboard_test(adbcl, input_text, keyboard_name, test_index, local_results_dir):
    vc = ViewClient(*ViewClient.connectToDeviceOrExit())
    fmt = '%Y-%m-%d %H:%M:%S'

    print(colored("[Text Files] Collecting data","yellow"))
    text_to_insert, lines_to_insert, words_to_insert, chars_to_insert, words_sugge, words_sugge_length = data.getData(input_text)
    coords = data.getCoords(coords_file,keyboard_name)

    deviceState.getDeviceSpecs(local_results_dir + "/device.json")
    deviceState.getDeviceState(local_results_dir + "/deviceState.json")
    time.sleep(2)
    
    print(colored("[Testing: "+ str(script_index) + "] " + str(datetime.datetime.now()),"green"))
    app.cleaningAppCache(adbcl,package) 

    print(colored("[Profiler] Init profiler","yellow"))
    profiler = TrepnProfiler(deviceDir)
    profiler.initProfiler(adbcl)
    
    print(colored("[WordPad] Init app","yellow"))
    app.openApp(adbcl,package)
    app.setImmersiveMode(adbcl,package)
    box_to_insert = app.getEditText(vc, edit_text)
    app.openKeyboard(box_to_insert)
    
    print(colored("[Device State] Collecting device resources state","green"))
    begin_time =  datetime.datetime.now().strftime(fmt)
    begin_state = local_results_dir + "/begin_state" + str(script_index) + ".json"
    deviceState.getDeviceResourcesState(begin_state)
    
    print(colored("[Start Profiling Phase] " + str(datetime.datetime.now()) ,"yellow"))
    profiler.startProfiler(adbcl)    
    app.writeSuggestedWords(vc,box_to_insert,words_sugge,words_sugge_length,coords)
    profiler.stopProfiler(adbcl)
    print(colored("[Stop Profiling Phase] " + str(datetime.datetime.now()),"green"))
    
    print(colored("[Device State] Collecting device resources state","yellow")) 
    end_state = local_results_dir + "/end_state" + str(script_index) + ".json"
    end_time =  datetime.datetime.now().strftime(fmt)
    deviceState.getDeviceResourcesState(end_state)

    print(colored("[WordPad] Close app","green"))
    app.closeApp(adbcl,package)
    time.sleep(2* analyzer.calculateExtraSleep(begin_time, end_time, fmt))

    print(colored("[Profiler] Export results","yellow")) 
    profiler.exportResults(local_results_dir,script_index,SED_COMMAND,MV_COMMAND,assure=True)
    print(colored("[Profiler] Close profiler","green"))
    profiler.shutdownProfiler(adbcl)


def initTestInfo(adbcl):
    getOS()
    android_version = change.detect_android_version()
    keyboard_dict = change.loadkeyboardInfo()
    installed_keyboards = change.get_installed_keyboards(keyboard_dict.values())    
    installed_keyboard_names = list(map( lambda it : str(it['name'])  ,filter(lambda it : str(it['package']) in installed_keyboards  , keyboard_dict.values() )))
    all_considered_keyboards = list(map(lambda it : str(it['name']), keyboard_dict.values()))
    current_keyboard = change.get_current_keyboard()
    local_results_dir = analyzer.initLocalResultsDir(current_keyboard,android_version,output_dir,test_type)
    deviceState.assureTestExecutionConditions(adbcl)
    deviceState.setBrightness(adbcl,0)
    return local_results_dir,current_keyboard
    

if __name__== "__main__":
    if len(sys.argv) > 1:
        input_text = sys.argv[1]
        sys.argv.pop(1)
        adbcl = adbclient.AdbClient('.*', settransport=True)
        
        print(colored("***** [KEYBOARD TEST] *****","blue"))
        print(colored("[Test Info] Loading...","yellow"))
        local_results_dir, current_keyboard = initTestInfo(adbcl)
        
        print(colored("[Starting] "+ str(datetime.datetime.now()),"green"))
        print(colored("[Keyboard] "+ current_keyboard,"yellow"))

        script_index = 0
        while script_index < nr_tests:
            script_index+=1
            keyboard_test(adbcl, input_text , current_keyboard ,script_index,local_results_dir)   
        #change.uninstallKeyboard(current_keyboard)
        analyzer.analyzeResults(local_results_dir)
        print(colored("***** [KEYBOARD TEST - The End] *****","blue"))
        #analyzer.alert()
        
    else:
        print (colored("at least 2 args required (text file to insert)","red"))

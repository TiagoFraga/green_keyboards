#!/usr/bin/env python
# -*- coding: utf-8 -*-
import re
import sys
import os
import io
import time
import datetime
import json
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

def analyzeResults(results_path):
        os.system( "java -jar ./resources/jars/AnaDroidAnalyzer.jar -TestOriented "+ results_path + " -none NONE" )


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
    return target_dir

def alert():
    timex = 30
    while(timex > 0):
        os.system("say -v diego ' Acorda caralho tens de mudar o teclado pilapilapilapilapilapilapilapilapilapilapila' ")
        timex = timex -1
        time.sleep(10)


def keyboard_test(adbcl, input_text, keyboard_name, test_index):
    android_version = change.detect_android_version()
    local_results_dir = initLocalResultsDir(keyboard_name,android_version)
    keyboard.getDeviceSpecs(local_results_dir + "/device.json")
    keyboard.getDeviceState(local_results_dir + "/deviceState.json")
    print("input text -> " + input_text)
    print("keyboard name-> " + keyboard_name)
    print("test index" + str(test_index))
    
    vc = ViewClient(*ViewClient.connectToDeviceOrExit())
    print(colored("[Testing: "+ str(script_index) + "] " + str(datetime.datetime.now()),"yellow"))
    keyboard.cleaningAppCache(adbcl,package) 
    
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
    keyboard.openApp(adbcl,package)  #wordpad  
    box_to_insert = keyboard.getEditText(vc, edit_text)
    keyboard.openKeyboard(box_to_insert)
    
    begin_state = local_results_dir + "/begin_state" + str(script_index) + ".json"
    keyboard.getDeviceResourcesState(begin_state)
    
    profiler.startProfiler(adbcl)    #keyboard.writeLines(box_to_insert,lines_to_insert)
    keyboard.writeWords(box_to_insert,words_to_insert)
    profiler.stopProfiler(adbcl)
    
    end_state = local_results_dir + "/end_state" + str(script_index) + ".json"
    keyboard.getDeviceResourcesState(end_state)
    
    keyboard.closeApp(adbcl,package)
    profiler.shutdownProfiler(adbcl)
    profiler.exportResults(local_results_dir,script_index,SED_COMMAND,MV_COMMAND)


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
        print(colored("***** [KEYBOARD TEST] *****","blue"))
        current_keyboard = change.get_current_keyboard()
        print("using keyboard " + current_keyboard)
        #change.installKeyboard(android_version, str(option), keyboardsPaths, all_keyboards )
        #print(keyboardsPackages[str(option)])
        #keyboard.setKeyboard(adbcl,keyboardsPackages[str(option)])
        script_index = 0
        while script_index < nr_tests:
            script_index+=1
            #output_filename = str(key) + str(++script_index)
            #keyboard_test(adbcl, input_text , all_keyboards[keyboardsPaths[str(option)]]  ,script_index)
            keyboard_test(adbcl, input_text , current_keyboard ,script_index)
        
        #change.uninstallKeyboard(current_keyboard)
        print(colored("***** [KEYBOARD TEST - The End] *****","blue"))
        analyzeResults(initLocalResultsDir(current_keyboard,android_version))
        alert()
        
    else:
        print (colored("at least 2 args required (text file to insert)","red"))

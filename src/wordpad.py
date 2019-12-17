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
import threading
from profiler import TrepnProfiler
sys.path.append(os.getcwd()+"src/")

###################
## Global Variables 
###################

SED_COMMAND = ''
MKDIR_COMMAND = ''
MV_COMMAND = ''


nr_tests = 25
output_dir='/outputs/'
deviceDir='/sdcard/trepn/'
package = "blackcarbon.wordpad"
edit_text = "blackcarbon.wordpad:id/et_document"
keyboard_mode = "minimal"
wordpad_cache_folder = ""
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
    kwargs1 = {'verbose': True, 'ignoresecuredevice': False}
    vc = ViewClient(*ViewClient.connectToDeviceOrExit(serialno=adbcl.serialno, **kwargs1))
    fmt = '%Y-%m-%d %H:%M:%S'

    print(colored("[Text Files] Collecting data","yellow"))
    text_to_insert, lines_to_insert, words_to_insert, chars_to_insert, words_sugge, words_sugge_length = data.getData(input_text)


    deviceState.getDeviceSpecs(adbcl.serialno,local_results_dir + "/device.json")
    deviceState.getDeviceState(adbcl.serialno,local_results_dir + "/deviceState.json")
    time.sleep(2)

    print("ulha o index " + str(test_index))

    print(colored("[Testing: "+ adbcl.serialno + " "+str(test_index) + "] " + str(datetime.datetime.now()),"green"))
    app.cleaningAppCache(adbcl,package) 

    print(colored("[Profiler] Init profiler","yellow"))
    profiler = TrepnProfiler(deviceDir,adbcl)
    profiler.initProfiler()
    
    print(colored("[WordPad] Init app","yellow"))
    app.openApp(adbcl,package)
    app.setImmersiveMode(adbcl,package)
    box_to_insert = app.getEditText(vc, edit_text)
    app.openKeyboard(box_to_insert)

    print(colored("[Device State] Collecting device resources state","green"))
    begin_time =  datetime.datetime.now().strftime(fmt)
    begin_state = local_results_dir + "/begin_state" + str(test_index) + ".json"
    deviceState.getDeviceResourcesState(adbcl.serialno,begin_state)
    
    print(colored("[Start Profiling Phase] " + str(datetime.datetime.now()) ,"yellow"))
    profiler.startProfiler()    
    app.writeWords(box_to_insert,words_to_insert)
    profiler.stopProfiler()
    print(colored("[Stop Profiling Phase] " + str(datetime.datetime.now()),"green"))

    print(colored("[Device State] Collecting device resources state","yellow")) 
    end_state = local_results_dir + "/end_state" + str(test_index) + ".json"
    end_time =  datetime.datetime.now().strftime(fmt)
    deviceState.getDeviceResourcesState(adbcl.serialno,end_state)

    print(colored("[WordPad] Close app","green"))
    app.closeApp(adbcl,package)
    time.sleep(2* analyzer.calculateExtraSleep(begin_time, end_time, fmt))
    
    print(colored("[Profiler] Export results","yellow")) 
    profiler.shutdownProfiler()
    profiler.exportResults(local_results_dir,test_index,SED_COMMAND,MV_COMMAND,assure=True)
    print(colored("[Profiler] Close profiler","green"))
    print(colored("[Profiler] wiping wordpad private folder","green"))
    wipe_wordpad_private_folder(adbcl)
   



def initTestInfo(adbcl):
    getOS()
    android_version = change.detect_android_version(adbcl)
    keyboard_dict = change.loadkeyboardInfo()
    installed_keyboards = change.get_installed_keyboards(adbcl,keyboard_dict.values())    
    installed_keyboard_names = list(map( lambda it : str(it['name'])  ,filter(lambda it : str(it['package']) in installed_keyboards  , keyboard_dict.values() )))
    all_considered_keyboards = list(map(lambda it : str(it['name']), keyboard_dict.values()))
    current_keyboard = change.get_current_keyboard(adbcl)
    local_results_dir = analyzer.initLocalResultsDir(adbcl,current_keyboard,android_version,output_dir, adbcl.serialno)
    deviceState.assureTestExecutionConditions(adbcl)
    deviceState.setBrightness(adbcl,0)
    return local_results_dir,current_keyboard



def each_thread(adbcl,local_results_dir,current_keyboard):
    print("***** [KEYBOARD TEST (device %s )] *****" % adbcl.serialno ,"blue")
    script_index = 0
    while script_index < nr_tests:
        script_index+=1
        keyboard_test(adbcl, input_text , current_keyboard ,script_index,local_results_dir)   
        analyzer.wipe_and_copy_to_tmp_dir(local_results_dir,script_index)
        analyzer.analyze_temp_dir(local_results_dir)

    analyzer.analyzeResults(local_results_dir)
    print(colored("***** [KEYBOARD TEST - The End] *****","blue"))



def wipe_wordpad_private_folder(adbcl):
    print("wiping")
    adbcl.shell( 'su -c " find  /data/data/blackcarbon.wordpad/  -type f | xargs rm   "')

if __name__== "__main__":
    if len(sys.argv) > 1:
        input_text = sys.argv[1]
        sys.argv.pop(1)
        devices_serial_list = os.popen('adb devices -l  | grep \"port\" | cut -f1 -d\ ').read()
        threads = list()
        for index in range(len(devices_serial_list.split("\n"))-1):
            adbcl = adbclient.AdbClient( serialno=str(devices_serial_list.split("\n")[index])  , settransport=True)
            local_results_dir, current_keyboard = initTestInfo(adbcl)
            x = threading.Thread(target=each_thread, args=(adbcl,local_results_dir,current_keyboard,))
            threads.append(x)
            x.start()
            time.sleep(10) # wait >10s between thread starts
        for index, thread in enumerate(threads):
            thread.join()
        #change.uninstallKeyboard(current_keyboard)
    else:
        print (colored("at least 2 args required (text file to insert)","red"))

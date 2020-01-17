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



nr_tests = 1
test_type = "default" #minimal or default
output_dir='/outputs/'
deviceDir='/sdcard/trepn/'
package = "blackcarbon.wordpad"
edit_text = "blackcarbon.wordpad:id/et_document"
wordpad_cache_folder = ""
type_mode="word"


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


## control functions

def askForStartProfiling():
    raw_input("Press Any Key to Start the Profiling Process...")
    

def askForStopProfiling():
    raw_input("Press Any Key to Stop the Profiling Process...")
#######################################################################################
## Main Functions 
#######################################################################################


def keyboard_test(adbcl, keyboard_name, test_index, local_results_dir):
    kwargs1 = {'verbose': True, 'ignoresecuredevice': False}
    vc = ViewClient(*ViewClient.connectToDeviceOrExit(serialno=adbcl.serialno, **kwargs1))
    fmt = '%Y-%m-%d %H:%M:%S'

    deviceState.getDeviceSpecs(adbcl.serialno,local_results_dir + "/device.json")
    deviceState.getDeviceState(adbcl.serialno,local_results_dir + "/deviceState.json")
    print(colored("[Testing: "+ adbcl.serialno + " "+str(test_index) + "] " + str(datetime.datetime.now()),"green"))
    app.cleaningAppCache(adbcl,package) 
    # init profiler
    print(colored("[Profiler] Initializing profiler","yellow"))
    profiler = TrepnProfiler(deviceDir,adbcl)
    profiler.initProfiler()
    # open wordpad and keyboard
    print(colored("[WordPad] Initializing app","yellow"))
    app.openApp(adbcl,package)
    app.setImmersiveMode(adbcl,package)
    box_to_insert = app.getEditText(vc, edit_text)
    app.openKeyboard(box_to_insert)

    print(colored("[Device State] Collecting device resources state","green"))
    begin_time =  datetime.datetime.now().strftime(fmt)
    begin_state = local_results_dir + "/begin_state" + str(test_index) + ".json"
    deviceState.getDeviceResourcesState(adbcl.serialno,begin_state)
    
    askForStartProfiling()
    print(colored("[Starting Profiling Phase] " + str(datetime.datetime.now()) ,"yellow"))
    profiler.startProfiler()    
    
    # wait for user to type text
    askForStopProfiling()
    profiler.stopProfiler()
    print(colored("[Stoping Profiling Phase] " + str(datetime.datetime.now()),"green"))

    print(colored("[Device State] Collecting device resources state","yellow")) 
    end_state = local_results_dir + "/end_state" + str(test_index) + ".json"
    end_time =  datetime.datetime.now().strftime(fmt)
    deviceState.getDeviceResourcesState(adbcl.serialno,end_state)

    print(colored("[WordPad] Closing app","green"))
    app.closeApp(adbcl,package)
    #time.sleep(2* analyzer.calculateExtraSleep(begin_time, end_time, fmt))
    
    print(colored("[Profiler] Exporting results","yellow")) 
    profiler.shutdownProfiler()
    profiler.exportResults(local_results_dir,test_index,SED_COMMAND,MV_COMMAND,assure=True)
    print(colored("[Profiler] Closing Trepn profiler","green"))
    print(colored("[Profiler] Wiping wordpad private folder","green"))
    wipe_wordpad_private_folder(adbcl)
   



def initTestInfo(adbcl):
    getOS()
    android_version = change.detect_android_version(adbcl)
    keyboard_dict = change.loadkeyboardInfo()
    installed_keyboards = change.get_installed_keyboards(adbcl,keyboard_dict.values())    
    installed_keyboard_names = list(map( lambda it : str(it['name'])  ,filter(lambda it : str(it['package']) in installed_keyboards  , keyboard_dict.values() )))
    all_considered_keyboards = list(map(lambda it : str(it['name']), keyboard_dict.values()))
    current_keyboard = change.get_current_keyboard(adbcl)
    local_results_dir = analyzer.initLocalResultsDir(adbcl,current_keyboard,android_version,output_dir, adbcl.serialno, test_type)
    deviceState.assureTestExecutionConditions(adbcl)
    deviceState.setBrightness(adbcl,128)
    return local_results_dir,current_keyboard


def askName():
    return str(raw_input("User name:"))


def move_to_username_folder(username,temp_dir):
    username_folder = "./outputs/6/Nexus5/" + username
    print("user name foldeer "+username_folder)
    os.system("mkdir %s" % username_folder)
    os.system( "mv %s/ %s/ " % (temp_dir, username_folder))

def wipe_wordpad_private_folder(adbcl):
    print("wiping")
    adbcl.shell( 'su -c " find  /data/data/blackcarbon.wordpad/  -type f | xargs rm   "')


if __name__== "__main__":
    devices_serial_list = os.popen('adb devices -l  | grep \"transport\" | cut -f1 -d\ ').read()
    #for index in range(len(devices_serial_list.split("\n"))-1):
    adbcl = adbclient.AdbClient( '.*'  , settransport=True)
    local_results_dir, current_keyboard = initTestInfo(adbcl)
    print("***** [KEYBOARD TEST (device %s )] *****" % adbcl.serialno ,"blue")
    script_index = 0
    user_name=askName()
    #while script_index < nr_tests:
    script_index+=1
    keyboard_test(adbcl , current_keyboard ,script_index,local_results_dir)   
    analyzer.wipe_and_copy_to_tmp_dir(local_results_dir,script_index)
    temp_dir = analyzer.analyze_temp_dir(local_results_dir)
    # todo move to username folder
    move_to_username_folder(user_name,temp_dir)
    #analyzer.analyzeResults(local_results_dir)
    print(colored("***** [KEYBOARD TEST - The End] *****","blue"))


    #x = threading.Thread(target=each_thread, args=(adbcl,local_results_dir,current_keyboard,))
   
    #change.uninstallKeyboard(current_keyboard)
   
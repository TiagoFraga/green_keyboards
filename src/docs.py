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

sys.path.append("/Users/tiagofraga/Desktop/HASLAB/Software/AndroidViewClient-15.8.1/src")
from com.dtmilano.android.viewclient import ViewClient
from com.dtmilano.android.adb import adbclient
from termcolor import colored



###################
## Global Variables 
###################

SED_COMMAND = ''
MKDIR_COMMAND = ''
MV_COMMAND = ''


script_index = 0
tamanho = 20
localDir='./MonkeyRunnerTest/'
deviceDir='/sdcard/trepn/'
trace="-TestOriented"
package = "blackcarbon.wordpad"
edit_text = "blackcarbon.wordpad:id/et_document"
#keyboardsPaths = {1:"com.touchtype.swiftkey/com.touchtype.KeyboardService",2:"com.google.android.inputmethod.latin/com.android.inputmethod.latin.LatinIME",3:"panda.keyboard.emoji.theme/com.android.inputmethod.latin.LatinIME", 4:"com.jb.emoji.gokeyboard/com.jb.gokeyboard.GoKeyboard",5:"com.pinssible.fancykey/.FancyService", 6:"com.sec.android.inputmethod/.SamsungKeypad"}
keyboardsPaths = {2:"com.google.android.inputmethod.latin/com.android.inputmethod.latin.LatinIME",6:"com.sec.android.inputmethod/.SamsungKeypad"}

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



def keyboard_test(adbcl,filename, script_index):
    vc = ViewClient(*ViewClient.connectToDeviceOrExit())
    print(colored("[Testing: "+ script_index + "] " + str(datetime.datetime.now()),"yellow"))
    keyboard.cleaningAppCache(adbcl,package) 
    # initialize app
    getOS()
    keyboard.initProfiler(adbcl,deviceDir)
    keyboard.activateFlags(adbcl,deviceDir)
    
    #extract file
    print(colored("Extracting text file...","white"))
    text_to_insert = keyboard.read_file(filename)
    lines_to_insert = keyboard.split_lines(filename)
    words_to_insert = keyboard.split_words(filename)
    chars_to_insert = keyboard.split_chars(filename)
    #print(len(words_to_insert))
    
    #open App
    keyboard.openApp(adbcl,package)    
    box_to_insert = keyboard.getEditText(vc, edit_text)
    keyboard.openKeyboard(box_to_insert)

    begin_state = localDir + "/begin_state" + str(script_index) + ".json"
    keyboard.getDeviceResourcesState(begin_state)
    
    keyboard.startProfiler(adbcl)
    #keyboard.writeLines(box_to_insert,lines_to_insert)
    keyboard.writeWords(box_to_insert,words_to_insert)
    keyboard.stopProfiler(adbcl)
    end_state = localDir + "/end_state" + str(script_index) + ".json"
    keyboard.getDeviceResourcesState(end_state)

    keyboard.closeApp(adbcl,package)
    keyboard.exitProfiler(adbcl)
    keyboard.getDataResult(deviceDir,localDir,script_index,SED_COMMAND,MV_COMMAND)


if __name__== "__main__":
    if len(sys.argv) > 1:
        filename = sys.argv[1]
        sys.argv.pop(1)
        adbcl = adbclient.AdbClient('.*', settransport=True)
        print(colored("***** [KEYBOARD TEST] *****","blue"))
        for key in keyboardsPaths:
            keyboard.setKeyboard(adbcl,keyboardsPaths[key])
            while script_index < tamanho:
                script_index = script_index + 1
                script_name = str(key) + str(script_index)
                keyboard_test(adbcl,filename, script_name)
            script_index = 0
        print(colored("***** [KEYBOARD TEST - The End] *****","blue"))
    else:
        print (colored("at least 2 args required (text file to insert)","red"))
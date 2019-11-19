#!/usr/bin/env python
# -*- coding: utf-8 -*-
import re
import sys
import os
import subprocess
import io
import json

#from com.android.monkeyrunner import MonkeyRunner, MonkeyDevice
sys.path.append("/Users/tiagofraga/Desktop/HASLAB/Software/AndroidViewClient-15.8.1/src")
from com.dtmilano.android.viewclient import ViewClient
from com.dtmilano.android.adb import adbclient
from os import sys
import time

adbcl = adbclient.AdbClient('.*', settransport=True)

'''
keyboardsPaths ={   
                    1:"com.touchtype.swiftkey",
                    2:"com.google.android.inputmethod.latin",
                    3:"panda.keyboard.emoji.theme",
                    4:"com.jb.emoji.gokeyboard",
                    5:"com.pinssible.fancykey.gifkeyboard",
                    6:"com.sec.android.inputmethod"
                }

all_keyboards = {
    "com.touchtype.swiftkey":"swiftkey",
    "com.google.android.inputmethod.latin":"google",
    "panda.keyboard.emoji.theme":"cheetah",
    "com.jb.emoji.gokeyboard":"go",
    "com.pinssible.fancykey.gifkeyboard":"fancykey",
    "com.sec.android.inputmethod":"samsung"
}

'''

def get_all_keyboards():
    return (adbcl.shell("dumpsys  input_method | grep 'mId' | cut -f2 -d= | cut -f1 -d/").split("\n"))



def show_all_keyboards():
    for keyboard in (adbcl.shell("dumpsys  input_method | grep 'mId' | cut -f2 -d= | cut -f1 -d/").split("\n")):
        print(keyboard)

def show_current_keyboard():
    print(adbcl.shell("dumpsys  input_method | grep 'mCurMethodId' | cut -f2 -d="))

def set_keyboard(key):
    path = keyboardsPaths.get(key)
    adbcl.shell("ime set " + path) 

def detect_android_version():
    x = adbcl.getProperty("ro.build.software.version")
    return (str(x).replace("Android","").split(".")[0])

    #for x in adbcl.shell("  getprop ro.build.software.version | sed \'s/Android//g\' | cut -f1 -d_ | cut -f1 -d." ):
    #"    print ("macaco " + str(x))

def installAPK(apks_folder):
    pattern = re.compile(".*.apk$")
    file_list = [os.path.join(apks_folder, f) for f in os.listdir(apks_folder)]
    print(file_list)
    all_apks = filter(lambda it: pattern.match(str(it)) , file_list )
    nr_apks = len(all_apks)
    if nr_apks==0:
        print ( "erro")
    elif nr_apks ==1:
        print ( " installing 1 apk " )
        result =  subprocess.call( "adb install-multiple  -r " + " ".join(all_apks), shell=True)
        if result==0:
            print( " Keyboard installed")
        #adbcl.shell( " install-multiple  -r " + " ".join(all_apks)) # nao da nao sei pk 
        else:
            print ( " ta male")
        #adbcl.shell( " install -r " + "".join(all_apks) )
    else:
        # several
        print ( " installing " + str(nr_apks) + " apks " )
        print (  " install-multiple  -r " + " ".join(all_apks))
        result =  subprocess.call( "adb install-multiple  -r " + " ".join(all_apks), shell=True)
        if result==0:
            print( " Keyboard installed")
        #adbcl.shell( " install-multiple  -r " + " ".join(all_apks)) # nao da nao sei pk 
        else:
            print ( " ta male")

def uninstallAllKeyboards(all_apks):
    #print ("pm uninstall " +  " ".join(all_apks) )
    #adbcl.shell(" pm uninstall " +  " ".join(all_apks) )
    pattern = re.compile("com.google.android")
    for x in all_apks:
        if not pattern.match(x):
            print("uninstalling " + x)
            uninstallKeyboard(x)

def uninstallKeyboard( keyboard_package):
    adbcl.shell(" pm uninstall " + keyboard_package )

def loadkeyboardInfo():
    with open(os.getcwd()+'/resources/keyboards.json') as json_file:
        data = json.load(json_file)
        keyboardsPaths=data['keyboards_index']
        all_keyboards=data['keyboards_name']
        print(keyboardsPaths)
        print(all_keyboards)
        return keyboardsPaths, all_keyboards

if __name__== "__main__":
    keyboardsPaths, all_keyboards = loadkeyboardInfo()
    android_version = detect_android_version()
    #init(keyboardsPaths, all_keyboards)
    print( "connected device has version %s of Android" % android_version )
    bol = False
    while bol == False:
        print("######################################")
        print("1 -> Show installed Keyboards")
        print("2 -> Show current Keyboard")
        print("3 -> Set Keyboard")
        print("4 -> Install Keyboard")
        print("5 -> Uninstall Keyboards")
        num1 = int(input())
        if num1 == 1:
            show_all_keyboards()
            #bol = True
        elif num1 == 2:
            show_current_keyboard()
            #bol = True
        elif num1 == 3:
            keys = keyboardsPaths.keys()
            print("Choose a Keyboard:")
            num2 = int(input())
            if num2 in keys:
                set_keyboard(num2)
                print("Your current keyboard is: ")
                show_current_keyboard()
                bol = True
            else:
                print("Wrong!!")
        elif num1 == 4:
                print("Choose a Keyboard:")
                for x,y in keyboardsPaths.items():
                    print("-> %s - %s" %(x,all_keyboards.get(y)))
                num2 = str(int(input()))
                if num2 in keyboardsPaths.keys():
                    dir_path = os.getcwd() + "/resources/apks/keyboard_apks/Android_" + android_version+"/" + all_keyboards.get( keyboardsPaths.get((num2)) )
                    if os.path.isdir(dir_path) :
                        print ( " installing apk(s) suited for version %s" % android_version)
                        installAPK(dir_path)
                    else:
                        print("No APKs available for version " + android_version + " folder /resources/apks/keyboard_apks/Android_" + android_version + " not found")
        elif num1 == 5:
            for x,y in keyboardsPaths.items():
                    print("-> %s - %s" %(x,all_keyboards.get(y)))
            print("-> %d - %s"  %(len(keyboardsPaths.keys())+1,"all"))
            num2 = str(int(input()))
            if num2 in keyboardsPaths.keys():
                uninstallKeyboard(keyboardsPaths[(num2)])
            elif int(num2)==len(keyboardsPaths.keys())+1:
                uninstallAllKeyboards(get_all_keyboards())
        else:
            print("Wrong!!")



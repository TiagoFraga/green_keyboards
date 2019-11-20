#!/usr/bin/env python
# -*- coding: utf-8 -*-
import re
import sys
import os
import subprocess
import io
import json

#from com.android.monkeyrunner import MonkeyRunner, MonkeyDevice
#sys.path.append("/Users/tiagofraga/Desktop/HASLAB/Software/AndroidViewClient-15.8.1/src")
sys.path.append(os.getcwd()+"src/")
from com.dtmilano.android.viewclient import ViewClient
from com.dtmilano.android.adb import adbclient
from os import sys
from termcolor import colored
import time

adbcl = adbclient.AdbClient('.*', settransport=True)


def get_all_keyboards():
    return (adbcl.shell("dumpsys  input_method | grep 'mId' | cut -f2 -d= | cut -f1 -d/").split("\n"))


def show_all_keyboards():
    for keyboard in (adbcl.shell("dumpsys  input_method | grep 'mId' | cut -f2 -d= | cut -f1 -d/").split("\n")):
        print(keyboard)

def show_current_keyboard():
    print(adbcl.shell("dumpsys  input_method | grep 'mCurMethodId' | cut -f2 -d="))

def set_keyboard(keyboards_full_definition):
    #path = keyboardsPaths.get(key)
    adbcl.shell("ime set " + keyboards_full_definition) 


def detect_device_model():
    x = adbcl.getProperty("ro.product.model")
    return (str(x).replace(" ",""))


def detect_android_version():
    x = adbcl.getProperty("ro.build.version.release")
    return (str(x).replace("Android","").split(".")[0])


def installAPK(apks_folder):
    pattern = re.compile(".*.apk$")
    file_list = [os.path.join(apks_folder, f) for f in os.listdir(apks_folder)]
    #print(file_list)
    all_apks = filter(lambda it: pattern.match(str(it)) , file_list )
    nr_apks = len(all_apks)
    if nr_apks==0:
        print (colored("[Erro] - Number of apks null","red"))
    elif nr_apks ==1:
        print (colored("installing 1 apk","yellow"))
        result = subprocess.call("adb install   " + " ".join(all_apks), shell=True)
        if result==0:
            print(colored("Keyboard installed","green"))
        #adbcl.shell( " install-multiple  -r " + " ".join(all_apks)) # nao da nao sei pk 
        else:
            print (colored("[Error] - Error installing apk(s)","red"))
        #adbcl.shell( " install -r " + "".join(all_apks) )
    else:
        # several
        print (colored("Installing " + str(nr_apks) + " apks ","yellow"))
        print (colored("Install-multiple " + " ".join(all_apks),"yellow"))
        result =  subprocess.call( "adb install-multiple " + " ".join(all_apks), shell=True)
        if result==0:
            print(colored("Keyboard installed","green"))
        #adbcl.shell( " install-multiple  -r " + " ".join(all_apks)) # nao da nao sei pk 
        else:
            print (colored("[Error] - Error installing apk(s)","red"))

def uninstallAllKeyboards(all_apks):
    #print ("pm uninstall " +  " ".join(all_apks) )
    #adbcl.shell(" pm uninstall " +  " ".join(all_apks) )
    pattern = re.compile("com.google.android")
    for x in all_apks:
        if not pattern.match(x):
            print(colored("Uninstalling " + x,"yellow"))
            uninstallKeyboard(x)

def uninstallKeyboard( keyboard_package):
    print(colored("Going to unistall" + keyboard_package),"yellow")
    adbcl.shell(" pm uninstall " + keyboard_package )

def loadkeyboardInfo():
    with open(os.getcwd()+'/resources/keyboards.json') as json_file:
        data = json.load(json_file)
        keyboardsPaths=data['keyboards_index']
        all_keyboards=data['keyboards_name']
        full_keyboards = data['keyboards_full']
        return keyboardsPaths, all_keyboards, full_keyboards

def installKeyboard(android_version, keyboard_index, keyboardsPaths, all_keyboards ):
    print(colored("installing keyboard " + str(keyboard_index),"yellow"))
    dir_path = os.getcwd() + "/resources/apks/keyboard_apks/Android_" + android_version+"/" + all_keyboards.get( keyboardsPaths.get((keyboard_index)) )
    if os.path.isdir(dir_path) :
        print ("installing apk(s) suited for version %s" % android_version)
        installAPK(dir_path)


if __name__== "__main__":
    keyboardsPaths, all_keyboards, full_keyboards = loadkeyboardInfo()
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
            for x,y in keyboardsPaths.items():
                print("-> %s - %s" %(x,all_keyboards.get(y)))
            print("Choose a Keyboard:")
            num2 = str(int(input()))
            if num2 in keyboardsPaths.keys():
                set_keyboard(full_keyboards[num2])
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



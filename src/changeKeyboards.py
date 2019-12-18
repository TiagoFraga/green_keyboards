#!/usr/bin/env python
# -*- coding: utf-8 -*-
import re
import sys
import os
import subprocess
import io
import json
sys.path.append(os.getcwd()+"src/")
from com.dtmilano.android.viewclient import ViewClient
from com.dtmilano.android.adb import adbclient
from os import sys
from termcolor import colored
import time

#


def get_all_keyboards(adbcl):
    return (adbcl.shell("dumpsys  input_method | grep 'mId' | cut -f2 -d= | cut -f1 -d/").split("\n"))

def get_installed_keyboards(adbcl,keyboard_package_list):
    keyboards_packages= list( map(lambda it: it['package'] , keyboard_package_list ))
    l=[]
    for keyboard in (adbcl.shell("dumpsys  input_method | grep 'mId' | cut -f2 -d= | cut -f1 -d/").split("\n")):
        if str(keyboard).strip() in keyboards_packages:
            l.append(str(keyboard).strip())
    return l

def show_current_keyboard(adbcl,keyboard_dict):
    current = adbcl.shell("dumpsys  input_method | grep 'mCurMethodId' | cut -f2 -d=")
    for key,val in keyboard_dict.items():
        ime = str(val['ime'])
        current_str = str(current).strip()
        if ime == current_str:
            print(colored(val['name'],"green"))

def set_keyboard(adbcl,keyboards_full_definition):
    adbcl.shell("ime set " + keyboards_full_definition)

def get_current_keyboard(adbcl):
    keyboard_dict = loadkeyboardInfo()
    current_keyboard = adbcl.shell("dumpsys  input_method | grep 'mCurMethodId' | cut -f2 -d=")
    return list( map( lambda x : str(x['name']) ,  filter(lambda it : str(it['ime']) == str(current_keyboard).strip() , keyboard_dict.values())))[0]

def detect_device_model(adbcl):
    x = adbcl.getProperty("ro.product.model")
    return (str(x).replace(" ",""))

def detect_android_version(adbcl):
    x = adbcl.getProperty("ro.build.version.release")
    return (str(x).replace("Android","").split(".")[0])


def installAPK(apks_folder):
    pattern = re.compile(".*.apk$")
    file_list = [os.path.join(apks_folder, f) for f in os.listdir(apks_folder)]
    all_apks = filter(lambda it: pattern.match(str(it)) , file_list )
    nr_apks = len(all_apks)
    if nr_apks==0:
        print (colored("[Erro] - Number of apks null","red"))
    elif nr_apks ==1:
        print (colored("installing 1 apk","yellow"))
        result = subprocess.call("adb install   " + " ".join(all_apks), shell=True)
        if result==0:
            print(colored("Keyboard installed","green"))
        else:
            print (colored("[Error] Error installing apk(s)","red"))
    else:
        #several
        result =  subprocess.call( "adb install-multiple " + " ".join(all_apks), shell=True)
        if result==0:
            print(colored("Keyboard installed","green"))
        else:
            print (colored("[Error] Error installing apk(s)","red"))

def uninstallAllKeyboards(adbcl,all_apks):
    pattern = re.compile("com.google.android")
    for x in all_apks:
        if not pattern.match(x):
            print(colored("[Uninstalling] " + x,"yellow"))
            uninstallKeyboard(adbcl,x)

def uninstallKeyboard(adbcl,keyboard_package):
    adbcl.shell("pm uninstall " + keyboard_package)

def uninstallSingleKeyboard(keyboard_name,keyboard_dict):
    for key,val in keyboard_dict.items():
        name = str(val['name'])
        current = str(keyboard_name).strip()
        if name == current:
            print(colored("[Uninstalling] " + name,"yellow"))
            uninstallKeyboard(adbcl,val['package'])

def loadkeyboardInfo():
    with open(os.getcwd()+'/resources/keyboards.json') as json_file:
        data = json.load(json_file)
        return data

def installKeyboard(adbcl,android_version, keyboard_name):
    dir_path = os.getcwd() + "/resources/apks/keyboard_apks/Android_" + android_version+"/" + keyboard_name
    if os.path.isdir(dir_path) :
        #print ("installing apk(s) suited for version %s" % android_version)
        installAPK(adbcl,dir_path)



def show_option_menu():
    print("\n")
    print(colored("***** [Menu] *****","blue"))
    print("1 -> Show installed Keyboards")
    print("2 -> Show current Keyboard")
    print("3 -> Set Keyboard")
    print("4 -> Install Keyboard")
    print("5 -> Uninstall Keyboards")
    print("0 -> Exit")
    print(colored("[Choose Option]","yellow"))


def option1(adbcl):
    android_version,keyboard_dict, installed_keyboards,installed_keyboard_names,all_considered_keyboards = loadInfo(adbcl)
    print(colored("[Installed Keyboards]","green")) 
    for f in installed_keyboard_names:
        print(colored(f,"green"))

def option2(adbcl):
    android_version,keyboard_dict, installed_keyboards,installed_keyboard_names,all_considered_keyboards = loadInfo(adbcl)
    print(colored("[Current Keyboard]","green"))
    current = adbcl.shell("dumpsys  input_method | grep 'mCurMethodId' | cut -f2 -d=")
    for key,val in keyboard_dict.items():
        ime = str(val['ime'])
        current_str = str(current).strip()
        if ime == current_str:
            print(colored(val['name'],"green"))
            

def option3(adbcl):
    android_version,keyboard_dict, installed_keyboards,installed_keyboard_names,all_considered_keyboards = loadInfo(adbcl) 
    print(colored("[Set Keyboard]","green"))
    for x in xrange(0, len(installed_keyboard_names)):
        print(colored("%s -> %s" %(x, installed_keyboard_names[x]),"green"))
    print(colored("[Choose a Keyboard]","yellow"))
    subOp = int(input())
    if subOp < len(installed_keyboards):
        keyboard_ime = list( map( lambda it : str(it['ime']),  filter(lambda it : str(it['name']) == installed_keyboard_names[subOp] , keyboard_dict.values() )))[0]
        set_keyboard(adbcl,keyboard_ime)
        print(colored("[Current Keyboard]","yellow")) 
        show_current_keyboard(keyboard_dict)
    else:
        print(colored("[Wrong option] Please choose a valid one!","red"))


def option4(adbcl):
    android_version,keyboard_dict, installed_keyboards,installed_keyboard_names,all_considered_keyboards = loadInfo(adbcl) 
    print(colored("[Install Keyboard]","green"))
    for x in xrange(0, len(all_considered_keyboards)):
        print(colored("%d -> %s" %(x+1, all_considered_keyboards[x]),"green"))
    print(colored("0 -> Back","white"))
    print(colored("[Choose a Keyboard]","yellow"))
    subOp = int(input())
    if subOp>0 and subOp < len(all_considered_keyboards)+1:
        dir_path = os.getcwd() + "/resources/apks/keyboard_apks/Android_" + android_version+"/" + all_considered_keyboards[subOp-1]
        if os.path.isdir(dir_path) :
            print(colored("Installing apk(s) suited for version %s" % android_version,"yellow"))
            installAPK(dir_path)
            installed_keyboards = get_installed_keyboards(adbcl,keyboard_dict.values())
            installed_keyboard_names = list(map( lambda it : str(it['name'])  ,filter(lambda it : str(it['package']) in installed_keyboards  , keyboard_dict.values() )))
        else:
            print(colored("[Error] No APKs available for version " + android_version + " folder /resources/apks/keyboard_apks/Android_" + android_version + " not found","red"))

def option5(adbcl):
    assoc_keyboard = {}
    android_version,keyboard_dict, installed_keyboards,installed_keyboard_names,all_considered_keyboards = loadInfo(adbcl)
    print(colored("[Uninstall Keyboard]","green"))
    for x in xrange(0, len(installed_keyboard_names)):
        print(colored("%d -> %s" %(x+1, installed_keyboard_names[x]),"green"))
        assoc_keyboard[x] = installed_keyboard_names[x] 
    print(colored("%d -> %s"  %(len(installed_keyboard_names)+1,"all"),"green"))
    print(colored("0 -> Back","white"))
    print(colored("[Choose a Keyboard]","yellow"))
    subOp = int(input())
    if subOp>0 and subOp < len(installed_keyboards)+1:
        uninstallSingleKeyboard(assoc_keyboard[subOp-1],keyboard_dict)
    elif int(subOp) == len(installed_keyboard_names)+1:
        uninstallAllKeyboards(adbcl,installed_keyboards)



def loadInfo(adbcl):
    android_version = detect_android_version(adbcl)
    keyboard_dict = loadkeyboardInfo()    
    installed_keyboards = get_installed_keyboards(adbcl,keyboard_dict.values())    
    installed_keyboard_names = list(map( lambda it : str(it['name'])  ,filter(lambda it : str(it['package']) in installed_keyboards  , keyboard_dict.values() )))
    all_considered_keyboards = list(map(lambda it : str(it['name']), keyboard_dict.values()))
    return android_version,keyboard_dict, installed_keyboards,installed_keyboard_names,all_considered_keyboards


if __name__== "__main__":
    adbcl = adbclient.AdbClient('.*', settransport=True)
    print(colored("***** [CHANGE KEYBOARD] *****","blue"))
    android_version,keyboard_dict, installed_keyboards,installed_keyboard_names,all_considered_keyboards = loadInfo(adbcl) 
    print(colored("[Device] Connected device has version %s of Android." % android_version,"green"))
    bol = False
    while bol == False:
        show_option_menu()
        op = int(input())
        if op == 1:
            option1(adbcl)
        elif op == 2:
            option2(adbcl)
        elif op == 3:
            option3(adbcl)
        elif op == 4:
            option4(adbcl)
        elif op == 5:
            option5(adbcl)
        elif op == 0:
            bol = True
        else:
            print(colored("[Wrong option] Please choose a valid one!","red"))
    print(colored("***** [GOODBYE] *****","blue"))
        

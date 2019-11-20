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


def get_installed_keyboards(keyboard_package_list):
    keyboards_packages= list( map(lambda it: it['package'] , keyboard_package_list ))
    l=[]
    for keyboard in (adbcl.shell("dumpsys  input_method | grep 'mId' | cut -f2 -d= | cut -f1 -d/").split("\n")):
        #print(keyboard)
        if str(keyboard).strip() in keyboards_packages:
            l.append(str(keyboard).strip())
            #print("->"+keyboard_package_list[str(keyboard).strip() ])
    print(l)
    return l
def show_current_keyboard():
    print(adbcl.shell("dumpsys  input_method | grep 'mCurMethodId' | cut -f2 -d="))


def set_keyboard(keyboards_full_definition):
    #path = keyboardsIndex.get(key)
    adbcl.shell("ime set " + keyboards_full_definition) 

def get_current_keyboard():
    keyboard_dict = loadkeyboardInfo()
    current_keyboard = adbcl.shell("dumpsys  input_method | grep 'mCurMethodId' | cut -f2 -d=")
    return list( map( lambda x : str(x['name']) ,  filter(lambda it : str(it['ime']) == str(current_keyboard).strip() , keyboard_dict.values())))[0]



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
    print(colored("Going to unistall" + keyboard_package,"yellow"))
    adbcl.shell("pm uninstall " + keyboard_package )

def loadkeyboardInfo():
    with open(os.getcwd()+'/resources/keyboards2.json') as json_file:
        data = json.load(json_file)
        #keyboardsIndex=data['keyboards_index']
        #keyboards_name_dict=data['keyboards_name']
        #full_keyboards = data['keyboards_full']
        #return keyboardsIndex, keyboards_name_dict, full_keyboards
        return data

def installKeyboard(android_version, keyboard_name):
    print(colored("installing  " + keyboard_name,"yellow"))
    dir_path = os.getcwd() + "/resources/apks/keyboard_apks/Android_" + android_version+"/" + keyboard_name
    if os.path.isdir(dir_path) :
        print ("installing apk(s) suited for version %s" % android_version)
        installAPK(dir_path)



def show_option_menu():
    print("######################################")
    print("1 -> Show installed Keyboards")
    print("2 -> Show current Keyboard")
    print("3 -> Set Keyboard")
    print("4 -> Install Keyboard")
    print("5 -> Uninstall Keyboards")

if __name__== "__main__":
    #keyboardsIndex, keyboards_name_dict, full_keyboards = loadkeyboardInfo()
    keyboard_dict = loadkeyboardInfo()    
    installed_keyboards = get_installed_keyboards(keyboard_dict.values())    
    android_version = detect_android_version()
    installed_keyboard_names = list(map( lambda it : str(it['name'])  ,filter(lambda it : str(it['package']) in installed_keyboards  , keyboard_dict.values() )))
    all_considered_keyboards = list(map(lambda it : str(it['name']), keyboard_dict.values()))
    #init(keyboardsIndex, keyboards_name_dict)
    print( "connected device has version %s of Android" % android_version )
    bol = False
    while bol == False:
        show_option_menu()
        num1 = int(input())
        if num1 == 1:
            print("installed keyboards:")
            for f in installed_keyboard_names:
                print("-> "+f)
        elif num1 == 2:
            show_current_keyboard()
        elif num1 == 3:
            print("installed keyboards:")
            for x in xrange(0, len(installed_keyboard_names)):
                print("-> %s - %s" %(x, installed_keyboard_names[x]))
            print("Choose a Keyboard:")
            num2 = int(input())
            if num2 < len(installed_keyboards):
                keyboard_ime = list( map( lambda it : str(it['ime']),  filter(lambda it : str(it['name']) == installed_keyboard_names[num2] , keyboard_dict.values() )))[0]
                print(keyboard_ime)
                set_keyboard(keyboard_ime)
                print("Your current keyboard is: ")
                show_current_keyboard()
                bol = True
            else:
                print("Wrong option!!")
        elif num1 == 4:
                print("Choose a Keyboard:")
                for x in xrange(0, len(all_considered_keyboards)):
                    print("-> %s - %s" %(x, all_considered_keyboards[x]))
                num2 = int(input())
                if num2 < len(all_considered_keyboards):
                    print( "Installing " + all_considered_keyboards[num2])
                    dir_path = os.getcwd() + "/resources/apks/keyboard_apks/Android_" + android_version+"/" + all_considered_keyboards[num2]
                    if os.path.isdir(dir_path) :
                        print ( " installing apk(s) suited for version %s" % android_version)
                        installAPK(dir_path)
                        installed_keyboards = get_installed_keyboards(keyboard_dict.values())    
                    else:
                        print("No APKs available for version " + android_version + " folder /resources/apks/keyboard_apks/Android_" + android_version + " not found")
        elif num1 == 5:
            for x in xrange(0, len(installed_keyboard_names)):
                print("-> %s - %s" %(x, installed_keyboard_names[x]))
            print("-> %d - %s"  %(len(installed_keyboard_names),"all"))
            num2 = int(input())
            if num2 < len(installed_keyboards):
                uninstallKeyboard(installed_keyboards[num2])
            elif int(num2)==len(installed_keyboard_names):
                print(installed_keyboards)
                uninstallAllKeyboards(installed_keyboards)
                installed_keyboards = get_installed_keyboards(keyboard_dict.values())    
        else:
            print("Wrong!!")
        

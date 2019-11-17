#!/usr/bin/env python
# -*- coding: utf-8 -*-
import re
import sys
import os
import io


#from com.android.monkeyrunner import MonkeyRunner, MonkeyDevice
sys.path.append("/Users/tiagofraga/Desktop/HASLAB/Software/AndroidViewClient-15.8.1/src")
from com.dtmilano.android.viewclient import ViewClient
from com.dtmilano.android.adb import adbclient
from os import sys
import time

adbcl = adbclient.AdbClient('.*', settransport=True)
keyboardsPaths = {1:"com.touchtype.swiftkey/com.touchtype.KeyboardService",2:"com.google.android.inputmethod.latin/com.android.inputmethod.latin.LatinIME",3:"panda.keyboard.emoji.theme/com.android.inputmethod.latin.LatinIME", 4:"com.jb.emoji.gokeyboard/com.jb.gokeyboard.GoKeyboard",5:"com.pinssible.fancykey/.FancyService", 6:"com.sec.android.inputmethod/.SamsungKeypad"}
all_keyboards = {}

def show_all_keyboards():
    print(adbcl.shell("dumpsys  input_method | grep 'mId' | cut -f2 -d="))

def show_current_keyboard():
    print(adbcl.shell("dumpsys  input_method | grep 'mCurMethodId' | cut -f2 -d="))

def set_keyboard(key):
    path = keyboardsPaths.get(key)
    adbcl.shell("ime set " + path) 

if __name__== "__main__":
    bol = False
    while bol == False:
        print("######################################")
        print("1 -> Show all Keyboards")
        print("2 -> Show current Keyboard")
        print("3 -> Set Keyboard")
        num1 = int(input())
        if num1 == 1:
            show_all_keyboards()
            bol = True
        elif num1 == 2:
            show_current_keyboard()
            bol = True
        elif num1 == 3:
            keys = keyboardsPaths.keys()
            print(keyboardsPaths)
            print("Choose a Keyboard:")
            num2 = int(input())
            if num2 in keys:
                set_keyboard(num2)
                print("Your current keyboard is: ")
                show_current_keyboard()
                bol = True
            else:
                print("Wrong!!")
        else:
            print("Wrong!!")



#!/usr/bin/env python
# -*- coding: utf-8 -*-

import re
import sys
import os
import io
import time
import datetime
import json
import string
from termcolor import colored

###############################
## Test File Auxiliar Functions 
###############################    

def read_file(filename):
    f = open(filename, "r")
    texto = f.read()
    return texto

def split_lines(filename):
   whiteSpaceRegex = r"\\s";
   lines = []
   with io.open(filename, "r", encoding='utf-8') as f:
       lines = f.readlines()
   return lines

def split_words(filename):
   whiteSpaceRegex = r"\\s";
   words = []
   lines = []
   with io.open(filename, "r", encoding='utf-8') as f:
       for line in f.read().split('\n'):
           lines.append(line)
       
   for line in lines:
        if(line == ''):
            words.append('\n')
        else:
            arr = line.split(' ')
            for w in arr:
                words.append(w)
                words.append(' ')
   return words

def split_chars(filename):
   words = split_words(filename)
   chars = []
   for word in words:
        if word == ' ':
            chars.append(' ')
        elif word == '\n':
            chars.append('\n')
        else:
            for c in word:
                chars.append(c)
   return chars

def getEmail(filename):
    with open(filename) as json_file:
        data_mail = json.load(json_file)
    return data_mail

def text_to_lines(text):
   lines = []
   lines = text.split('\n')
   return lines

def text_to_words(text):
   words = []
   lines = text_to_lines(text)
   for line in lines:
        arr = line.split(' ')
        for w in arr:
            words.append(w)
            words.append(' ')
        words.append('\n')
   return words

def text_to_chars(text):
   chars = []
   words = text_to_words(text)
   for word in words:
        if word == ' ':
            chars.append(' ')
        elif word == '\n':
            chars.append('\n')
        else:
            for c in word:
                chars.append(c)
   return chars



##################################
## Device State Auxiliar Functions 
##################################
  

def getDeviceResourcesState(arg):
    # three numbers represent averages over progressively longer periods of time (one, five, and fifteen minute averages)
    print(colored("collecting device resources state","yellow"))
    '''
    used_cpu = os.system("adb shell dumpsys cpuinfo | grep  'Load' | cut -f2 -d: | sed 's/ //g'")
    mem = os.system("adb shell dumpsys meminfo | grep 'Used RAM.*'")
    used_mem_pss = os.system("echo " + str(mem) + " |  cut -f2 -d\(   | cut -f1 -d+ | cut -f1 -d\ ")
    used_mem_kernel = os.system("echo " + str(mem) + " |  cut -f2 -d\(   | cut -f2 -d+     |  sed 's/kernel)//g' | sed 's/ //g' ")
    nr_processes = os.system("adb shell ps -o STAT  | egrep '^R|L' | wc -l | sed 's/ //g' ")
    battery = os.system("adb shell dumpsys battery")
    ischarging = os.system("echo " + str(battery) + " | grep 'powered' |  grep 'true' | wc -l | sed 's/ //g' ")
    battery_level = os.system("echo " + str(battery) + " | grep 'level:' | cut -f2 -d\: | sed 's/ //g' ")
    keyboard = os.system("adb shell dumpsys  input_method | grep 'mCurMethodId' | cut -f2 -d= ")
    battery_temperature = os.system("echo " + str(battery) + " | grep 'temperature:'  | cut -f2 -d\: | sed 's/ //g' ")
    battery_voltage = os.system("echo " + str(battery) + " | grep 'voltage:' | tail -1 | cut -f2 -d\: | sed 's/ //g'")
    timestamp = str(datetime.datetime.now())
    echo_string = {"timestamp": timestamp,
		           "used_cpu": used_cpu,
		           "used_mem_pss": used_mem_pss,
		           "used_mem_kernel": used_mem_kernel,
		           "nr_processes": nr_processes, 
		           "ischarging": ischarging,
		           "battery_level": battery_level,
		           "battery_temperature": battery_temperature,
		           "keyboard": keyboard,
		           "battery_voltage": battery_voltage
               	}
    print("###############################################")
    print("###############################################")
    print("###############################################")
    print(echo_string)
    print("###############################################")
    print("###############################################")
    print("###############################################")
    json_string = json.dumps(echo_string)
    file_to_write = open(arg,"w")
    file_to_write.write(json_string)
    file_to_write.close()
    '''
    os.system("./src/getDeviceResourcesState.sh " + arg)
    print(colored("device resources state are collected","green"))
    time.sleep(1)




####################################
## Trepn Profiler Auxiliar Functions 
#################################### 


def initProfiler(adbcl,deviceDir):
    print(colored("initializing the profiler","yellow"))
    adbcl.shell("monkey -p com.quicinc.trepn -c android.intent.category.LAUNCHER 1")
    time.sleep(1)
    adbcl.shell("am startservice --user 0 com.quicinc.trepn/.TrepnService")
    time.sleep(2)
    adbcl.shell("am start -a android.intent.action.MAIN -c android.intent.category.HOME")
    time.sleep(3)
    print(colored("profiler is runing ...","green"))
    adbcl.shell("> "+ deviceDir +"/TracedMethods.txt")


def startProfiler(adbcl):
    print(colored("starting profiler phase","yellow"))
    adbcl.shell("am broadcast -a com.quicinc.trepn.start_profiling -e com.quicinc.trepn.database_file 'myfile' ")
    time.sleep(3)
    print(colored("[Measuring] " + str(datetime.datetime.now()) ,"yellow"))
    adbcl.shell("am broadcast -a com.quicinc.Trepn.UpdateAppState -e com.quicinc.Trepn.UpdateAppState.Value '1' -e com.quicinc.Trepn.UpdateAppState.Value.Desc 'started' ")


def stopProfiler(adbcl):
    adbcl.shell("am broadcast -a com.quicinc.Trepn.UpdateAppState -e com.quicinc.Trepn.UpdateAppState.Value '0' -e com.quicinc.Trepn.UpdateAppState.Value.Desc 'stopped' ")
    print(colored("ending profiler phase","green"))


def exitProfiler(adbcl):
    print(colored("exit profiler","yellow"))
    time.sleep(1)
    adbcl.shell("am broadcast -a com.quicinc.trepn.stop_profiling")
    time.sleep(6)
    adbcl.shell ("am broadcast -a  com.quicinc.trepn.export_to_csv -e com.quicinc.trepn.export_db_input_file 'myfile' -e com.quicinc.trepn.export_csv_output_file 'GreendroidResultTrace0'")
    time.sleep(1)

def activateFlags(adbcl,deviceDir):
    adbcl.shell("echo 1 > "+deviceDir+"/GDflag")


#########################
## App Auxiliar Functions 
#########################

def openApp(adbcl,package):
    print(colored("App is starting ...","white"))
    adbcl.shell("monkey -p " + package + " -c android.intent.category.LAUNCHER 1")
    time.sleep(5)


def firstWindow_googledocs(vc):
    vc.dump(window=-1)
    firstbutton = vc.findViewById("com.google.android.apps.docs.editors.docs:id/fab_base_button")
    firstbutton.touch()
    time.sleep(5)
    

def firstWindow_gmail(vc):
    vc.dump(window=-1)
    firstbutton = vc.findViewById("com.google.android.gm:id/compose_button")
    firstbutton.touch()
    time.sleep(5)


def getEditText(vc, edit_text):
    print(colored("Get edit text id...","white"))
    vc.dump(window=-1)
    text = vc.findViewById(edit_text)
    return text

def openKeyboard(edit_text):
    print(colored("Open Keyboard...","white"))
    edit_text.touch()
    time.sleep(1)



def writeLines(text,lines_to_insert):
    for word in lines_to_insert:
        word_str = word.encode('ascii','replace')
        text.type(word_str,alreadyTouched=True)


def writeWords(text,words_to_insert):
    for word in words_to_insert:
        word_str = word.encode('ascii','replace')
        if word_str == '\n':
            text.type_without_sleep('\n',alreadyTouched=True)
            #time.sleep(1)
        else:
            text.type_without_sleep(word_str,alreadyTouched=True)
        #time.sleep(1)

def prepareEmail(vc,adbcl,data_mail):
    vc.dump(window=-1)
    to_text = vc.findViewById("com.google.android.gm:id/to")
    subject_text = vc.findViewById("com.google.android.gm:id/subject")
    mail_text = vc.findViewById("id/no_id/14")
    input_to = data_mail.get("to")
    to_str = input_to.encode('ascii','replace')
    input_subject = data_mail.get("subject")
    subject_str = input_subject.encode('ascii','replace')
    to_text.touch()
    adbcl.type(to_str) 
    subject_text.type(subject_str)
    mail_text.touch()
    return mail_text

        

def sendEmail(vc):
    vc.dump(window=-1)
    send_btn = vc.findViewById("com.google.android.gm:id/send")
    send_btn.touch()



def closeApp(adbcl,package):
    print(colored("closing App...","yellow"))
    time.sleep(1) 
    adbcl.shell("am force-stop "+ package)


def setImmersiveMode(adbcl,package):
    print(colored("setting imersive mode","yellow"))
    adbcl.shell("settings put global policy_control immersive.full="+ package)
    print(colored("imersive mode on","green"))
      

def cleaningAppCache(adbcl,package):
    print(colored("cleaning app cache ...","yellow"))
    adbcl.shell("pm clear "+ package) 



##########################
## Data Auxiliar Functions 
##########################

def getDataResult(deviceDir,localDir,script_index,SED_COMMAND,MV_COMMAND):
    print(colored("collecting data ...","yellow"))
    time.sleep(10)
    os.system("adb shell ls " + deviceDir + " | " + SED_COMMAND + " -r 's/[\r]+//g' | egrep -Eio '.*.csv' |  xargs -I{} adb pull "+ deviceDir + "/{} " + localDir)
    #os.system("adb shell ls " + deviceDir + "/TracedMethods.txt | tr '\r' ' ' | xargs -n1 adb pull")
    os.system("adb shell ls " + deviceDir + " | " + SED_COMMAND + " -r 's/[\r]+//g' | egrep -Eio TracedMethods.txt | xargs -I{} adb pull " + deviceDir + "/{} " + localDir)
    os.system(MV_COMMAND + " " + localDir + "/TracedMethods.txt " + localDir + "/TracedMethods" + str(script_index) + ".txt")
    os.system(MV_COMMAND + " " + localDir + "/GreendroidResultTrace0.csv " + localDir + "/GreendroidResultTrace" + str(script_index) +".csv")


##########################
## Keyboard Auxiliar Functions 
##########################

def setKeyboard(adbcl,key):
    print(colored("setting keyboard","yellow"))
    adbcl.shell("ime set " + key)
    current = "[Current Keyboard] " + adbcl.shell("dumpsys  input_method | grep 'mCurMethodId' | cut -f2 -d=")
    print(colored(current,"green"))
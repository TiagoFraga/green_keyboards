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
#from edited_edit_text import EditedEditText
from termcolor import colored
from difflib import SequenceMatcher

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

def getCoords(filename,keyboard_key):
    name = ''
    with open(filename) as json_file:
        dic = json.load(json_file)
    if keyboard_key == 1:
        name = "swift"
    elif keyboard_key == 2:
        name = "gboard"
    else:
        name = "samsung"
    coords = dic.get(name)
    return coords

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

def similar(a, b):
    return SequenceMatcher(None, a, b).ratio()

def cleanList(a):
    new_a = []
    for word in a:
        if word != ' ' and word != '' and word != '\n':
            new_a.append(word)
    
    return new_a


'''
def my_similar(written_words,espected_words):
    total_espected = len(espected_words)
    total_written = len(written_words)
    correct = 0
    if total_espected == total_written:
        for i, val in enumerate(espected_words):
            e_word = espected_words[i]
            w_word = written_words[i]
            if (e_word == w_word):
                correct = correct + 1
    elif total_espected < total_written:
        
    else:
        accuracy = -1
'''



def my_similar(written_words, espected_words):
    total_espected = len(espected_words)
    total_written = len(written_words)

    correct = 0
    j = 0
    for i, val in enumerate(espected_words):
        e_word = espected_words[i]
        bol = False
        while bol == False:
            w_word = written_words[j]
            if len(w_word) > 1:
                if (w_word != '') and (e_word != ''):    
                    if (w_word != ' ') and (e_word != ' '):
                        if (w_word != '\n') and (e_word != '\n'):
                            if w_word[0] == e_word[0]:
                                bol = True
                                if (w_word == e_word):
                                    correct = correct + 1
                                    j = j+1
                                else: 
                                    j=j+1
                            else:
                                j=j+1
            else:
                j=j+1
    accuracy = (correct / total_espected) * 100

def getSelectedWords(espected_words,suggested_length):
    new = []
    for word in espected_words:
        word_str = word.encode('ascii','replace')
        if word_str != ' ' and word_str !='\n' and word_str != '':
            string = ""
            tamanho = len(word_str)
            tamanho_to_write = (int(tamanho) * int(suggested_length)) / 100
            if tamanho_to_write == 0:
               tamanho_to_write = 1
            for c in word_str:
                if tamanho_to_write > 0:
                   string = string + c 
                   tamanho_to_write = tamanho_to_write - 1
            new.append(string)
    return new
    


def writeAccuracy(written, espected,script_index,suggested_length):
    print(colored("Calculating accuracy","yellow"))
    written_words = text_to_words(written)
    espected_words = text_to_words(espected)
    #accuracy = similar(written_words,espected_words)
    #accuracy = list_similar(written_words,espected_words)
    #accuracy = my_similar(written_words,espected_words)
    selected_words = getSelectedWords(espected_words,suggested_length)
    print(cleanList(written_words))
    print(cleanList(espected_words))
    print(cleanList(selected_words))
    f = open("./Accuracy/"+script_index+".txt","w+")
    string = "[Espected] \n" + str(cleanList(espected_words)) + "\n\n" + "[Selected] \n " + str(selected_words) + "\n\n" + "[Written] \n " + str(cleanList(written_words)) + "\n\n"  
    f.write(string)
    f.close()
    print(colored("Calculating accuracy done","green"))




##################################
## Device State Auxiliar Functions 
##################################
  
def getDeviceState(arg):
    print(colored("collecting device specs","yellow"))
    os.system("./src/getDeviceState.sh " + arg)
    print(colored("device specs collected","green"))
    time.sleep(1)

def getDeviceSpecs(arg):
    print(colored("collecting device specs","yellow"))
    os.system("./src/getDeviceSpecs.sh " + arg)
    print(colored("device specs collected","green"))
    time.sleep(1)


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

'''
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
'''

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
        #edited_view = EditedEditText(text)
        if word_str == '\n':
            #edited_view.type_without_sleep('\n',alreadyTouched=True)
            text.type_without_sleep('\n',alreadyTouched=True)
            #time.sleep(1)
        else:
            #edited_view.type_without_sleep(word_str,alreadyTouched=True)
            text.type_without_sleep(word_str,alreadyTouched=True)
        #time.sleep(1)

def writeSuggestedWords(vc,text,words_to_insert,coords,suggested_length):
    for word in words_to_insert:
        word_str = word.encode('ascii','replace')
        #edited_view = EditedEditText(text)
        if word_str == '\n':
            #edited_view.type_without_sleep('\n',alreadyTouched=True)
            text.type_without_sleep('\n',alreadyTouched=True)
            #time.sleep(1)
        elif word_str == ' ':
            #edited_view.type_without_sleep(' ',alreadyTouched=True)
            text.type_without_sleep(' ',alreadyTouched=True)
        else:
            tamanho = len(word_str)
            tamanho_to_write = (int(tamanho) * int(suggested_length)) / 100
            if tamanho_to_write == 0:
                tamanho_to_write = 1
            for c in word_str:
                if tamanho_to_write > 0:
                    #edited_view.type_without_sleep(c,alreadyTouched=True)
                    text.type_without_sleep(c,alreadyTouched=True)
                    tamanho_to_write = tamanho_to_write - 1
                elif tamanho_to_write == 0:
                    reco = coords.get("reco") 
                    option = coords.get(reco)
                    vc.touch(int(option[0]),int(option[1]))
                    tamanho_to_write = tamanho_to_write - 1

def getText(vc,edit_text):
    print(colored("get written text","yellow"))
    time.sleep(2)
    box_to_insert = getEditText(vc, edit_text)
    text = box_to_insert.getText()
    time.sleep(2)
    return text
                

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
    print(colored("cleaning " + package + " cache ...","yellow"))
    adbcl.shell("pm clear "+ package)


##########################
## Data Auxiliar Functions 
##########################

'''
def getDataResult(deviceDir,localDir,script_index,SED_COMMAND,MV_COMMAND):
    print(colored("collecting data ...","yellow"))
    time.sleep(10)
    os.system("adb shell ls " + deviceDir + " | " + SED_COMMAND + " -r 's/[\r]+//g' | egrep -Eio '.*.csv' |  xargs -I{} adb pull "+ deviceDir + "/{} " + localDir)
    #os.system("adb shell ls " + deviceDir + "/TracedMethods.txt | tr '\r' ' ' | xargs -n1 adb pull")
    os.system("adb shell ls " + deviceDir + " | " + SED_COMMAND + " -r 's/[\r]+//g' | egrep -Eio TracedMethods.txt | xargs -I{} adb pull " + deviceDir + "/{} " + localDir)
    os.system(MV_COMMAND + " " + localDir + "/TracedMethods.txt " + localDir + "/TracedMethods" + str(script_index) + ".txt")
    os.system(MV_COMMAND + " " + localDir + "/GreendroidResultTrace0.csv " + localDir + "/GreendroidResultTrace" + str(script_index) +".csv")
'''

##########################
## Keyboard Auxiliar Functions 
##########################

def setKeyboard(adbcl,key):
    print(colored("setting keyboard","yellow"))
    adbcl.shell("ime set " + key)
    current = "[Current Keyboard] " + adbcl.shell("dumpsys  input_method | grep 'mCurMethodId' | cut -f2 -d=")
    print(colored(current,"green"))
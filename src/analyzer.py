#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os
import time
import datetime
import shutil
import changeKeyboards as change

def analyzeResults(results_path):
        os.system( "java -jar ./resources/jars/AnaDroidAnalyzer.jar -TestOriented "+ results_path + " -none NONE" )
        trimmed_date = str(datetime.datetime.now()).replace(":","").replace(" ","").replace(".","")
        new_dir= results_path + "/" + trimmed_date
        os.mkdir(new_dir)
        for file in os.listdir(results_path):
            full_file_name = os.path.join(results_path, file)
            if os.path.isfile(full_file_name):
                shutil.copy(full_file_name, new_dir)


def initLocalResultsDir(keyboard_name, android_version,output_dir, device_serial_nr, test_type):
    output_dir_1 =  os.getcwd() + output_dir +"/"
    if not os.path.exists( output_dir_1 ):
        os.mkdir(output_dir_1)
    output_dir_android = output_dir_1 +"/" + android_version + "/" 
    if not os.path.exists( output_dir_android ):
        os.mkdir(output_dir_android)
    model_dir = output_dir_android + "/" + change.detect_device_model()
    if not os.path.exists( model_dir ):
        os.mkdir(model_dir)
    serial_dir = model_dir + "/" + device_serial_nr
    if not os.path.exists( serial_dir ):
        os.mkdir(serial_dir)
    type_dir = serial_dir  + '/' + test_type
    if not os.path.exists( serial_dir ):
        os.mkdir(serial_dir)
    target_dir = serial_dir + "/" + keyboard_name
    if not os.path.exists( target_dir ):
        os.mkdir(target_dir)
    else: 
        #already exists, wipe files of folder
        for file in os.listdir(target_dir):
            full_file_name = os.path.join(target_dir, file)
            if os.path.isfile(full_file_name):
                os.remove(full_file_name)
    return target_dir

def calculateExtraSleep(begin, end, fmt):
    d1 = datetime.datetime.strptime(str(begin),fmt)
    d2 = datetime.datetime.strptime(str(end),fmt)
    diff = d2-d1
    return diff.seconds/60

def alert():
    timex = 30
    while(timex > 0):
        os.system("say -v diego ' muda o teclado!!!!!' ")
        timex = timex -1
        time.sleep(10)
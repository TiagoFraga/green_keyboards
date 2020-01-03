#!/usr/bin/env python
# -*- coding: utf-8 -*-
import re
import sys
import os
import io
import json
from termcolor import colored

output_folder = './out_final/'
list_of_fildes = ['cpuloadnormalized','memoryusage','energyconsumed','elapsedtime']

def data_to_csv(data,string_folder):
    total_gpuload = 0
    total_cpuloadnormalized = 0
    total_memoryusage = 0
    total_enegyconsumed = 0
    total_elapsedtime = 0
    f = open(string_folder + "all_data.csv", "w")
    f.write("test_id; energy cons (J); time elapsed (ms); cpuloadnormalized (%); memoryusage (KB); gpuload (%)")
    f.write('\n')
    for line in data:
        #total_gpuload = total_gpuload + float(line['gpuload'])
        total_cpuloadnormalized = total_cpuloadnormalized + float(line['cpuloadnormalized'])
        total_memoryusage = total_memoryusage + float(line['memoryusage'])
        total_enegyconsumed = total_enegyconsumed + float(line['energyconsumed'])
        total_elapsedtime = total_elapsedtime + float(line['elapsedtime'])
        f.write(str(line['test_id']) + ';' + str(line['energyconsumed'])+ ';' + str(line['elapsedtime']) + ';' + str(line['cpuloadnormalized']) + ';' + str(line['memoryusage']) + ';' + str(line['gpuload']))
        f.write('\n')
    if len(data)==0:
        size = 1
    else:
        size = len(data)
    average_gpuload =  total_gpuload / size
    average_cpuloadnormalized = total_cpuloadnormalized / size
    average_memoryusage = total_memoryusage / size
    average_enegyconsumed = total_enegyconsumed / size
    average_elapsedtime = total_elapsedtime / size
    f.write('average' + ';' + str(average_enegyconsumed)+ ';' + str(average_elapsedtime) + ';' + str(average_cpuloadnormalized) + ';' + str(average_memoryusage) + ';' + str(average_gpuload))
    f.write('\n')
    f.close()

def sort_data(data):
    new = {}
    for stat in data:
        new['test_id'] = stat['test_results']
        if stat['metric'] == 'cpuloadnormalized':
            value = stat['value_text'].split(',')[1]
            new[stat['metric']] = value
        elif stat['metric'] == 'memoryusage':
            value = stat['value_text'].split(',')[1]
            new[stat['metric']] = value
        elif stat['metric'] == 'gpuload':
            value = stat['value_text'].split(',')[1]
            new[stat['metric']] = value
        else:
            if stat['metric'] in list_of_fildes:
                new[stat['metric']] = stat['value_text']
    return new


def getStats(all_folders):
    for folder in all_folders:
        stats = []
        string_folder = folder + "/"
        for filename in os.listdir(folder):
            if filename.endswith(".json") and filename.startswith('t'):
                with open(string_folder + filename) as json_file:
                    new = []
                    data = json.load(json_file)
                    data_sorted = sort_data(data)
                    stats.append(data_sorted)
        data_to_csv(stats,string_folder)

def getFolders():
    all_folders = []
    keyboard_folders = []
    for (dirpath, dirnames, filenames) in os.walk(output_folder):
        folders = dirpath.split('/')
        if len(folders) == 8:
            all_folders.append(dirpath)
        if len(folders) == 7:
            keyboard_folders.append(dirpath)
    return all_folders,keyboard_folders

def cleanFolders(keyboard_folders):
    for folder in keyboard_folders:
        for filename in os.listdir(folder):
            str_filename = folder + '/' + filename
            if os.path.isfile(str_filename):
                os.remove(str_filename)


if __name__== "__main__":
    all_folders,keyboard_folders = getFolders()
    cleanFolders(keyboard_folders)
    getStats(all_folders)
    print(colored("[Success] Created " + str(len(all_folders)) + " resume files!","green"))
    
            
                        
        



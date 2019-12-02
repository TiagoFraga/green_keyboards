#!/usr/bin/env python
# -*- coding: utf-8 -*-
import re
import sys
import os
import io
import json

#folder = './../outputs/'
folder = '/Users/tiagofraga/Desktop/HASLAB/Keyboard/Local/green_keyboards/outputs/6/Nexus5/google/'
list_of_fildes = ['gpuload','cpuloadnormalized','memoryusage','energyconsumed','elapsedtime']
import json

def data_to_csv(data):
    f = open(folder + "all_data.csv", "w")
    f.write("test_id, energy cons (J), time elapsed (ms), cpuloadnormalized (%), memoryusage (KB), gpuload (%)")
    f.write('\n')
    for line in data:
        f.write(str(line['test_id']) + ',' + str(line['energyconsumed'])+ ',' + str(line['elapsedtime']) + ',' + str(line['cpuloadnormalized']) + ',' + str(line['memoryusage']) + ',' + str(line['gpuload']))
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


#def getStats(android_version,keyboard_name):
def getStats():
    stats = []
    #folder_to_search = folder + android_version + "/" + keyboard_name
    folder_to_search = folder
    for filename in os.listdir(folder_to_search):
        if filename.endswith(".json") and filename.startswith('t'):
            with open(folder + filename) as json_file:
                new = []
                data = json.load(json_file)
                data_sorted = sort_data(data)
                stats.append(data_sorted)
    data_to_csv(stats)

getStats()
            
                        
        



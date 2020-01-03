#!/usr/bin/env python

import numpy as np
import matplotlib.pyplot as plt
import os, sys
import subprocess
import csv
import itertools

min_csv_row_len=10

def fetch_all_data_csvs(folder):
    ret_list = []
    output = subprocess.check_output("find %s -type f -name \"all_data.csv\"" % folder, shell=True)
    for x in output.strip().split("\n"):
        ret_list.append(x)
    return ret_list


def sort_csv_test_id(csv_file):
    reader = csv.reader(open(csv_file), delimiter=";")
    header = next(reader)
    csv_row_list = list(reader)
    avg_row = csv_row_list[-1]
    sortedlist = sorted(csv_row_list[:-1], key=lambda row: int(row[0]))
    return header, sortedlist, avg_row

def generate_box_plots(csvs_dict):
    
    # energy boxplot
    generate_box_plots_from_column(" energy cons (J)", csvs_dict )
    generate_box_plots_from_column( ' time elapsed (ms)', csvs_dict)
    #generate_box_plots_from_column(" energy cons (J)", csvs_dict )
    generate_box_plots_from_column( ' cpuloadnormalized (%)', csvs_dict)
    generate_box_plots_from_column( ' memoryusage (KB)', csvs_dict)



def extract_keyboard_name(file_name):
    if "cheetah" in file_name:
        return "cheetah"
    elif  "google" in file_name:
        return "google"
    elif  "go" in file_name:
        return "go"
    elif  "swiftkey" in file_name:
        return "swiftkey"
    elif  "fancykey" in file_name:
        return "fancykey"
    elif  "samsung" in file_name:
        return "samsung"
    else:
        return "bieira"


def generate_box_plots_from_column(col_name , csvs_dict):
    fig1, en_box = plt.subplots()
    en_box.set_title(col_name)
    list_all_samples = []
    list_labels= []
    for x in csvs_dict.keys():
        triple = csvs_dict[x]
        list_labels.append(extract_keyboard_name(x))
        header = triple[0]
        sorted_csv = triple[1]
        values = get_column_values(col_name, header, sorted_csv)
        list_all_samples.append(values)
    
    #en_box.set_ylabel('Energy (J)')
    en_box.set_xlabel('Keyboard')
    en_box.boxplot(list_all_samples) 
    xtickNames = plt.setp(en_box, xticklabels=list_labels)
    plt.setp(xtickNames, rotation=0, fontsize=8)




def get_column_values( header_str,header,sorted_csv):
    energy_col_index = header.index(header_str)
    energy_values =map( lambda x :  float(x[energy_col_index]) , sorted_csv )
    return energy_values
    

def generate_test_behaviour_graphs(csvs_dict):
    generate_test_behaviour_graph(" energy cons (J)", csvs_dict )        




def generate_test_behaviour_graph(col_name, csvs_dict):
    fig1, line = plt.subplots()
    list_all_samples = []
    for x in csvs_dict.keys():
        triple = csvs_dict[x]
        label = (extract_keyboard_name(x))
        header = triple[0]
        sorted_csv = triple[1]
        values = get_column_values(col_name, header, sorted_csv)    
        n_tests =  get_column_values("test_id", header, sorted_csv )
        list_all_samples.append((values,n_tests,label))
        
    for l , s , label in list_all_samples:
        line.plot(s,l, label=label)


if __name__== "__main__":
    if len(sys.argv) > 1:
        device_folder = sys.argv[1]
        all_csvs_of_folder = fetch_all_data_csvs(device_folder)
        csvs_dict={}
        for csv_file in all_csvs_of_folder:
            header, sortedlist, avg_row = sort_csv_test_id(csv_file)
            if len( sortedlist) >= min_csv_row_len :
                csvs_dict[csv_file] = (header, sortedlist, avg_row)
                #generate_box_plot(header,sortedlist)
        generate_test_behaviour_graphs(csvs_dict)
        generate_box_plots(csvs_dict)
        plt.show()
    else:
        print ("bad arg len")
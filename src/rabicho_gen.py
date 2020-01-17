#import seaborn as sns
import numpy as np
import matplotlib.pyplot as plt
import os, sys
import subprocess
import csv
import itertools
from pylab import *
from termcolor import colored
from collections import OrderedDict 


min_csv_row_len=10

def fetch_all_data_csvs(folder):
    ret_list = []
    output = subprocess.check_output("find %s -type f -name \"all_data.csv\"" % folder, shell=True)
    for x in output.decode("utf-8").strip().split("\n"):
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
    generate_box_plots_from_column(" energy cons (J)", csvs_dict , title = "Energy consumed (J)" )
    generate_box_plots_from_column( ' time elapsed (ms)', csvs_dict, yfactor=1000, title = "Elapsed Time (s)")
    #generate_box_plots_from_column(" energy cons (J)", csvs_dict )
    generate_box_plots_from_column( ' cpuloadnormalized (%)', csvs_dict , title="CPU Load (%)")
    generate_box_plots_from_column( ' memoryusage (KB)', csvs_dict, yfactor=(1024*1024), title = "Memory (GB)")



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

def extract_keyboard_mode(file_name):
    if "default" in file_name:
        return "default"
    elif  "minimal" in file_name:
        return "minimal"
    else:
        return "bieira"


def generate_box_plots_from_column(col_name , csvs_dict, yfactor=1, title=''):
    fig1, en_box = plt.subplots()
    if title=='':
        title=col_name
    en_box.set_title(title)
    dict_keyboard_samples = OrderedDict() 
    list_all_samples = []
    for x in csvs_dict.keys():
        triple = csvs_dict[x]
        header = triple[0]
        sorted_csv = triple[1]
        values = get_column_values(col_name, header, sorted_csv, factor=yfactor)
        list_all_samples.append(values)
        keyboard_mode = extract_keyboard_mode(x)
        keyboard_name = extract_keyboard_name(x)
        if  keyboard_name in dict_keyboard_samples.keys():
            dict_keyboard_samples[keyboard_name][keyboard_mode] = values
        else:
            dict_keyboard_samples[keyboard_name] = {}
            dict_keyboard_samples[keyboard_name][keyboard_mode] = values

    
    final_res_dic = OrderedDict()
    for kbname in dict_keyboard_samples.keys() :
        kb_modes_dict = dict_keyboard_samples[kbname]
        for kbmode in kb_modes_dict:
            final_res_dic [kbname+"_"+kbmode] = kb_modes_dict[kbmode]
    #en_box.set_ylabel('Energy (J)')
    en_box.set_xlabel('Keyboard')
    bp_dict = en_box.boxplot(final_res_dic.values())
    i = 0
    for line in bp_dict['medians']:
        x, y = line.get_xydata()[1] # top of median line
        xx, yy =line.get_xydata()[0] 
        text(x, y, '%.2f' % y) # draw above, centered
        text(xx, en_box.get_ylim()[1] * 0.98, '%.2f' % np.average(list_all_samples[i]), color='darkkhaki') 
        i = i +1
    #for line in bp_dict['boxes']:
    #    x, y = line.get_xydata()[0] # bottom of left line
    #    text(x,y, '%.2f' % y, horizontalalignment='center', verticalalignment='top')      # below
        #x, y = line.get_xydata()[3] # bottom of right line
       #text(x,y, '%.2f' % y, horizontalalignment='center', verticalalignment='top')      # below
    xtickNames = plt.setp(en_box, xticklabels=final_res_dic.keys())
    plt.setp(xtickNames, rotation=0, fontsize=8)




def get_column_values( header_str,header,sorted_csv, factor=1):
    energy_col_index = header.index(header_str)
    energy_values =map( lambda x :  float(x[energy_col_index]) / factor , sorted_csv )
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
        values = get_column_values(col_name, header, sorted_csv )    
        n_tests =  get_column_values("test_id", header, sorted_csv  )
        list_all_samples.append((values,n_tests,label))
        
    for l , s , label in list_all_samples:
        #print( str (l) + "-" + str(s) + "-" + str(label))
        line.plot(s,l, label=label)
        plt.legend()
        


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
            else:
                print(colored("ignoring file :%s " % csv_file ,"red"))
        generate_test_behaviour_graphs(csvs_dict)
        generate_box_plots(csvs_dict)
        plt.show()
    else:
        print ("bad arg len")
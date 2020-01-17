#!/usr/bin/env python

from numpy.random import seed
from numpy.random import randn
from scipy.stats import normaltest
import os, sys
import subprocess
import csv
import itertools
from termcolor import colored
from scipy.stats import kruskal

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


def check_data_parametric_normal(data, alpha=0.05):
    stat, p = normaltest(data)
    print('Statistics=%.3f, p=%.3f' % (stat, p))
    if p > alpha:
        print(colored("Sample looks Gaussian (fail to reject H0)","green"))
        return True
    else:
        print(colored("Sample does not look Gaussian (reject H0)'","red"))
        return False


def get_column_values( header_str,header,sorted_csv, factor=1):
    energy_col_index = header.index(header_str)
    energy_values =map( lambda x :  float(x[energy_col_index]) / factor , sorted_csv )
    return energy_values
    


def kruskall_wallis_test(data_list):

    stat, p = kruskal(*data_list)
    print('Statistics=%.3f, p=%.3f' % (stat, p))
    # interpret
    alpha = 0.05
    if p > alpha:
        print('Same distributions (fail to reject H0)')
    else:
        print('Different distributions (reject H0)')




if __name__== "__main__":
    if len(sys.argv) > 1:
        device_folder = sys.argv[1]
        all_csvs_of_folder = fetch_all_data_csvs(device_folder)
        csvs_dict={}
        samples_list=[]
        for csv_file in all_csvs_of_folder:
            header, sortedlist, avg_row = sort_csv_test_id(csv_file)
            energy_values = get_column_values(" energy cons (J)", header, sortedlist )
            if len(energy_values)>min_csv_row_len:
                samples_list.append(energy_values)
                print("->" +csv_file)
                check_data_parametric_normal(energy_values[10:])
            else:
                print(colored("ignoring file :%s " % csv_file ,"red"))
            #if len( sortedlist) >= min_csv_row_len :
            #    csvs_dict[csv_file] = (header, sortedlist, avg_row)
        
        kruskall_wallis_test(samples_list)
        
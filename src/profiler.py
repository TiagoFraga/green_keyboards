#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os
import time
from termcolor import colored

class OperationNotSupported(Exception):
    """docstring for OperationNotSupported"""
    def __init__(self):
        super(OperationNotSupported, self).__init__()
        


class Profiler(object):
    """docstring for Profiler"""
    def __init__(self):
        super(Profiler, self).__init__()
        
    def initProfiler(self,adbcl):
        raise OperationNotSupported("Operation Not supported")

    def loadPreferences(self,adbcl):
        pass


    def startProfiler(self,adbcl):
        pass

    def stopProfiler(self,adbcl):
        pass

    def startProfiling(self,adbcl):
        pass

    def stopProfiling(self,adbcl):
        pass

    def exportResults(self,adbcl):
        pass


class TrepnProfiler(Profiler):
    """docstring for TrepnProfiler"""
    def __init__(self,deviceDir, adbcl):
        super(TrepnProfiler, self).__init__()
        self.deviceDir=deviceDir
        self.adbcl = adbcl

    def initProfiler(self):
        self.adbcl.shell("monkey -p com.quicinc.trepn -c android.intent.category.LAUNCHER 1")
        time.sleep(1)
        self.adbcl.shell("am startservice --user 0 com.quicinc.trepn/.TrepnService")
        time.sleep(2)
        self.adbcl.shell("am start -a android.intent.action.MAIN -c android.intent.category.HOME")
        time.sleep(3)
        self.adbcl.shell("> "+ self.deviceDir +"/TracedMethods.txt")


    def loadPreferences(self, preferences_file_path):
        self.adbcl.shell("am broadcast -a com.quicinc.trepn.load_preferences -e com.quicinc.trepn.load_preferences_file"  + self.deviceDir + "/saved_preferences/" + preferences_file_path)

    def startProfiler(self):
        self.adbcl.shell("am broadcast -a com.quicinc.trepn.start_profiling -e com.quicinc.trepn.database_file \"myfile\" ")
        time.sleep(3)
        self.adbcl.shell("am broadcast -a com.quicinc.Trepn.UpdateAppState -e com.quicinc.Trepn.UpdateAppState.Value 1 -e com.quicinc.Trepn.UpdateAppState.Value.Desc \"started\" ")


    def stopProfiler(self):
        self.adbcl.shell("am broadcast -a com.quicinc.Trepn.UpdateAppState -e com.quicinc.Trepn.UpdateAppState.Value 0 -e com.quicinc.Trepn.UpdateAppState.Value.Desc \"stopped\" ")


    def shutdownProfiler(self):
        time.sleep(1)
        self.adbcl.shell("am broadcast -a com.quicinc.trepn.stop_profiling")
        time.sleep(6)
        print("amandei")
        self.adbcl.shell ("am broadcast -a  com.quicinc.trepn.export_to_csv -e com.quicinc.trepn.export_db_input_file \"myfile\" -e com.quicinc.trepn.export_csv_output_file \"GreendroidResultTrace0\"")
        time.sleep(1)

    def exportResults(self,localDir,script_index,SED_COMMAND,MV_COMMAND,assure=False):
        time.sleep(5)
        n_times = 10
        os.system("adb -s " + self.adbcl.serialno+ " shell ls " + self.deviceDir + "/ | " + SED_COMMAND + " -r 's/[\r]+//g' | egrep -Eio '.*.csv' |  xargs -I{} adb -s " + self.adbcl.serialno +  " pull "+ self.deviceDir + "/{} " + localDir)
        os.system("adb -s " + self.adbcl.serialno+ " shell ls " + self.deviceDir + " | " + SED_COMMAND + " -r 's/[\r]+//g' | egrep -Eio TracedMethods.txt | xargs -I{} adb -s "   + self.adbcl.serialno +   " pull " + self.deviceDir + "/{} " + localDir)
        os.system(MV_COMMAND + " " + localDir + "/TracedMethods.txt " + localDir + "/TracedMethods" + str(script_index) + ".txt")
        os.system(MV_COMMAND + " " + localDir + "/GreendroidResultTrace0.csv " + localDir + "/GreendroidResultTrace" + str(script_index) +".csv")
        pulled_file_path = localDir + "/GreendroidResultTrace" + str(script_index) +".csv"
        has_stopped_tag = os.system( " grep \"stopped\" " + pulled_file_path + " > /dev/null" )
        was_file_pulled_and_contains_stopped = os.path.exists( pulled_file_path ) and str(has_stopped_tag) == "0"
        while not was_file_pulled_and_contains_stopped and assure and n_times>0:
            print(colored("[Profiler] Results file is empty or wasn't exported. Waiting for trepn to export results file","red"))
            time.sleep(5)
            os.system("adb -s " + self.adbcl.serialno+" shell ls " + self.deviceDir + "/ | " + SED_COMMAND + " -r 's/[\r]+//g' | egrep -Eio '.*.csv' |  xargs -I{} adb -s "  + self.adbcl.serialno +  " pull "+ self.deviceDir + "/{} " + localDir)
            os.system(MV_COMMAND + " " + localDir + "/GreendroidResultTrace0.csv " + localDir + "/GreendroidResultTrace" + str(script_index) +".csv")
            pulled_file_path = localDir + "/GreendroidResultTrace" + str(script_index) +".csv"
            has_stopped_tag = os.system( " grep \"stopped\" " + pulled_file_path + " > /dev/null" )
            was_file_pulled_and_contains_stopped = os.path.exists( pulled_file_path ) and str(has_stopped_tag) == "0"
            n_times = n_times -1
        
    
    def activateFlags(self):
        self.adbcl.shell("echo 1 > "+self.deviceDir+"/GDflag")

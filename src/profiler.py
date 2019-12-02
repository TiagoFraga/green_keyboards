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
    def __init__(self,deviceDir):
        super(TrepnProfiler, self).__init__()
        self.deviceDir=deviceDir

    def initProfiler(self,adbcl):
        adbcl.shell("monkey -p com.quicinc.trepn -c android.intent.category.LAUNCHER 1")
        time.sleep(1)
        adbcl.shell("am startservice --user 0 com.quicinc.trepn/.TrepnService")
        time.sleep(2)
        adbcl.shell("am start -a android.intent.action.MAIN -c android.intent.category.HOME")
        time.sleep(3)
        adbcl.shell("> "+ self.deviceDir +"/TracedMethods.txt")


    def loadPreferences(self,adbcl, preferences_file_path):
        adbcl.shell("am broadcast -a com.quicinc.trepn.load_preferences -e com.quicinc.trepn.load_preferences_file"  + self.deviceDir + "/saved_preferences/" + preferences_file_path)

    def startProfiler(self,adbcl):
        adbcl.shell("am broadcast -a com.quicinc.trepn.start_profiling -e com.quicinc.trepn.database_file 'myfile' ")
        time.sleep(3)
        adbcl.shell("am broadcast -a com.quicinc.Trepn.UpdateAppState -e com.quicinc.Trepn.UpdateAppState.Value '1' -e com.quicinc.Trepn.UpdateAppState.Value.Desc 'started' ")


    def stopProfiler(self,adbcl):
        adbcl.shell("am broadcast -a com.quicinc.Trepn.UpdateAppState -e com.quicinc.Trepn.UpdateAppState.Value '0' -e com.quicinc.Trepn.UpdateAppState.Value.Desc 'stopped' ")


    def shutdownProfiler(self,adbcl):
        time.sleep(1)
        adbcl.shell("am broadcast -a com.quicinc.trepn.stop_profiling")
        time.sleep(6)
        adbcl.shell ("am broadcast -a  com.quicinc.trepn.export_to_csv -e com.quicinc.trepn.export_db_input_file 'myfile' -e com.quicinc.trepn.export_csv_output_file 'GreendroidResultTrace0'")
        time.sleep(1)

    def exportResults(self,localDir,script_index,SED_COMMAND,MV_COMMAND,assure=False):
        time.sleep(5)
        os.system("adb shell ls " + self.deviceDir + "/ | " + SED_COMMAND + " -r 's/[\r]+//g' | egrep -Eio '.*.csv' |  xargs -I{} adb pull "+ self.deviceDir + "/{} " + localDir)
        os.system("adb shell ls " + self.deviceDir + " | " + SED_COMMAND + " -r 's/[\r]+//g' | egrep -Eio TracedMethods.txt | xargs -I{} adb pull " + self.deviceDir + "/{} " + localDir)
        os.system(MV_COMMAND + " " + localDir + "/TracedMethods.txt " + localDir + "/TracedMethods" + str(script_index) + ".txt")
        os.system(MV_COMMAND + " " + localDir + "/GreendroidResultTrace0.csv " + localDir + "/GreendroidResultTrace" + str(script_index) +".csv")
        pulled_file_path = localDir + "/GreendroidResultTrace" + str(script_index) +".csv"
        was_file_pulled= os.path.exists( pulled_file_path )
        while not was_file_pulled and assure==True:
            print(colored("[Profiler] Results file not exported. Waiting for trepn to export results file","red"))
            time.sleep(5)
            os.system("adb shell ls " + self.deviceDir + "/ | " + SED_COMMAND + " -r 's/[\r]+//g' | egrep -Eio '.*.csv' |  xargs -I{} adb pull "+ self.deviceDir + "/{} " + localDir)
            os.system(MV_COMMAND + " " + localDir + "/GreendroidResultTrace0.csv " + pulled_file_path)
            was_file_pulled= os.path.exists( pulled_file_path )
    
    def activateFlags(self,adbcl):
        adbcl.shell("echo 1 > "+self.deviceDir+"/GDflag")

#!/usr/bin/env python
# -*- coding: utf-8 -*-

import time

def openApp(adbcl,package):
    adbcl.shell("monkey -p " + package + " -c android.intent.category.LAUNCHER 1")
    time.sleep(5)


def firstWindow_gmail(vc):
    vc.dump(window=-1)
    firstbutton = vc.findViewById("com.google.android.gm:id/compose_button")
    firstbutton.touch()
    time.sleep(5)


def getEditText(vc, edit_text):
    vc.dump(window=-1)
    text = vc.findViewById(edit_text)
    return text

def openKeyboard(edit_text):
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


def writeSuggestedWords(vc,text,words_to_insert,words_length,coords):
    for key,word in words_to_insert.items():
        word_str = word.encode('ascii','replace')
        chars = int(words_length.get(key))
        char_limit = 0
        
        while(char_limit < chars):
            text.type_without_sleep(word_str[char_limit],alreadyTouched=True)
            char_limit = char_limit+1
                
        if(char_limit < len(word_str)):
            reco = coords.get("reco") 
            option = coords.get(reco)
            vc.touch(int(option[0]),int(option[1]))
            char_limit = char_limit+1
        text.type_without_sleep(' ',alreadyTouched=True)
        

def writeChars(text,words):
    for word in words:
        word_str = word.encode('ascii','replace')
        if word_str == '\n':
            text.type_without_sleep('\n',alreadyTouched=True)
        elif word_str == ' ':
            text.type_without_sleep(' ',alreadyTouched=True)
        else:
            for c in word_str:
                text.type_without_sleep(c,alreadyTouched=True)


def getText(vc,edit_text):
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
    time.sleep(1) 
    adbcl.shell("am force-stop "+ package)


def setImmersiveMode(adbcl,package):
    adbcl.shell("settings put global policy_control immersive.full="+ package)
      
def cleaningAppCache(adbcl,package):
    adbcl.shell("pm clear "+ package)


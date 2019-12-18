#!/usr/bin/env python
# -*- coding: utf-8 -*-

import time
import data

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
        print ("key %s , word %s" % (key,word))
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
      
# input_text file is a text file splitted by spaces 
def write_cutted_word_with_suggestion_touch(adbcl, box_text , input_text_file , coords):
    text = data.split_lines( input_text_file)
    suggestion_box = coords.get("reco") 
    suggestion_box_coords = coords.get(suggestion_box)
    for line in text:
        l = line.split(" ")
        word = l[0].encode('ascii','replace')
        n_chars_to_write = l[1].replace("\n","")
        trunc_word=word[:int(n_chars_to_write)]
        
        if int(n_chars_to_write)==0:
           # print("nada")  
            #adbcl.touch(int(suggestion_box_coords[0]),int(suggestion_box_coords[1]))        
            #time.sleep(3)
            #my_touch(adbcl, int(suggestion_box_coords[0]),int(suggestion_box_coords[1]))
            #my_touch(adbcl, 200, 1050)
            my_touch(adbcl, 200, 1050)
            #adbcl.touch(int(suggestion_box_coords[0]),int(suggestion_box_coords[1]))        
    
            #adbcl.touchDip(200,1050)        
            
        else:
            print("word to write ->%s" % trunc_word)
            box_text.type_without_sleep(trunc_word,alreadyTouched=True)
            print("coords: %s, %s" % (suggestion_box_coords[0],suggestion_box_coords[1]))
            #time.sleep(5)
            #adbcl.touchDip(200,1050)        
            my_touch(adbcl, 200, 1050)
           
            #my_touch(adbcl, int(suggestion_box_coords[0]),int(suggestion_box_coords[1]))
            adbcl.touch(int(suggestion_box_coords[0]),int(suggestion_box_coords[1]))        
            


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
     
def my_touch(adbcl,x,y):
   # print ("touching")
    adbcl.shell("input swipe %d %d %d %d 1" % (x,y,x,y))
    #print("touched")       

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


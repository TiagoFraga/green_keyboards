#!/usr/bin/env python
# -*- coding: utf-8 -*-
import io
import json


def getData(input_text):
    text_to_insert = read_file(input_text)
    lines_to_insert = split_lines(input_text)
    words_to_insert = split_words(input_text)
    chars_to_insert = split_chars(input_text)
    words_sugge,words_sugge_length = getSuggestions(input_text)
    return text_to_insert, lines_to_insert,words_to_insert, chars_to_insert, words_sugge, words_sugge_length

def read_file(filename):
    f = open(filename, "r")
    texto = f.read()
    return texto

def split_lines(filename):
   lines = []
   with io.open(filename, "r", encoding='utf-8') as f:
       lines = f.readlines()
   return lines

def split_words(filename):
   words = []
   lines = []
   with io.open(filename, "r", encoding='utf-8') as f:
       for line in f.read().split('\n'):
           lines.append(line)
       
   for line in lines:
        if(line == ''):
            words.append('\n')
        else:
            arr = line.split(' ')
            for w in arr:
                words.append(w)
                words.append(' ')
   return words

def split_chars(filename):
   words = split_words(filename)
   chars = []
   for word in words:
        if word == ' ':
            chars.append(' ')
        elif word == '\n':
            chars.append('\n')
        else:
            for c in word:
                chars.append(c)
   return chars

def getEmail(filename):
    with open(filename) as json_file:
        data_mail = json.load(json_file)
    return data_mail

def getCoords(filename,keyboard_key):
    with open(filename) as json_file:
        dic = json.load(json_file)
        coords = dic.get(keyboard_key)
    return coords

def text_to_lines(text):
   lines = []
   lines = text.split('\n')
   return lines

def text_to_words(text):
   words = []
   lines = text_to_lines(text)
   for line in lines:
        arr = line.split(' ')
        for w in arr:
            words.append(w)
            words.append(' ')
        words.append('\n')
   return words

def text_to_chars(text):
   chars = []
   words = text_to_words(text)
   for word in words:
        if word == ' ':
            chars.append(' ')
        elif word == '\n':
            chars.append('\n')
        else:
            for c in word:
                chars.append(c)
   return chars


def cleanList(a):
    new_a = []
    for word in a:
        if word != ' ' and word != '' and word != '\n':
            new_a.append(word)
    
    return new_a

def getSuggestions(filename):
   lines = []
   words = {}
   words_length = {}
   w = 0
   with io.open(filename, "r", encoding='utf-8') as f:
       lines = f.readlines()
       for line in lines:
           info = line.split(' ')
           words[w] = info[0]
           words_length[w] = info[1].split('\n')[0]
           w = w+1
   return words,words_length


def get_triples_word_trunc_len(filename):
    ret_list = []
    text = split_lines( filename)
    for line in text:
        l = line.split(" ")
        word = l[0].encode('ascii','replace')
        n_chars_to_write = l[1].replace("\n","")
        trunc_word=word[:int(n_chars_to_write)]      
        ret_list.append((word,trunc_word,int(n_chars_to_write)))
    return ret_list

def getCalibration(chars,calib_file,keyboard_name):
    calib = getCoords(calib_file,keyboard_name)
    calib_list = []
    for char in chars:
        char_lower = char.lower()
        if char_lower.isalpha() == True:
            coord = calib.get(char_lower)
            calib_list.append(coord)            
        else:
            if(char_lower == '.'):
               coord = calib.get('.')
               calib_list.append(coord)
            elif(char_lower == ','):
               coord = calib.get(',')
               calib_list.append(coord) 
            elif(char_lower == ' '):
               coord = calib.get('space')
               calib_list.append(coord)
    return calib_list

    








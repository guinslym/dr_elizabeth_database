# -*- coding: utf-8 -*-
import os
from os import listdir
from os.path import isfile, join
import shutil
import json

mypath = os.path.dirname(os.path.realpath(__file__))

def get_all_the_json_files():
    onlyfiles = [f for f in listdir(mypath+"/live_tweets") if isfile(join(mypath+"/live_tweets", f))]
    onlyjson = [f for f in onlyfiles if f.split('.')[1] == 'json']
    onlyjson = [f for f in onlyjson if len(f) < 25]
    return onlyjson

def move_files(onlyjson):
    for fichier in onlyjson:
        shutil.move(mypath+"/live_tweets/"+fichier, mypath+"/targets")

def aggregate():
    onlyfiles = [f for f in listdir(mypath+"/live_tweets") if isfile(join(mypath+"/live_tweets", f))]
    onlyjson = [f for f in onlyfiles if f.split('.')[1] == 'json']
    contenjson = []
    for fichier in onlyjson[0:1000]:
        with open(mypath+"/live_tweets/"+fichier, encoding='utf-8') as data_file:
            contenjson.append( json.loads(data_file.read()) )
    with open('data.json', 'w') as outfile:
        json.dump(contenjson, outfile, sort_keys = True, indent = 4)

"""
with open(fname) as f:
    content = f.readlines()
"""
onlyjson = get_all_the_json_files()
move_files(onlyjson)
print(onlyjson)
aggregate()
print("done")

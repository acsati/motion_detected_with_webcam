# !/usr/bin/env python3
# Author: ALP CANER SATI, May 2021

import os
import datetime
import time
import json

CONFIG_PATH = "/home/pi/Desktop/config.json"

f = open(CONFIG_PATH, "r")
config = json.load(f)
f.close()
path = config["path"]
while True:
    old = ["",datetime.datetime.now()]
    ls = os.listdir(path)
    try:
        ls.remove("lastsnap.jpg")
    except:
        pass
    if (len(ls)>10):
        for i in [[path+j,datetime.datetime.fromtimestamp(os.stat(path+j).st_mtime)] for j in ls]:
            if (i[1] < old[1]):
                old = i
        os.remove(old[0])
    time.sleep(1)
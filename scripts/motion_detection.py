# !/usr/bin/env python3
# Author: ALP CANER SATI, May 2021

from pathlib import Path
import os
from datetime import datetime as dt
import time
import json
from traceback import format_exc
import requests
import pwd


CONFIG_PATH = "/home/pi/Desktop/config.json"
LOG_FOLDER_PATH = "/home/pi/Desktop/camera_logs/"

def create_Log_File(log:list):
    log_file_name = "camera_"+str(dt.now()).split(" ")[0]+".log"
    log_path = LOG_FOLDER_PATH+log_file_name
    if(log_file_name in os.listdir(LOG_FOLDER_PATH)):
        with open(log_path, "a", encoding="utf-8") as f:
            f.write("\n\n"+str(dt.now()).split(" ")[1]+" saatinde loglandi;\n")
            f.writelines([i[0]+","+i[1]+","+i[2]+"\n" for i in log[1:]])
    else:
        with open(log_path, "w", encoding="utf-8") as f:
            f.write("******************** "+str(dt.now()).split(" ")[0]+" Camera Script Logu ********************\n")
            f.write("\n\n"+str(dt.now()).split(" ")[1].split(".")[0]+" saatinde loglandi;\n")
            f.writelines([i[0]+","+i[1]+","+i[2]+"\n" for i in log[1:]])

def send_slack_message(payload, webhook):
    """Send a Slack message to a channel via a webhook. 
    
    Args:
        payload (dict): Dictionary containing Slack message, i.e. {"text": "This is a test"}
        webhook (str): Full Slack webhook URL for your chosen channel. 
    
    Returns:
        HTTP response code, i.e. <Response [503]>
    """
    return requests.post(webhook, json.dumps(payload))

class SlackMessageTemplate:
    motion_detected = """\
    :warning: Hi, motion detected from the camera !!
    - *File name*: `{}`
    - *Motion start*: `{}`
    """
    motion_ended = """\
    :exclamation: This is a recently detected motion from the camera. Please check your _OneDrive/camera_ folder.
    - *File name*: `{}`
    - *Motion end*: `{}` \
    """

def file_check(path_to_watch):
    before = dict ([(f, None) for f in os.listdir (path_to_watch)])
    while 1:
            after = dict ([(f, None) for f in os.listdir (path_to_watch)])
            added = [f for f in after if not f in before]
            if added:
                    return added
            else:
                before = after

if __name__=="__main__":
    log = [["Date","User","Message"]]
    try:
        f = open(CONFIG_PATH, "r")
        config = json.load(f)
        f.close()
        while True:
            ls1 = os.listdir(config["path"])
            log = [["Date","User","Message"]]
            added_file_names = file_check(config["path"])
            for i in added_file_names:
                if not i.endswith("lastsnap.jpg"):
                    path = config["path"]+i
                    rs = send_slack_message({"text":SlackMessageTemplate.motion_detected.format(i,dt.now())},config["slack_webhook"])
                    if rs.status_code != 200:
                        log.append([str(dt.now()),pwd.getpwuid(os.geteuid())[0],"Motion detected but Slack message could not be sent.. File Name: {}".format(i)])
                        create_Log_File(log)
                    while (not "mlp_actions: End of event" in os.popen("tail -1 {}".format(config["log_path"])).read()):
                        time.sleep(0.2)
                    send_slack_message({"text":SlackMessageTemplate.motion_ended.format(i,dt.now())},config["slack_webhook"])
            time.sleep(2)
            added_file_names = None
    except:
        log.append([str(dt.now()),pwd.getpwuid(os.geteuid())[0],format_exc()])
        create_Log_File(log)


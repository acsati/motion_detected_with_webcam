#!/bin/bash

CAMERA_FOLDER="/home/pi/Desktop/camera"
COULD_TAG="OneDrive"
CLOUD_FOLDER="camera"

inotifywait -m $CAMERA_FOLDER -e create -e moved_to |
    while read dir action file; do
        echo "The file '$file' appeared in directory '$dir' via '$action'"
	sleep 10
        rclone sync $CAMERA_FOLDER $CLOUD_TAG:$CLOUD_FOLDER
	sleep 10
    done

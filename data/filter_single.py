import numpy as np
import re
import os
import sys
import subprocess

#get video length
def getLength(filename):
    result = subprocess.Popen(["ffprobe", filename], universal_newlines=True, 
        stdout = subprocess.PIPE, stderr = subprocess.STDOUT)
    temp = result.stdout.readlines()
    line = [x for x in temp if "Duration" in x][0]
    words = re.split(r'[ ,\n]', line)
    duration = words[3]
    splits = re.split(r'[ :,.\n]', duration)
    hours = int(splits[0])
    mins = int(splits[1])
    secs = int(splits[2])
    tenths = int(splits[3])
    tot = ((((hours * 60 + mins) * 60) + secs) * 1000) + tenths * 10
    return tot

#input from the cmd line script
result_path = sys.argv[-1]
reject_path = sys.argv[-2]
vid_path = sys.argv[-3]

list_dir = os.listdir(vid_path)
count = 0
lengths = []
for vid in list_dir:
    if vid.endswith(".mp4"):
        count += 1
        full_vid_path = vid_path + "/" + vid
        lengths.append(getLength(full_vid_path))

move = False
result_files = os.listdir(result_path)

for result_file in result_files:
    #filter a single result
    result = result_path + "/" + result_file
    with open(result, "r") as fp:
        lines = fp.readlines()
        move = False

        video_times = list(map(int,lines[2].strip().split(','))) #read times spent on each video  
        rating_times = list(map(int,lines[3].strip().split(','))) #read times spent on each rating  
        video_order = list(map(int,lines[1].strip().split(','))) #read the video order seen by the surveyee
        scores = list(map(int,lines[0].strip().split(','))) #read scores
    
        #print(video_times,rating_times,video_order,scores)

        #TODO: insert filtering logic and set move accordingly

        if move:
            os.system("mv {} ../rejected_results".format(result))

import numpy as np
import re
import os
import sys
import subprocess


#Sample filter function
def filter_single_video(lengths, video_times, rating_times, video_order, scores):
    #First check if user watching alines with video length
    #0.5 sec tolerance for black screen at the end
    for i in range(len(lengths)):
        if (lengths[i] - 0.5> video_times[i]):
            return True

    #Suppose left video is always better 
    #check if user indeed rates it higher than the right 
    for i in range(len(lengths)):
    	if (scores[i][0] < scores[i][1]):
    		return True

    return False #We don't move this user to rejected folder

#Parse data from user result file 
def parse_results(lines):
    video_times = list(map(int,lines[2].strip().split(','))) #read times spent on each video  
    rating_times = list(map(int,lines[3].strip().split(','))) #read times spent on each rating  
    video_order = list(map(int,lines[1].strip().split(','))) #read the video order seen by the surveyee
		
		#read scores
    temp_scores = lines[0].strip().split(',')
    scores = []
    for i in range(len(temp_scores)):
    	scores.append(list(map(int,temp_scores[0].split(" "))))

    return video_times, rating_times, video_order, scores

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
result_path, reject_path, vid_path = sys.argv[-1], sys.argv[-2], sys.argv[-3]

list_dir = os.listdir(vid_path)
lengths = [] #actual video lengths
for vid in list_dir:
    if vid.endswith(".mp4"):
        full_vid_path = vid_path + "/" + vid
        lengths.append([vid, getLength(full_vid_path)]) 

#put the lengths into pairs
temp_lengths = []

lengths = list(sorted(lambda x: x[0], lengths))

for i in range(len(lengths)//2):
	temp_lengths.append([lengths[i*2][1],lengths[i*2+1][1]])
lengths = temp_lengths

move = False
result_files = os.listdir(result_path)


for result_file in result_files:
    print(result_file)
    #filter a single result
    result = result_path + "/" + result_file
    with open(result, "r") as fp:
        lines = fp.readlines()
        move = False

        #insert customized filter here 
        move = filter_single_video(lengths,*parse_results(lines))
        if move:
            os.system("mv {} ../rejected_results".format(result))

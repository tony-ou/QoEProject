import numpy as np
import re
import os
import sys
import subprocess

# Require a name to name plots and log
args = len(sys.argv) - 2 if sys.argv[0] == "python" else len(sys.argv) - 1


def getLength(filename):
    result = subprocess.Popen(["ffprobe", filename], stdout = subprocess.PIPE, stderr = subprocess.STDOUT)
    line = [x for x in result.stdout.readlines() if "Duration" in x][0]
    words = re.split(r'[ ,\n]', line)
    duration = words[3]
    splits = re.split(r'[ :,.\n]', duration)
    hours = int(splits[0])
    mins = int(splits[1])
    secs = int(splits[2])
    tenths = int(splits[3])
    tot = ((((hours * 60 + mins) * 60) + secs) * 1000) + tenths * 10
    return tot

inp = sys.argv[-3]
tolerate = int(sys.argv[-4])
high = int(sys.argv[-2])
low = int(sys.argv[-1])
result_path = inp

vid_path = "../videos/buffer_location3"
list_dir = os.listdir(vid_path)
count = 0
lengths = []
for vid in list_dir:
    if vid.endswith(".mp4"):
        count += 1
        full_vid_path = vid_path + "/" + vid
        lengths.append(getLength(full_vid_path))

def print_no_n(line):
    if line[-1] == '\n':
        print(line[:-1])
    else:
        print(line)

move = False
with open(result_path, "r") as fp:
    lines = fp.readlines()
    
    # check times
    times = re.split(r'[,\n]', lines[2])[:-1]
    nums_arr = np.zeros(count, dtype=int)
    for i in range(count):
        if times[i] != '':
            nums_arr[i] = int(times[i])
    
    for i in range(count):
        if lengths[i] >= nums_arr[i] + tolerate*1000:
            move = True 

    #check low/high score
    scores = re.split(r'[,\n]', lines[0])[:-1]
    scores = list(map(int, scores))
    if high != -1:
        if max(scores) != scores[high-1]:
            move = True
    if low != -1:
        if min(scores) != scores[low-1]:
            move = True
    if move:
        os.system("mv {} ../rejected_results".format(result_path))


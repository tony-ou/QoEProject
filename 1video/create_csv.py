import os, subprocess, re
from os import listdir
from os.path import isfile, join
from collections import namedtuple
import csv

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
vid_path = './videos/original_videos_Sports_720P_Sports_720P-07d0'
list_dir = os.listdir(vid_path)
lengths = [] #actual video lengths
for vid in list_dir:
    if vid.endswith(".mp4"):
        full_vid_path = vid_path + "/" + vid
        lengths.append(str(getLength(full_vid_path)))


files = ['./results/' + f for f in listdir('./results') if f.split('.')[-1]=='txt']
data = []
data.append(['5,5,-1,0,0,5','n',','.join(lengths)])
fields = ['score', 'video order', 'view time', 'grade time', 'ID', 'device',
        'age', 'env', 'reason']
for file in files: 
    temp = [line.rstrip('\n') for line in open(file)]
    data.append(temp)
with open("./sum.csv", "w", newline="") as f:
    writer = csv.writer(f)
    writer.writerows(data)


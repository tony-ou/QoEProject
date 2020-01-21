import csv
import os
from collections import * 
print("Please make sure you have run filter script")
file = input('Enter path to Mturk csv')
comment = input("Enter a reject comment")
rejected_results = list(map(lambda x: x.split('.')[0], os.listdir('../rejected_results')))
approved_results = list(map(lambda x: x.split('.')[0], os.listdir('../results')))

buffer = []
def parse(line):
    line = line.strip().split("\",\"")
    line[0]= line[0][1:] #get rid of first "
    line[-1]= line[-1][:-1] # ... last "
    return line
def cat(line):
    line = "\"" + "\",\"".join(line) + "\"\n"
    return line

with open(file) as csv_file:    
    buffer = csv_file.readlines()
    buffer = list(map(parse, buffer))
    header = buffer[0]
    
    reject = header.index('Reject')
    approve = header.index('Approve') 
    w_id = header.index('WorkerId')
    cmt = header.index('RequesterFeedback')
    
    buffer[0] = cat(header)
    
    for i in range(1,len(buffer)): 
        row = buffer[i]
        while (len(row) <= 30): 
            row.append('')
        if row[w_id] in rejected_results:
            row[reject]='x'
            row[cmt] = comment
        if row[w_id] in approved_results:
            row[approve]='x'
        buffer[i]= cat(row)


with open(file, 'w',newline='') as csv_file:
    csv_file.writelines(buffer)
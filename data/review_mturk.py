import csv
import os
from collections import * 
print("Please make sure you have run filter script")
file = input('Enter path to Mturk csv')
comment = input("Enter a reject comment")
rejected_results = list(map(lambda x: x.split('.')[0], os.listdir('../rejected_results')))
approved_results = list(map(lambda x: x.split('.')[0], os.listdir('../results')))

buffer = []
with open(file) as csv_file:    
    csv_reader = csv.reader(csv_file, delimiter=',')
    header = next(csv_reader,None)
    reject = header.index('Reject')
    approve = header.index('Approve') 
    w_id = header.index('WorkerId')
    cmt = header.index('RequesterFeedback')
    
    buffer.append(header)
    for row in csv_reader: 
        while (len(row) <= 30): 
            row += ['']
        if row[w_id] in rejected_results:
            row[reject]='x'
            row[cmt] = comment
        if row[w_id] in approved_results:
            row[approve]='x'
        buffer.append(row)

with open(file, 'w',newline='') as csv_file:
    csv_writer = csv.writer(csv_file, delimiter=',')
    for row in buffer: 
        csv_writer.writerow(row)
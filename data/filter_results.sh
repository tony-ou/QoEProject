#!/bin/bash
# A script to check whether to accept or reject results
read -p "Enter the path to videos relative to this script?" path
rejected="../rejected_results"
results="../results"
python3 ../data/filter_single.py $path $rejected $results

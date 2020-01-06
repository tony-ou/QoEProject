#!/bin/bash
# A script to check whether to accept or reject results


# check each result and manually decide to keep or not
for result in ../results/*.txt; do
    read -p "Time length of black screen at the end of video (tolerate if user skips that part)" tolerate
    read -p "Enter video number for highest quality video (-1 if no such video) " high
    read -p "Enter video number for lowest quality video. (-1 if no such video) " low
    python ../data/filter_single.py $tolerate $result $high $low

done

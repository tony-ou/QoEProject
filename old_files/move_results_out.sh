#!/bin/bash
# A script to move results out of the results directory

ls videos

echo "Please enter the video set currently in results"
read RES_NAME

if ! [[ -d "videos/$RES_NAME" ]]; then
    echo "Video directory does not exist."
    exit 1
fi

old_result=old_results/$RES_NAME

if ! [[ -d "$old_result" ]]; then
    mkdir $old_result
    echo "$old_result directory created successfully"
fi

old_rej=$old_result/rejected_results

if ! [[ -d "$old_rej" ]]; then
    mkdir $old_rej
    echo "$old_rej directory created successfully"
fi

mv results/*.txt $old_result
echo "moved results into $old_result"

mv rejected_results/*.txt $old_rej
echo "moved rejected results into $old_rej"


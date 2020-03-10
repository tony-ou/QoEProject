#!/bin/bash
# A script to move results out of the results directory

ls old_results

echo "Please enter which old results to move into results"
read RES_NAME

old_result=old_results/$RES_NAME

if ! [[ -d "$old_result" ]]; then
    echo "$old_result does not exist"
    exit 1
fi
old_accept=$old_result/results
old_rej=$old_result/rejected_results

if ! [[ -d "$old_rej" ]]; then
    mkdir $old_rej
    echo "$old_rej directory created successfully"
fi

mv $old_accept/*.txt results/
echo "moved results from $old_accept into results"

mv $old_rej/*.txt rejected_results/
echo "moved rejected results from $old_rej"


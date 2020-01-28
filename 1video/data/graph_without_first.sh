#!/bin/bash
# A script to read results and return plots based on video order

ls ../videos

echo "Please enter a name to name the result plots and log:"
read RES_NAME

if ! [[ -d "../videos/$RES_NAME" ]]; then
    echo "Video directory does not exist."
    exit 1
fi

fig_folder=../fig/$RES_NAME
subfolder=$fig_folder/without_first
log_file=${RES_NAME}_without_first.log
png_file=${RES_NAME}_without_first_plot.png

if ! [[ -d "$fig_folder" ]]; then
    mkdir $fig_folder
    echo "$fig_folder directory created successfully"
fi

if ! [[ -d "$subfolder" ]]; then
    mkdir $subfolder
    echo "$subfolder directory created successfully"
fi

python plot_wo_first.py $RES_NAME

if [[ -f "$png_file" ]]; then
    mv $png_file $subfolder
    echo "$subfolder/$png_file created successfully"
fi

if [[ -f "$log_file" ]]; then
    mv $log_file $subfolder
    echo "$subfolder/$log_file created successfully"
fi


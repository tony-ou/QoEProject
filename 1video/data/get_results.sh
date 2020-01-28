#!/bin/bash
# A script to read results and return plots and a log

ls ../videos

echo "Please enter a name to name the result plots and log:"
read RES_NAME

if ! [[ -d "../videos/$RES_NAME" ]]; then
    echo "Video directory does not exist."
    exit 1
fi

fig_folder=../fig/$RES_NAME

if ! [[ -d "$fig_folder" ]]; then
    mkdir fig_folder
    echo "$fig_folder directory created successfully"
fi

PLOT_1=${RES_NAME}_plot.png
PLOT_2=${RES_NAME}_standardized_plot.png
LOG_1=${RES_NAME}_results.log

FILE_CHECK1=$fig_folder/$PLOT_1
FILE_CHECK2=$fig_folder/$PLOT_2
FILE_CHECK3=../logs/$LOG_1

FILE_1=$PLOT_1
FILE_2=$PLOT_2
FILE_3=$LOG_1

EXISTS=0

if [[ -f "$FILE_CHECK1" ]]; then
    echo "$FILE_CHECK1 already exists."
    EXISTS=1
fi
if [[ -f "$FILE_CHECK2" ]]; then
    echo "$FILE_CHECK2 already exists."
    EXISTS=1
fi
if [[ -f "$FILE_CHECK3" ]]; then
    echo "$FILE_CHECK3 already exists."
    EXISTS=1
fi

if [[ $EXISTS == 0 ]]; then
    python plot_results.py $RES_NAME
    if [[ -f "$FILE_1" ]]; then
        mv $FILE_1 ../fig/
        echo "$FILE_CHECK1 created successfully"
    else
        echo "Failed to create $PLOT_1"
    fi
    if [[ -f "$FILE_2" ]]; then
        mv $FILE_2 ../fig/
        echo "$FILE_CHECK2 created successfully"
    else
        echo "Failed to create $PLOT_2"
    fi
    if [[ -f "$FILE_3" ]]; then
        mv $FILE_3 ../logs/
        echo "$FILE_CHECK3 created successfully"
    else
        echo "Failed to create $LOG_1"
    fi
else
    echo "Please remove any conflicting files or try a different name."
fi


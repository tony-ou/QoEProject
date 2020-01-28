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
order_folder=$fig_folder/order_plots
log_file=${RES_NAME}_order_plots.log

if ! [[ -d "$fig_folder" ]]; then
    mkdir $fig_folder
    echo "$fig_folder directory created successfully"
fi

if ! [[ -d "$order_folder" ]]; then
    mkdir $order_folder
    echo "$order_folder directory created successfully"
fi

python plot_result_order.py $RES_NAME

for result in ./${RES_NAME}_order_plot*.png; do
    mv $result $order_folder
    echo "$order_folder/$result created successfully"
done

if [[ -f "$log_file" ]]; then
    mv $log_file $order_folder
    echo "$order_folder/$log_file created successfully"
fi


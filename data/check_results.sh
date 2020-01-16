#!/bin/bash
# A script to check whether to accept or reject results

# function to check user input
get_inp() {
    read -p "Would you like to keep this result? [y/n]: " inp
    case "$inp" in
        Y|y)
            keep=true
            return 0
            ;;
        N|n)
            keep=false
            return 0
            ;;
        *)
            printf %s\\n "Please enter y or n"
            return 1
            ;;
    esac
}

# check each result and manually decide to keep or not
for result in ../results/*.txt; do
    python ../data/read_single.py $result
    until get_inp; do : ; done
    if [[ "$keep" = false ]] ; then
        mv $result ../rejected_results
    fi
done
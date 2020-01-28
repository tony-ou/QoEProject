import os
import sys
import numpy as np
import matplotlib
matplotlib.use('agg')
import matplotlib.pyplot as plt
from scipy.stats import t
import read_results as rr

# Require a name to name plots and log
args = len(sys.argv) - 2 if sys.argv[0] == "python" else len(sys.argv) - 1

if args != 1:
    print("please enter one argument as the name of a video set")
    exit(0)

inp = sys.argv[-1]

log_name = inp + "_order_plots.log"
header = "LOG OF " + inp + " ORDER PLOT STATISTICS\n\n"

# Count the total number of videos
vid_path = "../videos/" + inp
list_dir = os.listdir(vid_path)
count = 0
for file in list_dir:
    if file.endswith(".mp4"):
        count += 1

def single_order_plot(num_graph):

    # Check for correct inputs
    if (num_graph < 0) or (num_graph > count):
        print("Invalid video number")
        exit(0)

    elif num_graph == 0:
        plot_name = inp + "_order_plot_overall.png"

    else:
        plot_name = inp + "_order_plot_video_" + str(num_graph) + ".png"

    # Reading the results
    res_path = "../results"
    rej_path = "../rejected_results"
    res = rr.get_results(res_path, inp)
    rej_res = rr.get_results(rej_path, inp)

    # Make empty list of lists
    list_stack = []
    for i in range(count):
        tmp_list = []
        list_stack.append(tmp_list)

    # function to sort results into corresponding lists
    def sort_results(res, grade_order_list):
        for user in res:
            pair = []
            pair.append(user[0])
            pair.append(user[1])
            grade_order_list.append(pair)

    grade_order_list = []
    rej_grade_order_list = []

    sort_results(res, grade_order_list)
    sort_results(rej_res, rej_grade_order_list)

    # Plot overall
    if num_graph == 0:
        for pair in grade_order_list:
            i = 0
            for order in pair[1]:
                grade = pair[0][order - 1]
                list_stack[i].append(grade)
                i += 1
                
    #Plot given a certain video
    else:
        for pair in grade_order_list:
            i = 0
            for order in pair[1]:
                if num_graph == order:
                    grade = pair[0][num_graph - 1]
                    list_stack[i].append(grade)
                    break
                i += 1

    means = []
    std_errs = []
    for grades in list_stack:
        mean = np.mean(grades)
        means.append(mean)
        std = np.std(grades)
        se = std / np.sqrt(len(grades))
        std_errs.append(se)

    # x axis configuration
    x = range(1, count + 1)
    x_label = "Video Order"

    # Plot Graph
    plt.figure()
    plt.style.use('ggplot')
    plt.xlabel(x_label)
    plt.ylabel('grade')
    plt.plot(x, means, "blue")
    plt.errorbar(x, means, yerr=std_errs, fmt="-o", ecolor="red", alpha=0.5)
    plt.legend(['mean','Standard Error'],
                loc='upper right',
                numpoints=1,
                fancybox=True)
    plt.savefig(plot_name)

    return [means, std_errs]


# Will Run on all Videos
tot_stats = []

for i in range(count + 1):
    ret_pair = single_order_plot(i)
    tot_stats.append(ret_pair)

# Write log
log = open(log_name, "w+")
log.write(header)

log.write("#################\n")
log.write("#PLOT STATISTICS#\n")
log.write("#################\n\n")

i = 0
for pair in tot_stats:
    if i == 0:
        log.write("STATISTICS FOR ORDER ON ALL VIDEOS\n\n")
    else:
        log.write("STATISTICS FOR ORDER ON VIDEO " + str(i) + "\n\n")
    log.write("MEANS:\n")
    means_str = [str("%.3f" % x) for x in pair[0]]
    log.write(' '.join(means_str))
    log.write("\n")
    log.write("STANDARD ERRORS:\n")
    se_str = [str("%.3f" % x) for x in pair[1]]
    log.write(' '.join(se_str))
    log.write("\n\n")
    i += 1

log.close()


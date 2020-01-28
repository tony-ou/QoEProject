import os
import sys
import numpy as np
import math
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

log_name = inp + "_by_before.log"
header = "LOG OF " + inp + " BY BEFORE STATISTICS\n\n"

# Count the total number of videos
vid_path = "../videos/" + inp
list_dir = os.listdir(vid_path)
count = 0
for file in list_dir:
    if file.endswith(".mp4"):
        count += 1

mid = int(math.ceil(count / 2))

def plot_by_before():

    plot_name = inp + "_by_before_plot.png"

    # Reading the results
    res_path = "../old_results/" + inp
    rej_path = res_path + "/rejected_results"
    res = rr.get_results(res_path, inp)
    rej_res = rr.get_results(rej_path, inp)

    # Make empty list of lists
    list_stack = [[], []]

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

    # Get grades based on if first video is unbuffered and grade given
    for pair in grade_order_list:
        for i in range(count):
            if i != 0 and pair[1][i] == mid: # find middle video and check not first
                before = pair[1][i - 1]
                grade = pair[0][mid - 1]
                if before < mid:
                    list_stack[0].append(grade)
                elif before > mid:
                    list_stack[1].append(grade)

    means = []
    std_errs = []

    for grades in list_stack:
        mean = np.mean(grades)
        means.append(mean)
        std = np.std(grades)
        se = std / np.sqrt(len(grades))
        std_errs.append(se)

    # x axis configuration
    x = ["better video", "worse video"]
    x_label = "Preceding Video Quality"

    # Plot Graph
    plt.figure()
    plt.style.use('ggplot')
    plt.xlabel(x_label)
    plt.ylabel('grade')

    plt.plot(x, means, "blue")
    plt.errorbar(x, means, yerr=std_errs, fmt="-o", ecolor="red", alpha=0.5)
    plt.legend(loc='upper right', numpoints=1, fancybox=True)
    plt.savefig(plot_name)

    return [means, std_errs, list_stack]


# Run Without First Function
ret = plot_by_before()

# Write log
log = open(log_name, "w+")
log.write(header)

log.write("#################\n")
log.write("#PLOT STATISTICS#\n")
log.write("#################\n\n")

log.write("RAW SCORES:\n\n")

log.write("BEFORE VIDEO IS WORSE:\n")
grade_str = [str(x) for x in ret[2][0]]
log.write(' '.join(grade_str))
log.write("\n\n")

log.write("BEFORE VIDEO IS BETTER:\n")
grade_str = [str(x) for x in ret[2][1]]
log.write(' '.join(grade_str))
log.write("\n\n")

log.write("COUNTS:\n")
count_str = [str(len(x)) for x in ret[2]]
log.write(' '.join(count_str))
log.write("\n\n")

log.write("MEANS:\n")
means_str = [str("%.3f" % x) for x in ret[0]]
log.write(' '.join(means_str))
log.write("\n\n")

log.write("STANDARD ERRORS:\n")
se_str = [str("%.3f" % x) for x in ret[1]]
log.write(' '.join(se_str))
log.write("\n")

log.close()


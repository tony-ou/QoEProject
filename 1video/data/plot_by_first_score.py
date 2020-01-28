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

log_name = inp + "_by_first_score.log"
header = "LOG OF " + inp + " BY FIRST SCORE STATISTICS\n\n"

# Count the total number of videos
vid_path = "../videos/" + inp
list_dir = os.listdir(vid_path)
count = 0
for file in list_dir:
    if file.endswith(".mp4"):
        count += 1

def plot_by_first_score():

    plot_name = inp + "_by_first_score_plot.png"

    # Reading the results
    res_path = "../old_results/" + inp
    rej_path = res_path + "/rejected_results"
    res = rr.get_results(res_path, inp)
    rej_res = rr.get_results(rej_path, inp)

    # Make empty list of lists
    list_stack = []
    for i in range(2):
        tmp_list = []
        for j in range(count - 1):
            tmp2_list = []
            tmp_list.append(tmp2_list)
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

    # Get grades based on if first video is unbuffered and grade given
    for pair in grade_order_list:
        if pair[1][0] == 1: # check if first video is unbuffered
            grade = pair[0][0]
            if grade == 1 or grade == 2 or grade == 3: # low grade
                for i in range(count - 1):
                    const_vid_grade = pair[0][i + 1]
                    list_stack[0][i].append(const_vid_grade)
            else:
                for i in range(count - 1):
                    const_vid_grade = pair[0][i + 1]
                    list_stack[1][i].append(const_vid_grade)

    means = []
    std_errs = []
    for i in range(count - 1):
        means.append([0, 0])
        std_errs.append([0, 0])

    for i in range(count - 1):
        for j in range(2):
            mean = np.mean(list_stack[j][i])
            means[i][j] = mean
            std = np.std(list_stack[j][i])
            se = std / np.sqrt(len(list_stack[j][i]))
            std_errs[i][j] = se

    # x axis configuration
    x = ["low (1-3)", "high (4-5)"]
    x_label = "Unbuffered Video Score"

    # Plot Graph
    plt.figure()
    plt.style.use('ggplot')
    plt.xlabel(x_label)
    plt.ylabel('grade')
    for i in range(count - 1):
        plt.plot(x, means[i], label=str(i + 2))
#        plt.errorbar(x, means[i], yerr=std_errs[i], fmt="-o", ecolor="red", alpha=0.5)
    plt.legend(title="Constant Video", loc='upper right', numpoints=1, fancybox=True)
    plt.savefig(plot_name)

    return [means, std_errs, list_stack]


# Run Without First Function
ret = plot_by_first_score()


# Write log
log = open(log_name, "w+")
log.write(header)

log.write("#################\n")
log.write("#PLOT STATISTICS#\n")
log.write("#################\n\n")

log.write("RAW SCORES:\n\n")

log.write("FIRST SCORE LOW:\n")
for vid in ret[2][0]:
    grade_str = [str(x) for x in vid]
    log.write(' '.join(grade_str))
    log.write("\n")

log.write("FIRST SCORE HIGH:\n")
for vid in ret[2][1]:
    grade_str = [str(x) for x in vid]
    log.write(' '.join(grade_str))
    log.write("\n")

log.write("COUNTS:\n")
count_str = [str(len(x[0])) for x in ret[2]]
log.write(' '.join(count_str))
log.write("\n\n")

log.write("MEANS:\n")
for pair in ret[0]:
    means_str = [str("%.3f" % x) for x in pair]
    log.write(' '.join(means_str))
    log.write("\n")
log.write("\n")

log.write("STANDARD ERRORS:\n")
for pair in ret[1]:
    se_str = [str("%.3f" % x) for x in pair]
    log.write(' '.join(se_str))
    log.write("\n")
log.write("\n")

log.close()


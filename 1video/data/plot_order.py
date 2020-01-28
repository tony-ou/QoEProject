import numpy as np
import matplotlib.pyplot as plt
from scipy.stats import t


data002 = np.load("002.npy")
data003 = np.load("003.npy")
data004 = np.load("004.npy")

order002 = np.load("order002.npy")
order003 = np.load("order003.npy")
order004 = np.load("order004.npy")

data = np.row_stack((data002, data003, data004))
order = np.row_stack((order002, order003, order004))

n = np.shape(data)[0]

ordered_results_list =[]
for i in range(n):
    temp = []
    for j in range(13):
        temp.append(data[i][order[i][j] - 1])
    print temp
    ordered_results_list.append(temp)
ordered_result = np.array(ordered_results_list)
print np.shape(ordered_result)

y_mean = np.mean(ordered_result, axis=0)

y_std = np.std(ordered_result, axis=0)

y_se = y_std / np.sqrt(n)

x_list =[1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13]
x = np.array(x_list)

plt.figure()
plt.style.use('ggplot')
plt.xlabel('order')
plt.ylabel('grade')
plt.plot(x, y_mean,"blue")
plt.errorbar(x, y_mean, yerr=y_se, fmt="-o",ecolor='red', alpha=.5)
plt.legend(['mean','Standard Error'],
           loc='upper right',
           numpoints=1,
           fancybox=True)
plt.show()
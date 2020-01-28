import numpy as np
import matplotlib.pyplot as plt
from scipy.stats import t


data001 = np.load("001.npy")
data002 = np.load("002.npy")
data003 = np.load("003.npy")
data004 = np.load("004.npy")

# print data004

combine = np.row_stack((data001, data002, data003, data004))

# combine = np.load("google.npy")
# print combine
n = np.shape(combine)[0]
print np.shape(combine)

y_mean = np.mean(combine, axis=0)
print y_mean
# standard deviation
y_std = np.std(combine, axis=0)

# standard error
y_se = y_std / np.sqrt(np.shape(combine)[0])
print y_se
# 95% confidence interval
'''
dof = np.shape(combine)[0] - 1
alpha = 1.0 - 0.95
conf_interval = t.ppf(1-alpha/2., dof) * y_std * np.sqrt(1.+1./n)
'''


x_list_amazon = [
0.94,
1.36,
2.18,
3.36,
4.08,
4.26,
5.16,
6.4,
8,
9.96,
12.86,
20.52,
30.52
]

x_list_google =[0.24,
0.72,
1.52,
2.8,
3.84,
4.32,
6.32,
8.26,
10.48,
12.84,
15.88,
20.12,
24.04
]

x_list_youtube =[0.28,
1.16,
1.56,
2.12,
3.52,
4.16,
4.88,
6.92,
7.4,
8.28,
13,
20.64,
28.8
]

x_list_cnn = [0.52,
1.4,
1.66,
2.48,
3.76,
4.84,
5.36,
7.5,
9.2,
13.92,
17.64,
21.16,
35.72
]

x = np.array(x_list_amazon)

x = np.delete(x, 4)
y_mean = np.delete(y_mean, 4)
y_se = np.delete(y_se, 4)

plt.figure()
plt.style.use('ggplot')
plt.xlabel('latency/second(s)')
plt.ylabel('grade')
plt.plot(x, y_mean,"blue")
plt.errorbar(x, y_mean, yerr=y_se, fmt="-o",ecolor='red', alpha=.5)
plt.legend(['mean','Standard Error'],
           loc='upper right',
           numpoints=1,
           fancybox=True)
plt.show()

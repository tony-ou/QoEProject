import numpy as np
import matplotlib.pyplot as plt

x_list_ms =[0.56,
1.12,
1.72,
2.22,
3.48,
4.32,
5.04,
6.72,
8.04,
10.64,
12.72,
16.56,
20.52,
25.46
]

google = np.load('ms.npy')
print "google shape: ", google.shape

y_mean = np.mean(google, axis=0)
y_err = np.std(google, axis=0) / np.sqrt(50)

x = np.array(x_list_ms)

plt.figure()
plt.style.use('ggplot')
plt.xlabel('latency/second(s)')
plt.ylabel('grade')
plt.plot(x, y_mean,"blue")
plt.errorbar(x, y_mean, yerr=y_err, fmt="-o",ecolor='red', alpha=.5)
plt.legend(['mean','Standard Error'],
           loc='upper right',
           numpoints=1,
           fancybox=True)
plt.show()

import numpy as np
import matplotlib.pyplot as plt

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

google_old = np.load("google.npy")
google_new = np.load("google_new.npy")

fast = google_new[:,0]
fast_mean = np.mean(fast, axis=0)
fast_error = np.std(fast, axis=0) / np.sqrt(30)

google_new_delete = np.delete(google_new, 0, axis=1)

combine = np.row_stack((google_old, google_new_delete))
print "combine shape: ", np.shape(combine)

combine_mean = np.mean(combine, axis=0)
combine_error = np.std(combine, axis=0) / np.sqrt(50)

y_mean = np.insert(combine_mean, 0, values=fast_mean)

y_err = np.insert(combine_error, 0, values=fast_error)

x = np.array(x_list_google)

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



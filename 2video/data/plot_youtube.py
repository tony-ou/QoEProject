import numpy as np
import matplotlib.pyplot as plt

y_mean_old =[4.66666667, 
4.6,
4.43333333,
3.66666667,
3.26666667,
3,
2.46666667,
2.26666667,
2.06666667,
1.8,
1.5,
1.33333333]

y_mean_old_array = np.array(y_mean_old)

youtube_new = np.load("youtube_new.npy")

youtube_new_delete = np.delete(youtube_new, 0, axis=1)

youtube_new_sum = np.sum(youtube_new_delete, axis=0)

# print "youtube new sum: ", youtube_new_sum

total_sum = youtube_new_sum + y_mean_old_array * 30

# print total_sum

y_mean_delete = total_sum / 50

# print y_mean_delete

y_mean = np.insert(y_mean_delete, 0, values=np.mean(youtube_new[:,0]))

y_se = np.std(youtube_new, axis=0) / np.sqrt(50)


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

x = np.array(x_list_youtube)

x = np.delete(x, 8)
y_mean = np.delete(y_mean, 8)
y_se = np.delete(y_se, 8)


plt.figure(1)
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

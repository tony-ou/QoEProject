import numpy as np
import matplotlib.pyplot as plt


x_list_cnn = [0.52,
1.4,
1.76,
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

cnn_new = np.load("cnn_new.npy")
cnn_old = np.load("cnn.npy")

inserted = cnn_old[:,2]
inserted_mean = np.mean(inserted, axis=0)
inserted_error = np.std(inserted, axis=0) / np.sqrt(30)
print inserted_mean

fast = cnn_new[:,0]
fast_mean = np.mean(fast, axis=0)
fast_error = np.std(fast, axis=0) / np.sqrt(30)

cnn_old_delete = np.delete(cnn_old, 2, axis=1)
print np.shape(cnn_old_delete)

cnn_new_delete = np.delete(cnn_new, 0, axis=1)

combine = np.row_stack((cnn_new_delete, cnn_old_delete))
print "combine shape: ", np.shape(combine)

combine_mean = np.mean(combine, axis=0)
combine_error = np.std(combine, axis=0) / np.sqrt(50)

y_mean = np.insert(combine_mean, 0, values=fast_mean)
y_mean = np.insert(y_mean, 3, values=inserted_mean)

print y_mean, np.shape(y_mean)

y_err = np.insert(combine_error, 0, values=fast_error)
y_err = np.insert(y_err, 3, values=inserted_error)

x = np.array(x_list_cnn)

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




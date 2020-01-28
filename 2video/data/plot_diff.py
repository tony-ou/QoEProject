import numpy as np
import matplotlib.pyplot as plt

from plot_combine import *

x_amazon, y_amazon = plot_amazon()
x_google, y_google = plot_google()
x_youtube, y_youtube = plot_youtube()
x_cnn, y_cnn = plot_cnn()
x_ms, y_ms = plot_ms()

def get_diff(x, y):
    len = np.shape(x)[0]
    y_diff = []
    x_diff = []
    for i in range(len-2):
        diff_i = (y[i] - y[i+2]) / (x[i+2] - x[i])
        x_i = (x[i+2] + x[i]) / 2
        y_diff.append(diff_i)
        x_diff.append(x_i)
    return x_diff, y_diff

x_amazon_diff, y_amazon_diff = get_diff(x_amazon, y_amazon)
x_google_diff, y_google_diff = get_diff(x_google, y_google)
x_youtube_diff, y_youtube_diff = get_diff(x_youtube, y_youtube)
x_cnn_diff, y_cnn_diff = get_diff(x_cnn, y_cnn)
x_ms_diff, y_ms_diff = get_diff(x_ms, y_ms)



plt.figure()
plt.style.use('ggplot')
plt.xlabel('latency/second(s)')
plt.ylabel('diff')
plt.plot(x_amazon_diff, y_amazon_diff,"blue")
plt.plot(x_google_diff, y_google_diff, "green")
plt.plot(x_youtube_diff, y_youtube_diff, "red")
plt.plot(x_cnn_diff, y_cnn_diff, "black")
plt.plot(x_ms_diff, y_ms_diff, "yellow")
plt.legend(['amazon', 'google', 'youtube', 'cnn', 'microsoft'],
           loc='upper right',
           numpoints=1,
           fancybox=True)
plt.show()


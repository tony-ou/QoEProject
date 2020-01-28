import numpy as np
import matplotlib.pyplot as plt

def plot_amazon():
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
    x = np.array(x_list_amazon)

    x = np.delete(x, 4)
    y_mean = np.delete(y_mean, 4)
    y_se = np.delete(y_se, 4)

    return x, y_mean

def plot_google():
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
    return x, y_mean

def plot_youtube():
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
    return x, y_mean

def plot_cnn():
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
    y_se = np.insert(y_err, 3, values=inserted_error)

    x = np.array(x_list_cnn)
    return x, y_mean

def plot_ms():
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

    x = np.array(x_list_ms)
    return x, y_mean


x_amazon, y_amazon = plot_amazon()
np.save("amazon_x.npy", x_amazon)
np.save("y_amazon.npy", y_amazon)
x_google, y_google = plot_google()
x_youtube, y_youtube = plot_youtube()
x_cnn, y_cnn = plot_cnn()
x_ms, y_ms = plot_ms()

plt.figure()
plt.style.use('ggplot')
plt.xlabel('latency/second(s)')
plt.ylabel('grade')
plt.plot(x_amazon, y_amazon,"blue")
plt.plot(x_google, y_google, "green")
plt.plot(x_youtube, y_youtube, "red")
plt.plot(x_cnn, y_cnn, "black")
plt.plot(x_ms, y_ms, "yellow")
plt.legend(['amazon', 'google', 'youtube', 'cnn', 'microsoft'],
           loc='upper right',
           numpoints=1,
           fancybox=True)
plt.show()

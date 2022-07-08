import time

import matplotlib.pyplot as plt
import pickle
from datetime import datetime
import numpy as np

print(datetime(2022, 5, 9))
with open('time.pickle', 'rb') as f:
    try:
        file = pickle.load(f)
        start_h = 18
        end_h = 19
        start = datetime(2022, 5, 14, start_h)
        end = datetime(2022, 5, 14, end_h)
        """time_list = [i
                     for i in range(1)]"""
        res = []
        maximum = []
        minimum = []
        #for start_h in range(24):
        for day in range(13, 17):
            print(datetime(2022, 5, day, start_h))
            time_list = [  # '%s:%s' % (i[0].hour, i[0].minute)
                '%s' % (i[0].minute)
                for i in file
                if i[0] >= datetime(2022, 5, day, start_h) and i[0] < datetime(2022, 5, day, start_h + 1)]
            price_list = [i[1]
                          for i in file
                          if i[0] >= datetime(2022, 5, day, start_h) and i[0] < datetime(2022, 5, day, start_h + 1)]
            print(price_list)
            print(len(price_list))
            #res.append(sum(price_list) / len(price_list))
            #maximum.append(max(price_list))
            #minimum.append(min(price_list))
            fig, ax = plt.subplots()
            ax.plot(time_list, price_list)
            plt.show()

        """for i in range(1, 3):
            start_h += 1
            end_h += 1
            print(start_h)
            print(end_h)
            price_list = [#price_list[i] + file[i][1]
                         min(price_list[i], file[i][1])
                         for i in range(len(price_list))]
        price_list = [price_list[i] / 3
                      for i in range(len(price_list))]"""
    except Exception as e:
        print('error')
        print(e)
        time_list = []

#x = time_list
#y = price_list
time.sleep(10000)
#plt.stem(x, y)
fig, ax = plt.subplots()  # Create a figure containing a single axes.
fig2, ax2 = plt.subplots()
fig3, ax3 = plt.subplots()
print(time_list)
print(price_list)
# ax.plot(time_list, price_list)  # Plot some data on the axes.
ax.plot([i for i in range(23)], res)
ax2.plot([i for i in range(23)], maximum)
ax3.plot([i for i in range(23)], minimum)
plt.show()
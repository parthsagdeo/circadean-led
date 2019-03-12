import database as db
import Alarms
import controller
import datetime
import time
import matplotlib.pyplot as plt

start_datetime = datetime.datetime(2019, 1, 8)
end_datetime = datetime.datetime(2019, 1, 9)

# get seconds since epoch
start_timestamp = time.mktime(start_datetime.timetuple())
end_timestamp = time.mktime(end_datetime.timetuple())

# generate map (type: datetime) of every minute in range
timestamp_range = range(int(start_timestamp), int(end_timestamp), 60)  # every minute in range, unit: seconds
datetime_range = map(lambda ts: datetime.datetime.fromtimestamp(ts), timestamp_range)

# evaluate LED color at every minute in range --> list of (r, g, b, w) tuples
rgbw_range = list(map(lambda dt: controller.get_color_at_datetime(dt), datetime_range))

# brightness is average of r, b, g, and w values
brightness_range = list(map(lambda rgbw: (rgbw[0] + rgbw[1] + rgbw[2] + rgbw[3])/4, rgbw_range))

# PLOTS
fig = plt.figure()
plt.plot(timestamp_range, brightness_range, color="black")
x_tick_vals = timestamp_range[::60]  # every hour (every 60th minute), unit: seconds
x_tick_labels = list(map(lambda ts: datetime.datetime.fromtimestamp(ts).strftime("%I%p\n%m/%d"), x_tick_vals))
plt.xticks(x_tick_vals, x_tick_labels)

for i, ts in enumerate(timestamp_range[:-1]):  # for every minute in range
    x_seg = [timestamp_range[i], timestamp_range[i+1]]
    y_seg = [brightness_range[i], brightness_range[i+1]]
    color = (rgbw_range[i][0]/100, rgbw_range[i][1]/100, rgbw_range[i][2]/100, 1)
    plt.fill_between(x_seg, y_seg, 0, color=color)

plt.show()


import datetime
import controller
import numpy

if __name__ == "__main__":
    from matplotlib import pyplot as plt

    start_datetime = datetime.datetime(2019, 12, 30, 0, 1, 0)
    end_datetime = datetime.datetime(2019, 12, 30, 1, 0, 0)

    step_size = (end_datetime - start_datetime).total_seconds() / 100
    x_vals = numpy.arange(start_datetime.timestamp(), end_datetime.timestamp(), step_size)

    blue_magnitude = []

    for i in x_vals:
        dt = datetime.datetime.fromtimestamp(i)
        rgbw = controller.get_color_at_datetime(dt)
        color_rgb, brightness = controller.rgbw_to_rgb_brightness(rgbw)

        blue_magnitude.append((rgbw[2] + rgbw[3]/3.0)/4.0)  # blue light

        color = list(map(lambda div: div / 255.0, color_rgb)) + [1]
        print(color)
        plt.bar([i], [brightness], width=step_size, color=color)

    plt.plot(x_vals, blue_magnitude)

    plt.xticks(x_vals[::8],
               list(map(lambda x: datetime.datetime.fromtimestamp(x).strftime("%H:%M"), x_vals[::8])))
    plt.show()

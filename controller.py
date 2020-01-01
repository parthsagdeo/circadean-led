import datetime
import database as db
import numpy


def get_color_at_datetime(dt):
    # Step 1: Get all rules
    rules_list = db.get_rules()

    # Step 2: Determine rule with the most recent activation time
    most_recent_rule = max(rules_list, key=lambda rule: rule.get_last_activation_time(dt)
                            if rule.is_activated(dt) else datetime.datetime.fromtimestamp(0))

    # Step 3: Determine the RGBW of that rule at the current datetime (or black, if no rules have been activated)
    rgbw = (0, 0, 0, 0) if not most_recent_rule.is_activated(dt) \
        else most_recent_rule.get_rgbw_at_datetime(dt)

    return rgbw


def rgbw_to_rgb_brightness(rgbw_tuple):
    brightness = (rgbw_tuple[0] + rgbw_tuple[1] + rgbw_tuple[2] + rgbw_tuple[3]) / 4.0

    max_color_val = max(rgbw_tuple[0:3])
    color_multiplier = 100/max_color_val

    rgb_tuple_0_255 = numpy.multiply(rgbw_tuple[0:3], 2.54 * color_multiplier)

    return rgb_tuple_0_255, brightness


if __name__ == "__main__":
    from matplotlib import pyplot as plt

    start_datetime = datetime.datetime(2019, 12, 30, 0, 1, 0)
    end_datetime = datetime.datetime(2019, 12, 30, 1, 0, 0)

    step_size = (end_datetime - start_datetime).total_seconds() / 100
    x_vals = numpy.arange(start_datetime.timestamp(), end_datetime.timestamp(), step_size)

    blue_magnitude = []

    for i in x_vals:
        dt = datetime.datetime.fromtimestamp(i)
        rgbw = get_color_at_datetime(dt)
        color_rgb, brightness = rgbw_to_rgb_brightness(rgbw)

        blue_magnitude.append((rgbw[2] + rgbw[3]/3.0)/4.0)  # blue light

        color = list(map(lambda div: div / 255.0, color_rgb)) + [1]
        print(color)
        plt.bar([i], [brightness], width=step_size, color=color)

    plt.plot(x_vals, blue_magnitude)

    plt.xticks(x_vals[::8],
               list(map(lambda x: datetime.datetime.fromtimestamp(x).strftime("%H:%M"), x_vals[::8])))
    plt.show()

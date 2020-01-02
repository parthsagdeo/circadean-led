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


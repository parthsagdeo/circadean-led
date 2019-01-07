import datetime
import database as db


def get_color_at_datetime(dt):
    # Step 1: Get all alarms
    alarms_list = db.get_alarms()

    # Step 2: Determine alarm with the most recent activation time
    most_recent_alarm = max(alarms_list, key=lambda alarm: alarm.get_last_activation_time(dt)
                            if alarm.is_activated(dt) else datetime.datetime.fromtimestamp(0))

    # Step 3: Determine the RGBW of that alarm at the current datetime (or black, if no alarms have been activated)
    rgbw = (0, 0, 0, 0) if not most_recent_alarm.is_activated(dt) \
        else most_recent_alarm.get_rgbw_at_datetime(dt)

    return rgbw


x = get_color_at_datetime(datetime.datetime.now())

y = get_color_at_datetime(datetime.datetime.fromtimestamp(0))

print(x)

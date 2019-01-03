import database as db
import Alarms
import datetime

conn = db.create_connection()

o_alarm = Alarms.OneTimeAlarm(datetime.datetime(2018, 12, 25, 0, 0, 0), (1, 2, 3, 4))
db.set_alarm(o_alarm)

alarms = list(db.get_alarms())
print(list(alarms))
from flask import Flask, render_template, request, jsonify
import database as db
import datetime
import Alarms
import controller

app = Flask(__name__)


@app.route("/configurator")
def serve_configurator():
    return render_template("configurator.html")


@app.route("/set_alarm", methods=['POST','GET'])
def set_alarm():
    f = request.form
    alarm_datetime = datetime.datetime(int(f.get('yr')), int(f.get('mon')), int(f.get('day')),
                                       int(f.get('hr')), int(f.get('min')))
    color_tuple = (f.get('r'), f.get('g'), f.get('b'), f.get('w'))

    db.set_alarm(Alarms.OneTimeAlarm(alarm_datetime, color_tuple))

    return "Success!"


@app.route("/set_led", methods=['POST','GET'])
def set_led():
    f = request.form
    rgbw_tuple = (f.get('r'), f.get('g'), f.get('b'), f.get('w'))

    db.set_alarm(Alarms.OneTimeAlarm(datetime.datetime.now(), rgbw_tuple))
    return "Success!"


@app.route("/simulator")
def serve_simulator():
    return render_template("simulator.html")


@app.route("/get_color_at_datetime", methods=['POST'])
def serve_color_at_datetime():
    f = request.form
    dt = datetime.datetime(int(f.get('yr')), int(f.get('mon')), int(f.get('day')),
                                       int(f.get('hr')), int(f.get('min')))

    current_color = controller.get_color_at_datetime(dt)
    return jsonify(current_color)


@app.route("/get_alarms")
def serve_alarms():
    alarms = db.get_alarms()
    alarms_dicts = map(lambda alarm: alarm.get_dict(), alarms)
    return jsonify(list(alarms_dicts))


app.run(debug=True)
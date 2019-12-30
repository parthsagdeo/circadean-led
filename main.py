from flask import Flask, render_template, request, jsonify
import database as db
import datetime
import Rules
import GradientRule
import controller

app = Flask(__name__)


@app.route("/configurator")
def serve_configurator():
    return render_template("configurator.html")


@app.route("/set_onetime_rule", methods=['POST','GET'])
def set_onetime_rule():
    f = request.form
    rule_datetime = datetime.datetime(int(f.get('yr')), int(f.get('mon')), int(f.get('day')),
                                       int(f.get('hr')), int(f.get('min')))
    color_tuple = (int(f.get('r')), int(f.get('g')), int(f.get('b')), int(f.get('w')))

    db.set_rule(Rules.OneTimeRule(rule_datetime, color_tuple))

    return "Success!"


@app.route("/set_gradient_rule", methods=['POST','GET'])
def set_gradient_rule():
    f = request.form
    start_datetime = datetime.datetime(int(f.get('start_yr')), int(f.get('start_mon')), int(f.get('start_day')),
                                       int(f.get('start_hr')), int(f.get('start_min')))
    end_datetime = datetime.datetime(int(f.get('end_yr')), int(f.get('end_mon')), int(f.get('end_day')),
                                     int(f.get('end_hr')), int(f.get('end_min')))
    
    start_brightness = int(f.get('start_brightness'))
    start_temperature = int(f.get('start_temp'))
    end_brightness = int(f.get('end_brightness'))
    end_temperature = int(f.get('end_temp'))
    
    db.set_rule(GradientRule.GradientRule(start_datetime, end_datetime, start_temperature,
                                          end_temperature, start_brightness, end_brightness))

    return "Success!"



@app.route("/set_led", methods=['POST', 'GET'])
def set_led():
    f = request.form
    rgbw_tuple = (int(f.get('r')), int(f.get('g')), int(f.get('b')), int(f.get('w')))

    db.set_rule(Rules.OneTimeRule(datetime.datetime.now(), rgbw_tuple))
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


@app.route("/get_rules")
def serve_rules():
    rules = db.get_rules()
    rules_dicts = map(lambda rule: rule.get_dict(), rules)
    return jsonify(list(rules_dicts))


app.run(debug=True)
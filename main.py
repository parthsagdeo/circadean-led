from flask import Flask, render_template, request, jsonify
from pprint import pprint
import sqlite3
import datetime

DATABASE_PATH = 'control.db'
app = Flask(__name__)


@app.route("/configurator")
def test():
    return render_template("configurator.html")


@app.route("/set_led", methods=['POST','GET'])
def set_led():
    conn = create_connection(DATABASE_PATH)
    with conn:
        if not current_color_table_exists(conn):
            create_current_color_table(conn)

        f = request.form
        color_tuple = (f.get('r'), f.get('g'), f.get('b'), f.get('w'))
        print(color_tuple)
        add_row_to_current_color_table(conn, color_tuple)
        print_current_color_table(conn)

    return "Hi!!!!!"


@app.route("/simulator")
def serve_simulator():
    conn = create_connection(DATABASE_PATH)
    with conn:
        get_current_color(conn)
        return render_template("simulator.html")


@app.route("/get_current_color")
def serve_current_color():
    conn = create_connection(DATABASE_PATH)
    with conn:
        color_dict = get_current_color(conn)
        return jsonify(color_dict)


def create_connection(db_file):
    """ create a database connection to the SQLite database
        specified by the db_file
    :param db_file: database file
    :return: Connection object or None
    """
    try:
        conn = sqlite3.connect(db_file)
        return conn
    except sqlite3.Error as e:
        print(e)
    return None


def create_current_color_table(conn):
    sql = """
        CREATE TABLE current_color (
            id integer PRIMARY KEY,
            date_set integer NOT NULL,
            red integer NOT NULL,
            green integer NOT NULL,
            blue integer NOT NULL,
            white integer NOT NULL           
        )"""
    cur = conn.cursor()
    cur.execute(sql)
    conn.commit()


def current_color_table_exists(conn):
    sql = """SELECT count(*) FROM sqlite_master WHERE type='table' AND name='current_color'"""
    cur = conn.cursor()
    cur.execute(sql)
    result = cur.fetchone()
    print(result)
    return result != (0,)


def add_row_to_current_color_table(conn, rgbw):
    current_datetime = datetime.datetime.now()
    seconds_since_epoch = (current_datetime - datetime.datetime.fromtimestamp(0)).total_seconds()
    sql = """DELETE FROM current_color"""
    cur = conn.cursor()
    cur.execute(sql)
    sql = """INSERT INTO current_color (date_set, red, green, blue, white) VALUES (?, ?, ?, ?, ?)"""
    cur = conn.cursor()
    cur.execute(sql, (seconds_since_epoch,) + rgbw)
    conn.commit()


def print_current_color_table(conn):
    sql = "SELECT * FROM current_color"
    cur = conn.cursor()
    cur.execute(sql)
    print(cur.fetchall())


def get_current_color(conn):
    sql = "SELECT red, green, blue, white FROM current_color"
    cur = conn.cursor()
    cur.execute(sql)
    (r, g, b, w) = cur.fetchone()
    return {'r': r, 'g': g, 'b': b, 'w': w}


app.run(debug=True)


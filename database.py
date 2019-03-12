import sqlite3
import json
import Alarms

DATABASE_FILE = 'control.db'


def create_connection():
    """ create a database connection to the SQLite database
        specified by the db_file
    :param db_file: database file
    :return: Connection object or None
    """
    try:
        conn = sqlite3.connect(DATABASE_FILE)
        return conn
    except sqlite3.Error as e:
        print(e)
    return None


def create_alarms_table(conn):
    sql = """
        CREATE TABLE alarms (
            id integer PRIMARY KEY,
            alarm_data text NOT NULL           
        )"""
    cur = conn.cursor()
    cur.execute(sql)
    conn.commit()


def table_exists(conn, name):
    sql = "SELECT count(*) FROM sqlite_master WHERE type='table' AND name='" + name + "'"
    cur = conn.cursor()
    cur.execute(sql)
    result = cur.fetchone()
    return result != (0,)


def add_row_to_alarms_table(conn, alarm_data):
    data_json = json.dumps(alarm_data)
    sql = """INSERT INTO alarms (alarm_data) VALUES (?)"""
    cur = conn.cursor()
    cur.execute(sql, (data_json, ))
    conn.commit()


def print_table(conn, name):
    sql = "SELECT * FROM " + name
    cur = conn.cursor()
    cur.execute(sql)
    print(cur.fetchall())


def get_rows_from_alarms_table(conn):
    sql = "SELECT alarm_data FROM alarms"
    cur = conn.cursor()
    cur.execute(sql)
    alarm_records = cur.fetchall()

    # Convert a list of tuples (each containing a JSON string representing a dict) into a list of dicts
    alarm_dicts = map(lambda result_tuple: json.loads(result_tuple[0]), alarm_records)

    # Return the list of dicts
    return alarm_dicts


def set_alarm(alarm):
    conn = create_connection()
    with conn:
        if not table_exists(conn, 'alarms'):
            create_alarms_table(conn)

        add_row_to_alarms_table(conn, alarm.get_dict())

        print_table(conn, 'alarms')


def get_alarms():
    conn = create_connection()
    with conn:
        if not table_exists(conn, 'alarms'):
            return None

        alarm_dicts = get_rows_from_alarms_table(conn)

        return list(map(Alarms.BaseAlarm.get_alarm_from_dict, alarm_dicts))

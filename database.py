import sqlite3
import json
import Rules

DATABASE_FILE = 'control.db'


def create_connection():
    """ create a database connection to the SQLite database
        specified by the db_file
    :param db_file: database file
    :return: Connection object or None
    """
    try:
        conn = sqlite3.connect(DATABASE_FILE)

        if not table_exists(conn, 'rules'):
            create_rules_table(conn)

        return conn
    except sqlite3.Error as e:
        print(e)
    return None


def create_rules_table(conn):
    sql = """
        CREATE TABLE rules (
            id integer PRIMARY KEY,
            rule_data text NOT NULL           
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


def add_row_to_rules_table(conn, rule_data):
    data_json = json.dumps(rule_data)
    sql = """INSERT INTO rules (rule_data) VALUES (?)"""
    cur = conn.cursor()
    cur.execute(sql, (data_json, ))
    conn.commit()


def print_table(conn, name):
    sql = "SELECT * FROM " + name
    cur = conn.cursor()
    cur.execute(sql)
    print(cur.fetchall())


def get_rows_from_rules_table(conn):
    sql = "SELECT rule_data FROM rules"
    cur = conn.cursor()
    cur.execute(sql)
    rule_records = cur.fetchall()

    # Convert a list of tuples (each containing a JSON string representing a dict) into a list of dicts
    rule_dicts = list(map(lambda result_tuple: json.loads(result_tuple[0]), rule_records))

    # Return the list of dicts
    return rule_dicts


def set_rule(rule):
    conn = create_connection()
    with conn:
        if not table_exists(conn, 'rules'):
            create_rules_table(conn)

        add_row_to_rules_table(conn, rule.get_dict())

        print_table(conn, 'rules')


def get_rules():
    conn = create_connection()
    with conn:
        rule_dicts = get_rows_from_rules_table(conn)

        return list(map(Rules.BaseRule.get_rule_from_dict, rule_dicts))

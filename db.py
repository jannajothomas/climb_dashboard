# import sqlite3
import mariadb
import sys

import config
import constants
from web_requests import get_csv_reader_from_url


def create_tables_if_needed(con):
    for table in constants.tables:
        sql = 'CREATE TABLE IF NOT EXISTS ' + table['dict_name'] + '('
        for key, value in table.items():
            if key != 'dict_name':
                sql += key + ' ' + value + ','
        sql = sql.rstrip(sql[-1])
        sql += ');'
        cur = con.cursor()
        cur.execute(sql)

    for int_g, yd in constants.grade.items():
        sql = "INSERT IGNORE INTO grades(integer_grade, route_grade) VALUES (%s, %s)"
        params = (int_g, yd)
        cur = con.cursor()
        cur.execute(sql, params)
        con.commit()


def create_connection(database):
    try:
        con = mariadb.connect(
            user=config.user,
            password=config.password,
            host=config.host,
            port=config.port,
            database=database
        )
    except mariadb.Error as e:
        print("Error connecting to MariaDB Platform: {e}", e)
        sys.exit(1)
    return con


# ---------------------SETUP ROUTES------------------------
def update_routes(areas):
    # update database
    con = create_connection("climbDash")

    for area in areas:
        reader = get_csv_reader_from_url(area)
        # skip header
        next(reader)
        for row in reader:
            add_route_to_table(con, list(row))
    con.close()


def add_route_to_table(con, row):
    area, crag, wall = get_area_crag_wall(row[1])
    unkey = row[0] + row[1]
    route = (row[0], row[6], area, crag, row[1], wall, unkey)
    # route = ('name', 'grade', 'area', 'crag', 'location', 'wall')
    sql = "INSERT IGNORE INTO routes(name, grade, area, crag, full_location, wall, unkey)" \
          "VALUES (%s, %s, %s, %s, %s, %s, %s)"
    cur = con.cursor()
    cur.execute(sql, route)
    con.commit()


def get_area_crag_wall(location):
    if location.find('Rumney') != -1:
        applesauce = location.split('> *Rumney')[0]
        if applesauce.find('>') == -1:
            crag = applesauce
            wall = ''
        else:
            crag = applesauce.split('>')[1]
            wall = applesauce.split('>')[0]
        return 'Rumney', crag.strip(), wall.strip()

    elif location.find('Bishop') != -1:
        crag = location.split('>')[0]
        wall = ''
        return 'Bishop', crag.strip(), wall.strip()


# ---------------------SETUP TICKS------------------------
def update_ticks(reader, user_id):
    # skip the header
    next(reader)

    # update database
    database = "climbDash"
    conn = create_connection(database)
    for row in reader:
        add_tick_to_table(conn, list(row), user_id)
    conn.close()


def add_tick_to_table(con, row, user_id):
    tick_id = row[0] + row[1] + row[9] + row[10]
    #             name  location  date   style lead style  notes
    tick = (tick_id, row[1], row[6], row[0], row[9], row[10], row[3], user_id)

    sql = "INSERT IGNORE INTO ticks(id, route_name, location, date, style, lead_style, notes, user_id)" \
          "VALUES (%s, %s, %s, %s, %s, %s, %s, %s)"

    cur = con.cursor()
    cur.execute(sql, tick)
    con.commit()


# ---------------------------------QUERY-------------------------

def get_rows(area, crag, grade, exact_match, view):
    if crag == 'all':
        crag = '%'
    if grade == 'all':
        grade = 17

    # params = (area, crag, lt_grade, grade)
    params = (grade, crag, area)
    sql = ''
    if view == 'all' and exact_match == 'false':
        sql = '''
            SELECT r.crag, r.name, r.grade, t.date, t.style, t.lead_style, t.notes
            FROM routes r
                INNER JOIN grades g
                    ON r.grade = g.route_grade
                    AND g.integer_grade <= %s
                LEFT JOIN ticks t
                    ON r.name = t.route_name
            WHERE r.CRAG LIKE %s AND r.AREA LIKE %s
            ORDER BY r.crag, r.name
            '''
    elif view == 'all' and exact_match == 'true':
        sql = '''
            SELECT r.crag, r.name, r.grade, t.date, t.style, t.lead_style, t.notes
            FROM routes r
                INNER JOIN grades g
                    ON r.grade = g.route_grade
                    AND g.integer_grade = %s
                LEFT JOIN ticks t
                    ON r.name = t.route_name
            WHERE r.CRAG LIKE %s AND r.AREA LIKE %s
            ORDER BY r.crag, r.name
            '''
    elif view == 'completed' and exact_match == 'false':
        sql = '''
            SELECT r.crag, r.name, r.grade, t.date, t.style, t.lead_style, t.notes
            FROM routes r
            INNER JOIN grades g 
                ON r.grade = g.route_grade
                AND g.integer_grade <= %s
            INNER JOIN ticks t
                ON r.name = t.route_name
            WHERE r.CRAG = %s AND r.AREA = %s
            ORDER BY r.crag, r.name
            '''
    elif view == 'completed' and exact_match == 'true':
        sql = '''
            SELECT r.crag, r.name, r.grade, t.date, t.style, t.lead_style, t.notes
            FROM routes r
                INNER JOIN grades g 
                    ON r.grade = g.route_grade
                    AND g.integer_grade = %s
                INNER JOIN ticks t
                        ON r.name = t.route_name
            WHERE r.CRAG = %s AND r.AREA = %s
            ORDER BY r.crag, r.name
            '''
    elif view == 'remaining' and exact_match == 'false':
        sql = '''
            SELECT r.crag, r.name, r.grade, t.date, t.style, t.lead_style, t.notes
            FROM routes r
                INNER JOIN grades g 
                    ON r.grade = g.route_grade
                    AND g.integer_grade <= %s
                LEFT JOIN ticks t
                    ON r.name = t.route_name
                    AND t.route_name IS NULL
                WHERE r.CRAG = %s AND r.AREA = %s
                ORDER BY r.crag, r.name
                '''
    elif view == 'remaining' and exact_match == 'true':
        sql = '''
            SELECT r.crag, r.name, r.grade, t.date, t.style, t.lead_style, t.notes
            FROM routes r
                INNER JOIN grades g 
                    ON r.grade = g.route_grade
                    AND g.integer_grade = %s
                LEFT JOIN ticks t
                    ON r.name = t.route_name
                    AND t.route_name IS NULL
                WHERE r.CRAG = %s AND r.AREA = %s
                ORDER BY r.crag, r.name
                '''
    else:
        print('something wrong.  No cases selected')
    con = create_connection('climbDash')
    cur = con.cursor()
    cur.execute(sql, params)
    return cur.fetchall()

from logging import debug
from types import MethodType
import sqlite3

class DAO:
    '''
    Data Accessing Object allows us to get the DB data without
    directly adding the DB code within the routes!
    '''

    def __init__(self) -> None:
        pass

        
    def get_db_data(self):

        conn = sqlite3.connect('mlb.db')
        cur = conn.cursor()

        cur.execute('SELECT * FROM players;')
        rows = cur.fetchall()
        conn.close()

        #for row in rows:
        #   print(row)
        return rows

    def get_pitcher_stats(self):

        conn = sqlite3.connect('mlb.db')
        cur = conn.cursor()

        cur.execute('SELECT * FROM pitcher_stats;')
        rows = cur.fetchall()
        conn.close()

        return rows

    def get_hitting_stats(self):

        conn = sqlite3.connect('mlb.db')
        cur = conn.cursor()

        cur.execute('SELECT * FROM hitting_stats;')
        rows = cur.fetchall()

        conn.close()

        return rows
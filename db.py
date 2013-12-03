import os
import sys
import sqlite3
from ep import Ep


def initialize(path):
    """
    This method initializes the next database at the given path. It also sets up
    the tables and returns the created db connection.
    """
    path = os.path.expandvars(os.path.expanduser(path))
    # create the database dir if necessary
    if not os.path.exists(os.path.dirname(path)):
        try:
            os.makedirs(os.path.dirname(path))
        except:
            print(sys.argv[0] + ' : Could not create database directory "{0}"!'.format(path))

    # then open a connection and setup the tables
    conn = sqlite3.connect(path, detect_types=sqlite3.PARSE_DECLTYPES)

    with conn:
        c = conn.cursor()
        #test to see if the shows table exists
        test = c.execute(u'''SELECT name FROM sqlite_master WHERE type="table" AND name="eps"''').fetchall()
        if not test:
            c.execute(u'''CREATE TABLE eps(final_loc)''')
            c.execute(u'''CREATE UNIQUE INDEX unique_eps ON eps(final_loc)''')

    return conn


def add_ep(conn, final_loc):
    with conn:
        c = conn.cursor()
        c.execute(u'''INSERT OR REPLACE INTO eps VALUES (?)''', (final_loc,))


def get_all_eps(conn):
    with conn:
        c = conn.cursor()
        c.execute(u'''SELECT rowid, * FROM eps''')
        rows = c.fetchall()
        if rows:
            result = []
            for row in rows:
                try:
                    result.append(Ep(conn, row))
                except:
                    print(u'Could not create Ep for "{}"'.format(row))

            return result
        else:
            return []


def remove_downloaded(conn, downloaded):
    with conn:
        c = conn.cursor()
        c.executemany(u'''DELETE FROM eps WHERE rowid = ?''', ((int(x.id),) for x in downloaded))
        return True


def remove_single(conn, ep):
    with conn:
        c = conn.cursor()
        tvdbid = ep.tvdbid
        c.execute(u'''DELETE FROM eps WHERE tvdbid = ?''', (tvdbid,))
        return True

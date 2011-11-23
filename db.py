import os
import sys
import sqlite3
import bierdopje

def initialize(path):
    '''
    This method initializes the next database at the given path. It also sets up
    the tables and returns the created db connection.
    '''
    # create the database dir if necessary
    if not os.path.exists(os.path.dirname(path)):
        try:
            os.makedirs(os.path.dirname(path))
        except:
            print(sys.argv[0] + ' : Could not create database directory "{0}"!'.format(path))

    # then open a connection and setup the tables
    conn = sqlite3.connect(os.path.expanduser(os.path.expandvars(path)))

    with conn:
        c = conn.cursor()
        #test to see if the shows table exists
        test = c.execute(u'''SELECT name FROM sqlite_master
                WHERE type="table"
                AND name="eps"''').fetchall()
        if not test:
            c.execute(u'''CREATE TABLE eps(job_name, interm_loc, final_loc, tvdbid)''')
            c.execute(u'''CREATE UNIQUE INDEX unique_eps ON eps(job_name,
                    interm_loc)''')

        #test to see if the tvr_shows table exists
        test = c.execute(u'''SELECT name FROM sqlite_master
                WHERE type="table"
                AND name="sids"''').fetchall()
        if not test:
            c.execute(u'''CREATE TABLE sids(tvdbid, sid)''')
            c.execute(u'''CREATE UNIQUE INDEX unique_sids ON sids(tvdbid)''')

    return conn

def add_ep(conn, job_name, interm_loc):
    with conn:
        c = conn.cursor()
        c.execute(u'''INSERT INTO eps(job_name, interm_loc) VALUES (?, ?)''', (job_name, interm_loc))

def update_ep(conn, interm_loc, final_loc, tvdbid):
    with conn:
        c = conn.cursor()
        c.execute(u'''UPDATE eps SET final_loc = ?, tvdbid = ? WHERE interm_loc
                = ?''', (final_loc, tvdbid, interm_loc))

def get_sid(conn, tvdbid):
    with conn:
        c = conn.cursor()
        c.execute(u'''SELECT sid FROM sids WHERE tvdbid = ?''', (tvdbid,))
        result = c.fetchone()[0]
        if not result:
            # not in db, we have to get it from bierdopje
            sid = bierdopje.get_show_id(tvdbid)
            if sid:
                c.execute(u'''INSERT INTO sids VALUES (?, ?)''', (tvdbid, sid))
            result = sid
        return result

def get_all_eps(conn):
    with conn:
        c = conn.cursor()
        c.execute(u'''SELECT * FROM eps''')
        return c.fetchall()

def remove_downloaded(conn, downloaded):
    with conn:
        c = conn.cursor()
        tvdbids = [(x[2],) for x in downloaded.values()]
        c.executemany(u'''DELETE FROM eps WHERE tvdbid = ?''', tvdbids)



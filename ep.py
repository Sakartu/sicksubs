import db
import nameparser

class Ep(object):
    def __init__(self, conn):
        self.conn = conn

    def from_row(self, row):
        self.job_name = row[0]
        self.final_loc = row[2]
        self.tvdbid = row[3]
        self.sid = db.get_sid(self.conn, self.tvdbid)
        (self.season, self.ep) = nameparser.get_ep_details(self.job_name)
        self.sub = None
        return self

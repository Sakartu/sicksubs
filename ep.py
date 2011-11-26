import db
import nameparser

class Ep(object):
    def __init__(self, conn):
        self.conn = conn

    def from_row(self, row):
        self.interm_loc = row[0]
        self.final_loc = row[1]
        self.tvdbid = row[2]
        self.job_name = nameparser.get_job_name(self.interm_loc)
        self.sid = db.get_sid(self.conn, self.tvdbid)
        (self.season, self.ep) = nameparser.get_ep_details(self.job_name)
        self.sub = None
        return self

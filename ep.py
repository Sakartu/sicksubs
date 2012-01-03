import db
import nameparser

class Ep(object):
    def __init__(self, conn, row):
        self.conn = conn
        self.interm_loc = row[0]
        self.final_loc = row[1]
        self.tvdbid = row[2]
        self.job_name = nameparser.get_job_name(self.interm_loc)
        self.sid = db.get_sid(self.conn, self.tvdbid)
        (_, self.season, self.ep) = nameparser.get_ep_details(self.job_name)
        self.sub = None
        self.result = False

    def __repr__(self):
        return self.job_name

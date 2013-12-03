class Ep(object):
    def __init__(self, conn, row):
        self.conn = conn
        self.id = row[0]
        self.final_loc = row[1]

import sqlite3

class JobsDB:
    def __init__(self):
        # print('init called')
        pass

    def __enter__(self):
        # print('enter called')
        self.conn = sqlite3.connect('jobs.db')
        self.cur = self.conn.cursor()
        return self

    def __exit__(self, exc_type, exc_value, exc_traceback):
        # print('exit called', exc_type, exc_value, exc_traceback)
        self.conn.commit()
        self.conn.close()

    def create_db_table(self):
        self.cur.execute("""CREATE TABLE IF NOT EXISTS jobs (jobid integer, jobobj blob)""")
        self.conn.commit()

    def insert_request(self, jobid, jobobj):
        self.cur.execute("""INSERT INTO jobs VALUES (?, ?)""", (jobid,jobobj))
        self.conn.commit()

    def fetch_request_by_jobid(self, jobid):
        self.cur.execute("""SELECT * FROM jobs WHERE jobid=:jobid """, {'jobid':jobid})
        jobslist = self.cur.fetchall()
        return jobslist

    def remove_request_by_jobid(self, jobid):
        self.cur.execute("""DELETE FROM jobs WHERE jobid=:jobid""", {'jobid':jobid})
        self.conn.commit()

    def update_request_by_jobid(self, jobid, jobobj):
        self.cur.execute("""UPDATE jobs SET jobobj=:jobobj WHERE jobid=:jobid""", {'jobid':jobid, 'jobobj':jobobj})
        self.conn.commit()

if __name__ == '__main__':
    with JobsDB() as jdb:
        jdb.create_db_table()
        jdb.insert_request(1, 'string as blob')
        jobslist = jdb.fetch_request_by_jobid(jobid=1)
        print(jobslist)

import os
import sqlite3


class DB():
    def __init__(self):
        if os.path.isfile('endeavors.db'):
            self.con = sqlite3.connect('endeavors.db')
            self.cur = self.con.cursor()
        else:
            self.con = sqlite3.connect('endeavors.db')
            self.cur = self.con.cursor()
            self.cur.execute(
                "CREATE TABLE endeavors(idx INTEGER PRIMARY KEY, big_idea, details)")
            self.con.commit()

    def initial_read(self):
        res = self.cur.execute("SELECT * FROM endeavors")
        entries_list = res.fetchall()
        return entries_list

    def update_db(self, collection):
        self.cur.execute("DELETE FROM endeavors")
        self.con.commit()
        for endeavor in collection:
            self.cur.execute(
                "INSERT INTO endeavors (idx, big_idea, details) VALUES (?, ?, ?)", (endeavor.index, endeavor.big_idea, endeavor.details))
            self.con.commit()

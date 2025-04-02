import mysql.connector


mydb =mysql.connector.connect(host="ev-finder-db.cxqospjboyrv.eu-west-2.rds.amazonaws.com", user="admin", passwd="ev-finder-db")

class Db:
    def __init__(self):
        self.cnx = mysql.connector.connect(
            host="ev-finder-db.cxqospjboyrv.eu-west-2.rds.amazonaws.com",
            user="admin",
            password="ev-finder-db",
            database="ev-finder-db"
            )
        self.cur = self.cnx.cursor(dictionary=True,buffered=True)

    def select(self, q, params=None):
        self.cur.execute(q, params)
        return self.cur.fetchall()

    def selectOne(self, q, params=None):
        self.cur.execute(q, params)
        return self.cur.fetchone()

    def insert(self, q, params=None):
        self.cur.execute(q, params)
        self.cnx.commit()
        return self.cur.lastrowid

    def update(self, q, params=None):
        self.cur.execute(q, params)
        self.cnx.commit()
        return self.cur.rowcount

    def delete(self, q, params=None):
        self.cur.execute(q, params)
        self.cnx.commit()
        return self.cur.rowcount
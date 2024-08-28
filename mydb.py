import sqlite3

class Database:
    def __init__(self, db):
        self.conn = sqlite3.connect(db)
        self.cur = self.conn.cursor()
        self.cur.execute("CREATE TABLE IF NOT EXISTS expense_record (id INTEGER PRIMARY KEY, item_name TEXT, item_price REAL, purchase_date TEXT, item_group TEXT)")
        self.conn.commit()

    def insertRecord(self, item_name, item_price, purchase_date, item_group):
        self.cur.execute("INSERT INTO expense_record VALUES (NULL, ?, ?, ?, ?)", (item_name, item_price, purchase_date, item_group))
        self.conn.commit()

    def fetchRecord(self, query):
        self.cur.execute(query)
        return self.cur.fetchall()

    def updateRecord(self, item_name, item_price, purchase_date, item_group, id):
        self.cur.execute("UPDATE expense_record SET item_name = ?, item_price = ?, purchase_date = ?, item_group = ? WHERE id = ?", (item_name, item_price, purchase_date, item_group, id))
        self.conn.commit()

    def removeRecord(self, id):
        self.cur.execute("DELETE FROM expense_record WHERE id = ?", (id,))
        self.conn.commit()

    def __del__(self):
        self.conn.close()

import psycopg2
from authentication import login_db, password_db, host_db


class DatabasePG:

    def __init__(self, database):
        try:
            self.con = psycopg2.connect(
                database=database,
                user=login_db,
                password=password_db,
                host=host_db,
            )
        except psycopg2.OperationalError:
            return False
            Telegram("Не удалось подключиться к базе данных")

    def get_select(self, query):
        cur = self.con.cursor()
        cur.execute(query)
        rows = cur.fetchall()
        cur.close()
        return rows

    def update(self, query):
            self.cur = self.con.cursor()
            self.cur.execute(query)
            self.con.commit()
            self.cur.close()

    def close_db(self):
        self.con.close()

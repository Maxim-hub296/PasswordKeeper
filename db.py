import sqlite3 as sql


class DbUser:
    def __init__(self, db):
        self.db = db
        self.con = sql.connect(db)
        self.cursor = self.con.cursor()

    def correct_pin(self, pin: str):
        self.cursor.execute("SELECT * FROM pincode")
        if pin == self.cursor.fetchone()[0]:
            print("Вы авторизованы!")
        else:
            print("Пароль неверный")

    def print_passwords(self):
        self.cursor.execute("SELECT * FROM passwords")

        for name, password in self.cursor.fetchall():
            print(f"{name} - {password}")


test = DbUser("passwords.db")
test.print_passwords()

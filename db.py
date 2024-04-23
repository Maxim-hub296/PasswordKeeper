# Класс для работы с базой данных
import sqlite3 as sql


class DbUser:
    """
    Класс для работы с базой данных
    """

    def __init__(self, db):
        """
        :param db: база данных, с которой нужно работать
        """
        self.con = sql.connect(db)  # Подключаемся/создаем базу данных
        self.cursor = self.con.cursor()  # Не знаю, как это описать. Нужно, чтобы выполнять SQL-запросы

    def correct_pin(self, pin: str):
        """

        :param pin: введенный пин-код
        :return:
        """
        self.cursor.execute("SELECT * FROM pincode")  # Вызываем значения из таблицы
        # Проверка на пин-код
        if pin == self.cursor.fetchone()[0]:
            print("Вы авторизованы!")
        else:
            print("Пароль неверный")

    def print_passwords(self):
        """
        Метод вывода пароля
        :return:
        """
        self.cursor.execute("SELECT * FROM passwords")

        for name, password in self.cursor.fetchall():
            print(f"{name} - {password}")


# Тесты. Не обращать внимания
test = DbUser("passwords.db")
test.print_passwords()

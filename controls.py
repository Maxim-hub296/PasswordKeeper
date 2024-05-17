# Файл со всеми графическими элементами программы

import flet as ft
from random import choices, choice, shuffle
from os import listdir
from pyperclip import copy
from string import ascii_lowercase, ascii_uppercase, digits, punctuation
from func import *


class GeneratePasswordButton(ft.UserControl):
    """
    Это класс кнопки "Сгенерировать пароль"
    """

    def __init__(self, choose: dict, name: ft.TextField, length: ft.TextField, ):
        """

        :param choose: словарь на основе выбора пользователя символов
        :param name: название сайта, для которого пароль
        :param length: Введенная длина пароля
        """
        super().__init__()
        self.choose = choose
        self.length = length
        self.name = name
        self.user = None
        self.user_password = None

    def build(self):
        """
        Это служебный метод библиотеки flet (читать документацию flet)
        :return: создает в окне приложения колонну с кнопкой
        """
        button = ft.ElevatedButton(text="Сгенерировать пароль", on_click=self.on_click, width=200)
        return ft.Column(controls=[button])

    def alert_error(self):
        """
        Метод создания диалога, при отсутствии выбора символов
        :return:
        """
        dlg = ft.AlertDialog(title=ft.Text("Невозможно создать пустой пароль"))

        self.page.dialog = dlg
        dlg.open = True
        self.page.update()

    def on_click(self, e):
        """
        События происходящие при нажатии на кнопку
        :param e: служебный параметр, обязательный для запуска (читать документацию flet)
        :return:
        """
        # Проверяем выбрал ли пользователь хотя бы один набор символов
        if not any(self.choose.values()):
            # Если выбор не сделан, вызываем диалог ошибки
            self.alert_error()
            return
        # Иначе генерируем пароль
        self.generate_password()

    def generate_password(self):
        """
        Алгоритм генерации пароля, на основе введенной длины, выборе символов и названии сайта
        :return:
        """
        length = int(self.length.value)  # Длинна приходит в str. Поэтому обязательно делаем int
        symbols = ''  # Создаем строку, в которую будем класть нужные символы
        password = []  # Создаем список, в который кладем случайный символ из symbols
        kirill_up = ''.join(chr(i) for i in range(ord('А'), ord('Я') + 1))  # Кириллица в верхнем регистре
        kirill_low = ''.join(chr(i) for i in range(ord('а'), ord('я') + 1))  # Кириллица в нижнем регистре
        # Символьный словарь
        symbols_dict = {"kirill_low": kirill_low,
                        "kirill_up": kirill_up,
                        "latin_low": ascii_lowercase,
                        "latin_up": ascii_uppercase,
                        "digits": digits,
                        "special": punctuation}
        # Генерируем последовательность для пароля. Учитывая, чтобы из выбранных коллекций был хотя бы один символ
        for symbolsset in self.choose:
            if self.choose[symbolsset]:  # Проверяем выбрана ли последовательность символов
                password.append(choice(symbols_dict[symbolsset]))  # Добавляем случайный из последовательности.
                # Здесь и учитывается наличие хоть бы одного символа
                symbols += symbols_dict[symbolsset]  # Добавляем последовательность

        password.extend(choices(symbols, k=length - len(password)))  # Оставляем выбранные символы в случайном порядке
        # длинной self.length
        shuffle(password)  # Перемешиваем
        password = "".join(password)  # Делаем пароль строкой

        self.save_password(password, self.name.value)

        # Создаем и/или открываем файл для записи(добавления)
        with open(file="password.txt", mode="a", encoding="utf-8") as file:
            file.write(f"{self.name.value} - {password}\n")  # Делаем красивую запись в файл. Имя - пароль

        # Уведомляем, что пароль создан и предлагаем скопировать
        dlg = ft.AlertDialog(title=ft.Text(f"Пароль создан!\nПароль - {password}"), actions=[CopyButton(password)])

        self.page.dialog = dlg
        dlg.open = True
        self.page.update()

    def save_password(self, password, name):
        data = read_toml_file()
        data["passwords"][self.user][name] = Crypto.encrypt(password, self.user_password)
        write_toml_file(data)


class ShowPasswordButton(ft.UserControl):
    """
     Класс кнопки "Показать пароли"

    """

    def __init__(self):
        super().__init__()
        self.user = None
        self.user_password = None

    def build(self):
        """
        Служебный метод библиотеки flet (читать документацию flet)
        :return: создает в окне приложения колонну с кнопкой
        """
        button = ft.ElevatedButton(text="Показать пароли", on_click=self.on_click, width=200)
        return ft.Column(controls=[button])

    def on_click(self, e):
        """
        Событие, происходящие при нажатии на кнопку
        :param e: служебный параметр (читать документацию flet)
        :return:
        """
        # Проверяем, есть ли у пользователя пароли

        if "passwords.db" not in listdir():
            # Если нет - вызываем диалог с ошибкой
            dlg = ft.AlertDialog(title=ft.Text(value="У вас еще нет паролей"))
            self.page.dialog = dlg
            dlg.open = True
            self.page.update()
            # Иначе показываем пароли
        else:
            self.show_password()

    def show_password(self):
        """
        Метод показывающий окно с паролями и возможностью их скопировать
        :return:
        """
        contents = []  # Созадаем список, куда кладем пароли
        passwords = read_toml_file()['passwords'][self.user]
        print(passwords)

        for name, password in passwords.items():
            # Заполняем окно с паролями
            contents.append(PasswordCopyLine(ft.Text(value=f"{name} - {Crypto.decrypt(password, self.user_password)}")))

        # Создаем диалог
        dlg = ft.AlertDialog(title=ft.Text(value="Сохраненные пароли:"),
                             content=ft.Text(value="Посмотрите и скопируйте свои пароли"),
                             actions=[i for i in contents])
        self.page.dialog = dlg
        dlg.open = True
        self.page.update()




class SelectSymbols(ft.UserControl):
    """
    Класс поля выбора символов
    """

    def __init__(self, choose: dict):
        """

        :param choose: словарь для выбора. Используется в GeneratePasswordButton
        """
        super().__init__()
        self.choose = choose

    def build(self):
        """
        Служебный метод, создающий выборы символов (читать документацию flet)
        :return:
        """
        kirill_low = ft.Checkbox(label="Кириллица нижнего регистра", on_change=self.on_change, key="kirill_low",
                                 value=self.choose["kirill_low"])
        kirill_up = ft.Checkbox(label="Кириллица  верхнего регистра", on_change=self.on_change, key="kirill_up",
                                value=self.choose["kirill_up"])
        latin_low = ft.Checkbox(label="Латиница нижнего регистра", on_change=self.on_change, key="latin_low",
                                value=self.choose["latin_low"])
        latin_up = ft.Checkbox(label="Латиница верхнего регистра", on_change=self.on_change, key="latin_up",
                               value=self.choose["latin_up"])
        digits = ft.Checkbox(label="Цифры", on_change=self.on_change, key="digits", value=self.choose["digits"])
        special = ft.Checkbox(label="Специальные символы", on_change=self.on_change, key="special",
                              value=self.choose["special"])

        return ft.Column(controls=[kirill_low, kirill_up, latin_low,
                                   latin_up, digits, special])

    def on_change(self, e):
        """
        Событие, происходящие на нажатие кого либо выбора
        :param e: служебный параметр (читать документацию flet)
        :return:
        """
        self.choose[e.control.key] = e.control.value


class PasswordCopyLine(ft.UserControl):
    """
    Поле копирование. Используется в ShowPasswordButton
    """

    def __init__(self, password: ft.Text):
        """
        :param password: получает пароль из списка (В ShowPasswordButton)
        """
        super().__init__()
        self.password = password.value

    def build(self):
        """
        Служебный метод (читать документацию flet)
        :return:
        """
        return ft.Row(controls=[ft.Text(value=self.password),
                                ft.ElevatedButton(on_click=self.on_click, text="Скопировать",
                                                  icon=ft.icons.CONTENT_COPY)])

    def on_click(self, e):
        """
        События, происходящие на нажатие кнопки
        :param e: служебный параметр (читать документацию flet)
        :return:
        """
        # Создаем диалог
        dlg = ft.AlertDialog(title=ft.Text("Пароль скопирован"))
        self.page.dialog = dlg
        self.copy_password()
        dlg.open = True
        self.page.update()

    def copy_password(self):
        """
        Метод копирования пароля
        :return:
        """
        password = self.password.split(' - ')[1]
        copy(password)


class CopyButton(ft.UserControl):
    """
    То же самое, что прошлый класс, но только кнопка
    """

    def __init__(self, password):
        super().__init__()
        self.password = password

    def build(self):
        return ft.Row(
            controls=[ft.ElevatedButton(text="Скопировать!", icon=ft.icons.CONTENT_COPY, on_click=self.on_click)])

    def on_click(self, e):
        copy(self.password)


class Autentificator(ft.UserControl):
    def __init__(self, main_frame):
        super().__init__()
        # self.toml_data = read_toml_file()
        self.main_frame = main_frame
        self.login = ft.TextField(label="Логин", width=150)
        self.password = ft.TextField(label="Пароль", width=150, password=True, can_reveal_password=True)
        self.login_button = ft.ElevatedButton(text="Войти", on_click=self.on_click_login)
        self.register_button = ft.ElevatedButton(text="Зарегистрироваться!", on_click=self.on_click_register)

    def build(self):
        login_and_password_row = ft.Row(controls=[self.login, self.password])
        buttons_row = ft.Row(controls=[self.login_button, self.register_button])
        return ft.Column(controls=[login_and_password_row, buttons_row])

    def on_click_login(self, e):
        self.toml_data = read_toml_file()
        dlg_success = ft.AlertDialog(title=ft.Text("Авторизация прошла успешно"))
        dlg_no_user = ft.AlertDialog(title=ft.Text("Пользователь с таким именем не обнаружен"))
        dlg_wrong_password = ft.AlertDialog(title=ft.Text("Неверный пароль"))
        user = self.login.value.lower()
        password = self.password.value

        if user not in self.toml_data['users']:
            dialog = dlg_no_user

        elif not Hasher.verify_password(password, self.toml_data["users"][user]):
            dialog = dlg_wrong_password

        else:
            dialog = dlg_success
            self.main_frame.visible = True
            self.visible = False
            self.update()
            self.main_frame.update()
            self.main_frame.plane_password = password
            self.main_frame.user = user
            self.main_frame.generateButton.user = user
            self.main_frame.showButton.user = user
            self.main_frame.generateButton.user_password = password
            self.main_frame.showButton.user_password = password

        self.page.dialog = dialog
        dialog.open = True



        self.page.update()


    def on_click_register(self, e):

        self.new_login = ft.TextField(label="Введите логин")
        self.new_password = ft.TextField(label="Введите пароль")
        contents = [self.new_login, ft.Text(" "),self.new_password,
                    ft.ElevatedButton("Зарегистрироваться!", on_click=self.register)]
        self.dlg = ft.AlertDialog(title=ft.Text("Регистрация"),
                             actions=[i for i in contents])

        self.page.dialog = self.dlg
        self.dlg.open = True
        self.page.update()

    def register(self, e):
        data = read_toml_file()
        data["users"][self.new_login.value.lower()] = Hasher.get_password_hash(self.new_password.value)
        data["passwords"][self.new_login.value] = {}
        write_toml_file(data)
        self.dlg.open = False
        self.page.update()




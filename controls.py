# Файл с графическими элементами программы
import flet as ft
from func import *
from pyperclip import copy
from dialogs import RegisterDialog

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


class Authenticator(ft.UserControl):
    def __init__(self, main_frame):
        super().__init__()
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
        toml_data = read_toml_file()
        dlg_success = ft.AlertDialog(title=ft.Text("Авторизация прошла успешно!"))
        dlg_no_user = ft.AlertDialog(title=ft.Text("Пользователь с таким именем не обнаружен"))
        dlg_wrong_password = ft.AlertDialog(title=ft.Text("Неверный пароль"))
        user = self.login.value.lower()
        password = self.password.value

        if user not in toml_data['users']:
            dialog = dlg_no_user

        elif not Hasher.verify_password(password, toml_data["users"][user]):
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
            self.main_frame.save_button.user = user
            self.main_frame.save_button.user_password = password



        self.page.dialog = dialog
        dialog.open = True

        self.page.update()

    def on_click_register(self, e):

        dialog = RegisterDialog(self.page)
        dialog.create()

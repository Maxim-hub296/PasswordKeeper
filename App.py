# Класс всего приложения
from controls import *
from buttons import *


class PasswordKeeper(ft.UserControl):
    def __init__(self):
        """
        Инициализируем все, что нужно
        """
        super().__init__()
        self.main_frame = MainFrame()
        self.authentification_frame = Autentificator(self.main_frame)

    def build(self):
        """
        Служебный метод (читать документацию flet)
        :return:
        """

        return ft.Column(controls=[self.authentification_frame, self.main_frame])


class MainFrame(ft.UserControl):
    """
    Класс всего приложения
    """

    def __init__(self):
        """
        Инициализируем все, что нужно
        """
        super().__init__()
        self.visible = False
        self.user = None
        # Словарь с выбором
        self.choose = {
            "kirill_low": False,
            "kirill_up": False,
            "latin_low": True,
            "latin_up": False,
            "digits": True,
            "special": False
        }

        # Поле для ввода названия пароля
        self.name = ft.TextField(label="Введите название пароля", width=200)
        # Поле для ввода длины пароля
        self.length = ft.TextField(label="Введите длину пароля", input_filter=ft.NumbersOnlyInputFilter(), width=200,
                                   value="10")
        # Генерируем классы из controls.py
        self.generateButton = GeneratePasswordButton(self.choose, self.name, self.length)
        self.showButton = ShowPasswordButton()
        self.checkBox = SelectSymbols(self.choose)

    def build(self):
        """
        Служебный метод (читать документацию flet)
        :return:
        """
        password_button_row = ft.Row(controls=[self.generateButton, self.showButton], alignment=ft.alignment.center)
        return ft.Column(controls=[password_button_row, self.name, self.length, self.checkBox],
                         alignment=ft.alignment.center)

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
        self.authentification_frame = Authenticator(self.main_frame)

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
        self.name = ft.TextField(label="Введите название пароля", width=440)
        self.password = ft.TextField(label="Введите пароль", width=300)
        # Поле для ввода длины пароля
        self.length = ft.TextField(label="Введите длину пароля", input_filter=ft.NumbersOnlyInputFilter(), width=440,
                                   value="10")
        # Генерируем классы из controls.py и buttons.py
        self.generateButton = GeneratePasswordButton(self.choose, self.name, self.length, self.password)
        self.showButton = ShowPasswordButton()
        self.checkBox = SelectSymbols(self.choose)
        self.checkBox.visible = False
        self.save_button = SaveButton(self.password, self.name)
        self.show_parameters_button = ShowParameters(self.checkBox)

    def build(self):
        """
        Служебный метод (читать документацию flet)
        :return:
        """
        password_button_row = ft.Row(controls=[self.showButton], alignment=ft.alignment.center)
        password_and_save_button_row = ft.Row(
            controls=[self.password, ft.Column(controls=[self.generateButton, self.save_button])])
        return ft.Column(
            controls=[password_button_row, self.name, password_and_save_button_row, self.length,
                      self.show_parameters_button, self.checkBox],
            alignment=ft.alignment.center)

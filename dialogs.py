import flet as ft
from func import *


class RegisterDialog:
    def __init__(self, other_page: ft.Page):
        self.login = ft.TextField(label="Введите логин")
        self.password = ft.TextField(label="Введите пароль")
        self.other_page = other_page
        self.dlg = None
        self.data = read_toml_file()

    def create(self):
        button = ft.ElevatedButton(text="Зарегистрироваться!", on_click=self.on_click)
        contents = [self.login, ft.Text(" "), self.password, button]

        title = ft.Text("Регистрация")
        self.dlg = ft.AlertDialog(title=title,
                                  actions=[content for content in contents])

        self.other_page.dialog = self.dlg
        self.dlg.open = True
        self.other_page.update()

    def on_click(self, e):
        self.register()

    def register(self):
        self.data["users"][self.login.value.lower()] = Hasher.get_password_hash(self.password.value)
        self.data["passwords"][self.login.value] = {}
        write_toml_file(self.data)
        self.dlg.open = False
        self.other_page.update()

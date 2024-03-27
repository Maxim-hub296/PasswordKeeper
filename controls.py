import flet as ft
from random import choice


class GeneratePasswordButton(ft.UserControl):
    def __init__(self, choose: dict,  name: str, length=10):
        super().__init__()
        self.choose = choose
        self.length = length
        self.name = name

    def build(self):
        button = ft.ElevatedButton(text="Сгенерировать пароль", on_click=self.generate_password, width=200)
        return ft.Column(controls=[button])

    def generate_password(self, e):
     pass


class ShowPasswordButton(ft.UserControl):
    def build(self):
        button = ft.ElevatedButton(text="Показать пароли", on_click=self.show_password, width=200)
        return ft.Column(controls=[button])

    def show_password(self, e):
        pass


class CreateCodeButton(ft.UserControl):
    def build(self):
        button = ft.ElevatedButton(text="Создать PIN", on_click=self.create_code, width=200)
        return ft.Column(controls=[button])

    def create_code(self, e):
        pass


class DelCodeButton(ft.UserControl):
    def build(self):
        button = ft.ElevatedButton(text="Удалить PIN", on_click=self.del_code, width=200)
        return ft.Column(controls=[button])

    def del_code(self, e):
        pass


class CheckBox(ft.UserControl):
    def __init__(self, choose: dict):
        super().__init__()
        self.choose = choose

    def build(self):
        kirill_low = ft.Checkbox(label="Кириллица нижнего регистра", on_change=self.on_change, key="kirill_low")
        kirill_up = ft.Checkbox(label="Кириллица  верхнего регистра", on_change=self.on_change, key="kirill_up")
        latin_low = ft.Checkbox(label="Латиница нижнего регистра", on_change=self.on_change, key="latin_low")
        latin_up = ft.Checkbox(label="Латиница нижнего регистра", on_change=self.on_change, key="latin_up")
        digits = ft.Checkbox(label="Цифры", on_change=self.on_change, key="digits")
        special = ft.Checkbox(label="Специальные символы", on_change=self.on_change, key="special")

        return ft.Column(controls=[kirill_low, kirill_up, latin_low,
                                   latin_up, digits, special])

    def on_change(self, e):
        print(e.control.value)

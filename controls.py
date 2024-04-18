import flet as ft
from random import choices, choice, shuffle
from os import listdir
from pyperclip import copy
from string import ascii_lowercase, ascii_uppercase, digits, punctuation


class GeneratePasswordButton(ft.UserControl):
    def __init__(self, choose: dict, name: ft.TextField, length: ft.TextField):
        super().__init__()
        self.choose = choose
        self.length = length
        self.name = name

    def build(self):
        button = ft.ElevatedButton(text="Сгенерировать пароль", on_click=self.on_click, width=200)
        return ft.Column(controls=[button])

    def alert_error(self):
        dlg = ft.AlertDialog(title=ft.Text("Невозможно создать пустой пароль"))

        self.page.dialog = dlg
        dlg.open = True
        self.page.update()

    def on_click(self, e):
        if not any(self.choose.values()):
            self.alert_error()
            return
        self.generate_password()

    def generate_password(self):
        length = int(self.length.value)
        symbols = ''
        password = []
        kirill_up = ''.join(chr(i) for i in range(ord('А'), ord('Я') + 1))
        kirill_low = ''.join(chr(i) for i in range(ord('а'), ord('я') + 1))
        symbols_dict = {"kirill_low": kirill_low,
                        "kirill_up": kirill_up,
                        "latin_low": ascii_lowercase,
                        "latin_up": ascii_uppercase,
                        "digits": digits,
                        "special": punctuation}
        for symbolsset in self.choose:
            if self.choose[symbolsset]:
                password.append(choice(symbols_dict[symbolsset]))
                symbols += symbols_dict[symbolsset]

        password.extend(choices(symbols, k=length - len(password)))
        shuffle(password)
        password = "".join(password)

        with open(file="password.txt", mode="a", encoding="utf-8") as file:
            file.write(f"{self.name.value} - {password}\n")

        dlg = ft.AlertDialog(title=ft.Text(f"Пароль создан!\nПароль - {password}"), actions=[CopyButton(password)])

        self.page.dialog = dlg
        dlg.open = True
        self.page.update()


class ShowPasswordButton(ft.UserControl):
    def build(self):
        button = ft.ElevatedButton(text="Показать пароли", on_click=self.on_click, width=200)
        return ft.Column(controls=[button])

    def on_click(self, e):
        if "password.txt" not in listdir():
            dlg = ft.AlertDialog(title=ft.Text(value="У вас еще нет паролей"))
            self.page.dialog = dlg
            dlg.open = True
            self.page.update()
        else:
            self.show_password()

    def show_password(self):
        contents = []
        with open("password.txt", encoding="utf-8") as f:
            passwords = [i.strip() for i in f]

        for password in passwords:
            contents.append(PasswordCopyLine(ft.Text(value=password)))

        dlg = ft.AlertDialog(title=ft.Text(value="Сохраненные пароли:"),
                             content=ft.Text(value="Посмотрите и скопируйте свои пароли"),
                             actions=[i for i in contents])
        self.page.dialog = dlg
        dlg.open = True
        self.page.update()


class CreateCodeButton(ft.UserControl):
    def __init__(self, pin: str):
        super().__init__()
        self.pin = pin
        self.entry_field = ft.TextField(label="Поле ввода")
        self.entry_button = ft.ElevatedButton(text="Ввести", on_click=self.create_pin)

    def build(self):
        button = ft.ElevatedButton(text="Создать PIN", on_click=self.on_click, width=200)
        return ft.Column(controls=[button])

    def on_click(self, e):
        dlg = ft.AlertDialog(title=ft.Text("Создайте PIN-code"),
                             content=ft.Text("Введите 4 цифры"),
                             actions=[self.entry_field, self.entry_button])
        self.page.dialog = dlg
        dlg.open = True
        self.page.update()

        print(self.pin)

    def create_pin(self, e):
        print(f"до изменения - {self.pin}")
        self.pin = self.entry_field.value
        print(f"после изменения - {self.pin}")


class DelCodeButton(ft.UserControl):
    def build(self):
        button = ft.ElevatedButton(text="Удалить PIN", on_click=self.del_code, width=200)
        return ft.Column(controls=[button])

    def del_code(self, e):
        pass


class SelectSymbols(ft.UserControl):
    def __init__(self, choose: dict):
        super().__init__()
        self.choose = choose

    def build(self):
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
        self.choose[e.control.key] = e.control.value


class PasswordCopyLine(ft.UserControl):
    def __init__(self, password: ft.Text):
        super().__init__()
        self.password = password.value

    def build(self):
        return ft.Row(controls=[ft.Text(value=self.password),
                                ft.ElevatedButton(on_click=self.on_click, text="Скопировать",
                                                  icon=ft.icons.CONTENT_COPY)])

    def on_click(self, e):
        dlg = ft.AlertDialog(title=ft.Text("Пароль скопирован"))
        self.page.dialog = dlg
        self.copy_password()
        dlg.open = True
        self.page.update()

    def copy_password(self):
        index = self.password.find("- ")
        copy(self.password[index:])


class CopyButton(ft.UserControl):
    def __init__(self, password):
        super().__init__()
        self.password = password

    def build(self):
        return ft.Row(
            controls=[ft.ElevatedButton(text="Скопировать!", icon=ft.icons.CONTENT_COPY, on_click=self.on_click)])

    def on_click(self, e):
        copy(self.password)

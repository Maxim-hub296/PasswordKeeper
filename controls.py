import flet as ft
from string import ascii_lowercase, ascii_uppercase, digits, punctuation
from random import choices, choice, shuffle


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
        controls = [ft.TextField(), ft.ElevatedButton(text="тест")]
        content = ft.Column(controls)
        # dlg = ft.AlertDialog(title=ft.Text("Дурак? Я не могу создать пустой пароль!"))
        dlg = ft.AlertDialog(title=ft.TextField(),
                             content=content)

        self.page.dialog = dlg
        dlg.open = True
        self.page.update()

    def on_click(self, e):
        if not any(self.choose.values()):
            print('!!!!')
            self.alert_error()
            return
        self.generate_password()
        print(self)

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

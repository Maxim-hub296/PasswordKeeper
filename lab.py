import flet as ft
from pyperclip import copy


class PasswordCopyLine(ft.UserControl):
    def __init__(self, password: ft.Text):
        super().__init__()
        self.password = password.value

    def build(self):
        return ft.Row(controls=[ft.Text(value=self.password),
                                ft.ElevatedButton(on_click=self.on_click, text="Скопировать", icon=ft.icons.CONTENT_COPY)])

    def on_click(self, e):
        dlg = ft.AlertDialog(title=ft.Text("Пароль скопирован"))
        self.page.dialog = dlg
        self.copy_password()
        dlg.open = True
        self.page.update()

    def copy_password(self):
        copy(self.password)


def main(page: ft.Page):
    page.title = "PasswordKeeper"
    page.window_width = 200
    page.window_height = 200
    page.window_resizable = False

    page.update()

    app = PasswordCopyLine(ft.Text("Тест"))

    page.add(app)


ft.app(target=main)

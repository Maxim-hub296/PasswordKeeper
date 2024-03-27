import flet as ft
from App import PasswordKeeper


def main(page: ft.Page):
    page.title = "PasswordKeeper"
    page.window_width = 443
    page.window_height = 530
    page.window_resizable = False

    page.update()

    app = PasswordKeeper()

    page.add(app)


ft.app(target=main)

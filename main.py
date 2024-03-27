import flet as ft
from App import PasswordKeeper


def main(page: ft.Page):
    page.title = "PasswordKeeper"
    page.window_width = 400
    page.window_height = 450

    page.update()

    app = PasswordKeeper()

    page.add(app)


ft.app(target=main)

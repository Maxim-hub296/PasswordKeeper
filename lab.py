import flet as ft
from dialogs import RegisterDialog


def main(page: ft.Page):
    """

    :param page: служебный параметр (читать документацию flet)
    :return:
    """
    page.title = "PasswordKeeper"  # Название окно
    page.window_width = 443  # Длинна окна
    page.window_height = 530  # Ширина окна
    page.window_resizable = False  # Запрещаем изменять размер

    page.update()  # Что-то служебное (читать документацию flet)

    app = RegisterDialog()  # Экземпляр класса нашего приложения
    page.update()

    page.add(app)  # Добавляем класс на страницу. Что-то служебное (читать документацию flet)


ft.app(target=main)  # Запускаем!

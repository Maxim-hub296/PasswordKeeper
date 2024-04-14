from controls import *


class PasswordKeeper(ft.UserControl):
    def __init__(self):

        super().__init__()
        self.choose = {
            "kirill_low": False,
            "kirill_up": False,
            "latin_low": True,
            "latin_up": False,
            "digits": True,
            "special": False
        }

        self.name = ft.TextField(label="Введите название пароля", width=200)
        self.length = ft.TextField(label="Введите длину пароля", input_filter=ft.NumbersOnlyInputFilter(), width=200,
                                   value="10")
        self.generateButton = GeneratePasswordButton(self.choose, self.name, self.length)
        self.showButton = ShowPasswordButton()
        self.createCodeButton = CreateCodeButton()
        self.delCodeButton = DelCodeButton()
        self.checkBox = SelectSymbols(self.choose)

    def build(self):
        password_button_row = ft.Row(controls=[self.generateButton, self.showButton], alignment=ft.alignment.center)
        code_button_row = ft.Row(controls=[self.createCodeButton, self.delCodeButton], alignment=ft.alignment.center)
        return ft.Column(controls=[password_button_row, code_button_row, self.name, self.length, self.checkBox],
                         alignment=ft.alignment.center)

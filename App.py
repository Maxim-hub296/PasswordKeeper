from controls import *


class PasswordKeeper(ft.UserControl):
    def __init__(self):
        super().__init__()
        choose = {
            "kirill_low": True,
            "kirill_up": False,
            "latin_low": False,
            "latin_up": True,
            "digits": True,
            "special": False
        }

        self.name = ft.TextField(label="Введите название пароля", width=200)
        self.length = ft.TextField(label="Введите длину пароля", input_filter=ft.NumbersOnlyInputFilter(), width=200,
                                   hint_text="по умолчанию 10")

        self.generateButton = GeneratePasswordButton(choose, self.length.value, self.name.value)
        self.showButton = ShowPasswordButton()
        self.createCodeButton = CreateCodeButton()
        self.delCodeButton = DelCodeButton()
        self.checkBox = CheckBox(choose)

    def build(self):
        password_button_row = ft.Row(controls=[self.generateButton, self.showButton], alignment=ft.alignment.center)
        code_button_row = ft.Row(controls=[self.createCodeButton, self.delCodeButton], alignment=ft.alignment.center)
        return ft.Column(controls=[password_button_row, code_button_row, self.name, self.length, self.checkBox],
                         alignment=ft.alignment.center)

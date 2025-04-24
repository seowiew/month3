
import flet as ft
from db import Database

db = Database("expenses.db")


def main(page: ft.Page):
    page.title = "расходы"
    page.bgcolor = ft.colors.PINK_50
    page.theme_mode = ft.ThemeMode.LIGHT

    name_input = ft.TextField(label="описание расхода")
    amount_input = ft.TextField(label="сумма", keyboard_type="number")
    expenses_list = ft.Column(scroll="always", expand=True)
    total_text = ft.Text(str(db.get_total()), size=20, weight="bold", color=ft.colors.BLACK)

    def load_expenses():
        expenses_list.controls.clear()
        for name, amount in db.get_all_expenses():
            color = (
                ft.colors.TEAL_300 if amount <= 100 else
                ft.colors.LIGHT_BLUE_200 if amount <= 1000 else
                ft.colors.PURPLE_300 if amount <= 10000 else
                ft.colors.BLACK
            )
            expenses_list.controls.append(
                ft.Row([
                    ft.Text(name, color=ft.colors.BLACK),
                    ft.Text(f"{amount:.2f}", color=color),
                ])
            )

    def add_expense(e):
        name = name_input.value.strip()
        amount_str = amount_input.value.strip()

        try:
            amount = float(amount_str)
            if amount <= 0:
                raise ValueError
        except ValueError:
            page.add(ft.Text("введите положительное число!", color=ft.colors.RED))
            page.update()
            return

        db.add_expense(name, amount)

        name_input.value = ""
        amount_input.value = ""

        load_expenses()
        total_text.value = f"{db.get_total():.2f}"
        page.update()

    button = ft.ElevatedButton(
        text="добавить расход", on_click=add_expense,
        bgcolor=ft.colors.PINK_300, color=ft.colors.WHITE
    )

    input_row = ft.Row(controls=[name_input, amount_input, button])

    load_expenses()  # показать существующие

    page.add(
        ft.Text("Ваши расходы", size=30, weight=ft.FontWeight.BOLD, color=ft.colors.BLACK),
        input_row,
        ft.Text("Общая сумма расходов:", size=18, weight="bold", color=ft.colors.BLACK),
        total_text,
        expenses_list
    )


ft.app(target=main)
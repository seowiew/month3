
import flet as ft
from db import Database

db = Database("expenses.db")


def main(page: ft.Page):
    page.title = "Расходы"
    page.bgcolor = ft.colors.PINK_50
    page.theme_mode = ft.ThemeMode.LIGHT

    name_input = ft.TextField(label="Описание расхода")
    amount_input = ft.TextField(label="Сумма", keyboard_type="number")
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
                    ft.IconButton(
                        icon=ft.icons.EDIT_OUTLINED,
                        icon_color=ft.colors.BLUE,
                        data=name,
                        on_click=open_edit_modal  # кнопка для редактирования
                    ),
                    ft.IconButton(
                        icon=ft.icons.DELETE,
                        icon_color=ft.colors.RED,
                        data=name,
                        on_click=open_delete_modal
                    )
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
            page.add(ft.Text("Введите положительное число!", color=ft.colors.RED))
            page.update()
            return

        db.add_expense(name, amount)

        name_input.value = ""
        amount_input.value = ""

        load_expenses()
        total_text.value = f"{db.get_total():.2f}"
        page.update()

    def open_delete_modal(e):
        page.data = e.control.data
        page.open(delete_modal)

    def close_delete_modal(e):
        page.close(delete_modal)

    def delete_expense(e):
        db.delete_expense(page.data)
        page.close(delete_modal)

        load_expenses()
        total_text.value = f"{db.get_total():.2f}"
        page.update()

    def open_edit_modal(e):
        name_input.value = e.control.data  # заполняем поле редактирования
        page.open(update_modal)

    def close_edit_modal(e):
        page.close(update_modal)

    button = ft.ElevatedButton(
        text="Добавить расход", on_click=add_expense,
        bgcolor=ft.colors.PINK_300, color=ft.colors.WHITE
    )

    input_row = ft.Row(controls=[name_input, amount_input, button])

    load_expenses()

    delete_modal = ft.AlertDialog(
        modal=True,
        title=ft.Text("Подтвердите удаление"),
        content=ft.Text("Вы действительно хотите удалить этот расход?"),
        actions=[
            ft.ElevatedButton(
                "Удалить",
                on_click=delete_expense,
                bgcolor=ft.Colors.RED,
                color=ft.Colors.WHITE,
            ),
            ft.ElevatedButton("Отменить", on_click=close_delete_modal),
        ],
        actions_alignment=ft.MainAxisAlignment.END,
    )

    update_modal = ft.AlertDialog(
        modal=True,
        title=ft.Text("Редактирование расхода"),
        content=ft.Column(
            controls=[
                name_input,
                amount_input,
            ]
        ),
        actions=[
            ft.ElevatedButton(
                "Сохранить",
                on_click=add_expense,
                bgcolor=ft.Colors.BLUE,
                color=ft.Colors.WHITE,
            ),
            ft.ElevatedButton("Отменить", on_click=close_edit_modal),
        ],
    )

    page.add(
        ft.Text("Ваши расходы", size=30, weight=ft.
                FontWeight.BOLD, color=ft.colors.BLACK),
        input_row,
        ft.Text("Общая сумма расходов:", size=18, weight="bold", color=ft.colors.BLACK),
        total_text,
        expenses_list
    )


ft.app(target=main)
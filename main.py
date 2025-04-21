
import flet as ft

def main(page: ft.Page):
    total_sum = 0

    page.title = "расходы"
    page.bgcolor = ft.colors.PINK_50
    page.theme_mode = ft.ThemeMode.LIGHT

    name_input = ft.TextField(label="описание расхода")
    amount_input = ft.TextField(label="сумма", keyboard_type="number")

    expenses_list = ft.Column(scroll="always", expand=True)

    total_text = ft.Text("0", size=20, weight="bold", color=ft.colors.BLACK)

    def add_expense(e):
        nonlocal total_sum

        name = name_input.value.strip()
        amount_str = amount_input.value.strip()

        try:
            amount = float(amount_str)
            if amount <= 0:
                raise ValueError
        except ValueError:
            error_text = ft.Text("введите положительное число!")
            page.add(error_text)
            page.update()
            return

        if amount <= 100:
            color = ft.colors.TEAL_300
        elif amount <= 1000:
            color = ft.colors.LIGHT_BLUE_200  
        elif amount <= 10000:
            color = ft.colors.PURPLE_300
        else:
            color = ft.colors.BLACK  

        expenses_list.controls.append(
            ft.Row([
                ft.Text(name, color=ft.colors.BLACK),
                ft.Text(f"{amount:.2f}", color=color),
                ft.IconButton(
                    icon=ft.icons.EDIT_OUTLINED,
                    icon_color=ft.colors.BLUE,
                    icon_size=20,
                ),
                ft.IconButton(
                    icon=ft.icons.DELETE_OUTLINED,
                    icon_color=ft.colors.RED,
                    icon_size=20,
                ),
            ])
        )

        total_sum += amount
        total_text.value = f"{total_sum:.2f}"

        name_input.value = ""
        amount_input.value = ""

        page.update()

    button = ft.ElevatedButton(
        text="добавить расход",
        on_click=add_expense,
        bgcolor=ft.colors.PINK_300,
        color=ft.colors.WHITE
    )

    input_row = ft.Row(controls=[name_input, amount_input, button])

    page.add(
        ft.Text("Ваши расходы", size=30, weight=ft.FontWeight.BOLD, color=ft.colors.BLACK),
        input_row,
        ft.Text("Общая сумма расходов:", size=18, weight="bold", color=ft.colors.BLACK),
        total_text,
        expenses_list
    )

ft.app(target=main)
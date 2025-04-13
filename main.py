
import flet as ft

def main(page: ft.Page):
    friends_list = []

    def click_button(e):
        if name_input.value.strip():
            friends_list.append(name_input.value)
            print(friends_list)
            name_input.value = ""
            page.update()

    name_input = ft.TextField(
        label="Введите имя друга",
    )

    button = ft.ElevatedButton(
        text="Сохранить",
        on_click=click_button,
        color=ft.colors.PINK,
        bgcolor=ft.colors.AMBER,
    )

    page.add(name_input, button)

ft.app(target=main)

import flet as ft 

def main(page: ft.Page):
    page.title = "Chat with JASC"
    page.vertical_alignment = ft.MainAxisAlignment.CENTER

    #!Area con el chat
    chat_area = ft.Column(
        scroll="auto",
        expand=True,
        spacing=10,
    )
    
    #!entrada
    input_field = ft.TextField(
        hint_text="Write your message",
        expand=True
    )

    #! Botón de envío
    send_button = ft.ElevatedButton("Send")

    #! Función para el envío de mensajes
    def send_message(e):
        if input_field.value:
            chat_area.controls.append(ft.Text(f"Tú: {input_field.value}"))

            #! Aquí iría la lógica para obtener la respuesta de la IA
            chat_area.controls.append(ft.Text(f"AI: Simulated response"))
            input_field.value = ""
            page.update()

    send_button.on_click = send_message
    
    page.add(
            ft.Column(
            controls=[
                ft.Container(
                    content=chat_area,
                    border=ft.border.all(1, ft.colors.OUTLINE),
                    border_radius=5,
                    padding=10,
                    expand=True,
                ),
                ft.Row(
                    [input_field, send_button],
                    alignment=ft.MainAxisAlignment.SPACE_BETWEEN,
                ),
            ],
            expand=True,
            horizontal_alignment=ft.CrossAxisAlignment.STRETCH,
        ),
    )


ft.app(target=main)

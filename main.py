import flet as ft 
from openai import OpenAI
client = OpenAI(api_key="THE API KEY")
#! REMEMBER TO DELETE API KEY BEFORE PUSHING TO GITHUB!!!!!!!!!


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
            
            completion = client.chat.completions.create(
            model="gpt-4o",
            messages=[
                {"role": "developer", "content": "You should give advices to solve the user's issues without direct answers or solving the question yourself"},
                {"role": "user", "content": "{input_field.value}"}
            ]
            )
            chat_area.controls.append(ft.Text(completion.choices[0].message)) # ai's response
            #! Aquí iría la lógica para obtener la respuesta de la IA
            # chat_area.controls.append(ft.Text(f"AI: Simulated response"))
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

# Flet Hot reload command --> flet run main.py
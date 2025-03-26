import flet as ft 
from openai import OpenAI
import time as time
client = OpenAI(api_key="")
#! REMEMBER TO DELETE API KEY BEFORE PUSHING TO GITHUB!!!!!!!!!



def main(page: ft.Page):
    page.title = "Chat with JASC"
    page.vertical_alignment = ft.MainAxisAlignment.CENTER

    def slowPrint(textField, text):
        for i in range(len(text)):
            textField.value = f"{textField.value}{text[i]}"
            time.sleep(0.005)
            page.update()

    #!Area con el chat
    chat_area = ft.Column(
        scroll="auto",
        expand=True,
        spacing=10,
    )
    
    #!entrada
    input_field = ft.TextField(
        hint_text="Write your message",
        expand=True,
    )

    #! Botón de envío
    send_button = ft.IconButton("Send")

    #! Función para el envío y respuesta de mensajes
    def send_message(e):
        if input_field.value:
            chat_area.controls.append(ft.Text(f"You: {input_field.value}"))
            
            completion = client.chat.completions.create(
            model="gpt-4o",
            messages=[
                {"role": "developer", "content": "You should give advices to solve the user's issues without direct answers or solving the question yourself"},
                {"role": "user", "content": f"{input_field.value}"}
            ]
            )
            chat_area.controls.append(ft.Text(f"JASC: ")) # ai's response
            slowPrint(chat_area.controls[-1],completion.choices[0].message.content)

            # chat_area.controls.append(ft.Text(f"AI: Simulated response"))
            input_field.value = ""
            page.update()

    input_field = ft.TextField(
        hint_text="Write your message",
        expand=True,
        on_submit=send_message
    )
    send_button.on_click = send_message
    
    page.add(
            ft.Column(
            controls=[
                ft.Container(
                    content=chat_area,
                    border=ft.border.all(1, ft.Colors.OUTLINE),
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
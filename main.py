import flet as ft 
from openai import OpenAI
import time as time
import flet_audio as fta
client = OpenAI(api_key="API KEY")
#! REMEMBER TO DELETE API KEY BEFORE PUSHING TO GITHUB!!!!!!!!!



def main(page: ft.Page):
    page.title = "Chat with JASC"
    page.vertical_alignment = ft.MainAxisAlignment.CENTER
    
    background_image = ft.Container(
        ft.Image(
            src="light.png",
            expand=True,
            opacity=0.05,
        ), alignment=ft.alignment.center
    )

    def handle_brightness_change(e):
        print(page.platform_brightness)
        if page.platform_brightness == ft.Brightness.DARK:
            background_image.content.src = "dark.png"
        else:
            background_image.content.src = "light.png"
        page.update()

    page.on_platform_brightness_change = handle_brightness_change

    audio_player = fta.Audio(src="scream.mp3", autoplay=False)

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
    

    full_area = ft.Stack(
        controls=[
            background_image,
            chat_area,
        ]
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
            audio_player.play()
            chat_area.controls.append(ft.Text(f"You: {input_field.value}"))
            page.update()
            
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
        audio_player.pause()
    
    #!entrada
    input_field = ft.TextField(
        hint_text="Write your message",
        expand=True,
        on_submit=send_message
    )
    send_button.on_click = send_message
    handle_brightness_change(None)
    page.add(
        ft.Column(
            controls=[
                ft.Container(
                    content=full_area,
                    border=ft.border.all(1, ft.Colors.OUTLINE),
                    border_radius=5,
                    padding=10,
                    expand=True,
                ),
                # background_image,
                ft.Row(
                    [input_field, send_button],
                    alignment=ft.MainAxisAlignment.SPACE_BETWEEN,
                ),
            ],
            expand=True,
            horizontal_alignment=ft.CrossAxisAlignment.STRETCH,
        ),
        audio_player
    )


ft.app(target=main, assets_dir="assets")

# Flet Hot reload command --> flet run main.py
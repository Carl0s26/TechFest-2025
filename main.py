import flet as ft 
from openai import OpenAI
import time as time
client = OpenAI(api_key="API KEY")
import threading
import json
import os

chat_file = "history.json"
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
        if page.platform_brightness == ft.Brightness.DARK:
            background_image.content.src = "dark.png"
            input_field.border_color = ft.Colors.GREY_600
        else:
            background_image.content.src = "light.png"
            input_field.border_color = ft.Colors.BLACK
        page.update()

    page.on_platform_brightness_change = handle_brightness_change

    def slowPrint(textField, text, callback):
        textField.value = "JASC: "
        for i in range(len(text)):
            textField.value = f"{textField.value}{text[i]}"
            time.sleep(0.005)
            page.update()
        callback()

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
            current_text = input_field.value
            chat_area.controls.append(ft.Text(f"You: {current_text}"))
            page.update()
            input_field.value = ""
            dot1 = ft.Container(width=8, height=8, bgcolor=ft.Colors.GREY, border_radius=4, opacity=0.3)
            dot2 = ft.Container(width=8, height=8, bgcolor=ft.Colors.GREY, border_radius=4, opacity=0.3)
            dot3 = ft.Container(width=8, height=8, bgcolor=ft.Colors.GREY, border_radius=4, opacity=0.3)
            thinking_row = ft.Row([ft.Text("JASC:"), dot1, dot2, dot3], spacing=5)
            chat_area.controls.append(thinking_row)
            page.update()

            stop_typing = False

            def animate_typing():
                step = 0
                while not stop_typing:
                    dot1.opacity = 1.0 if step % 3 == 0 else 0.3
                    dot2.opacity = 1.0 if step % 3 == 1 else 0.3
                    dot3.opacity = 1.0 if step % 3 == 2 else 0.3
                    page.update()
                    step += 1
                    time.sleep(0.3)

            animation_thread = threading.Thread(target=animate_typing, daemon=True)
            animation_thread.start()

            def fetch_response():
                nonlocal stop_typing
                history = [control.value for control in chat_area.controls if isinstance(control, ft.Text)]
                messages = [{"role": "system", "content": "Your name is JASC, a very helpful assistant. You should give advices to solve the user's issues without direct answers or solving the question yourself"}]
                for i, msg in enumerate(history[-10:]):
                    role = "user" if i % 2 == 0 else "assistant"
                    messages.append({"role": role, "content": msg.replace("You: ", "").replace("JASC: ", "")})
                messages.append({"role": "user", "content": current_text})

                completion = client.chat.completions.create(
                    model="gpt-4o",
                    messages=messages
                )

                stop_typing = True
                page.update()
                chat_area.controls.remove(thinking_row)

                ai_response = completion.choices[0].message.content

                chat_area.controls.append(ft.Row([ft.Text("")], wrap=True))
                page.update()

                #! Cuando termina reemplaza por Markdown
                def finalize_markdown():
                    chat_area.controls.pop()
                    chat_area.controls.append(ft.Markdown(f"JASC: {ai_response}"))
                    page.update()

                slowPrint(chat_area.controls[-1].controls[0], ai_response, finalize_markdown)
            
                history = [
                    control.value
                    for control in chat_area.controls
                    if isinstance(control, (ft.Text, ft.Markdown))
                ]

                with open(chat_file, "w") as f:
                    json.dump(history, f, indent=2)

            threading.Thread(target=fetch_response, daemon=True).start()

    #!entrada
    input_field = ft.TextField(
        hint_text="Write your message",
        expand=True,
        on_submit=send_message,
    )
    send_button.on_click = send_message
    handle_brightness_change(None)
    
    if os.path.exists(chat_file):
        with open(chat_file, "r") as f:
            messages = json.load(f)
            for stuff in messages:
                chat_area.controls.append(ft.Markdown(stuff))
                
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
                ft.Row(
                    [input_field, send_button],
                    alignment=ft.MainAxisAlignment.SPACE_BETWEEN,
                ),
            ],
            expand=True,
            horizontal_alignment=ft.CrossAxisAlignment.STRETCH,
        )
    )

ft.app(target=main, assets_dir="assets")

# Flet Hot reload command --> flet run main.py
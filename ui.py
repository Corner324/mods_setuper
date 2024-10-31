from ctypes import alignment
import flet as ft
from installer import check_and_install_mods
import os

# Путь по умолчанию к папке модов
MODS_FOLDER = os.path.join(os.environ['USERPROFILE'], "Zomboid", "mods1")

def main(page: ft.Page):
    page.title = "Zomboid Mod Installer by Corner"
    page.window.width = 450
    page.window.height = 350
    page.bgcolor = ft.colors.BLACK
    page.vertical_alignment = ft.MainAxisAlignment.START

    # Заголовок
    title = ft.Text(
        "Установщик модов Zomboid by Corner",
        color=ft.colors.WHITE,
        size=20,
        weight=ft.FontWeight.BOLD,
        text_align=ft.TextAlign.CENTER  # Указываем выравнивание текста
    )

    # Путь к папке модов
    mods_folder = ft.Text(
        f"Папка с модами:\n{MODS_FOLDER}",
        color=ft.colors.GREY,
        size=12,
        text_align=ft.TextAlign.CENTER
    )

    # Поле статуса
    status_text = ft.Text(value="")
    
    # Прогресс-бар
    progress = ft.ProgressBar(value=0, width=400, bar_height=5, opacity=0.9, border_radius=10)
    server_status = ft.Text(value="", color=ft.colors.GREY, size=12, text_align=ft.TextAlign.CENTER)
    

    # Кнопка установки
    install_button = ft.ElevatedButton(
        text="Установить сборку",
        icon=ft.icons.DOWNLOAD,
        scale=1.2,
        color=ft.colors.GREEN_500,
        on_click=lambda e: install_mods(status_text, progress, page, install_button, server_status)
    )

    # Добавляем элементы на страницу
    page.add(title,
             ft.Divider(height=20, color=ft.colors.BACKGROUND),
             mods_folder,
             install_button,
             server_status,
             ft.Divider(height=30, color=ft.colors.BACKGROUND),
             status_text,
             progress)
    page.horizontal_alignment = "center"
    page.vertical_alignment = ft.MainAxisAlignment.CENTER
    page.window.center()
    page.horizontal_alignment = "center"
    page.vertical_alignment = "center"
    page.window.resizable = True
    page.bgcolor=ft.colors.BACKGROUND,
    page.update()

def install_mods(status_text, progress, page, install_button, server_status):
    progress.value = 0

    server_status.value = "Соединение с сервером установлено\nВерсия сборки - 1.0.0"
    try:
        check_and_install_mods(MODS_FOLDER, progress, status_text, page)
        install_button.disabled = True
    except Exception as ex:
            install_button.text = "Повторить установку"
            server_status.value = ex
            server_status.text_align=ft.TextAlign.CENTER
            server_status.color = ft.colors.RED_200
            install_button.icon = ft.icons.REPLAY_OUTLINED
    else:
        install_button.text = "Снести Windows"
        install_button.icon = ft.icons.WINDOW
        install_button.color = ft.colors.BACKGROUND
        
    page.update()
        


if __name__ == "__main__":
    ft.app(target=main)

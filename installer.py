import os
from turtle import st
import requests
import zipfile
import io
import flet as ft

# Ссылка на релиз GitHub
GITHUB_RELEASE_URL = "https://api.github.com/repos/Corner324/mods_setuper/releases/latest"

def get_github_mods():
    response = requests.get(GITHUB_RELEASE_URL)
    if response.status_code == 200:
        assets = response.json().get("assets", [])
        mods = {asset["name"]: asset["browser_download_url"] for asset in assets if asset["name"].endswith(".zip")}
        return mods
    else:
        raise Exception("Не удалось получить список модов с GitHub")

def install_mod(mod_name, url, mods_folder, page, status_text):
    try:
        status_text.value = f"Устанавливаем {mod_name.split(".")[0]}"
        page.update()
        response = requests.get(url)
        if response.status_code == 200:
            mod_path = os.path.join(mods_folder, mod_name)
            with zipfile.ZipFile(io.BytesIO(response.content)) as zip_ref:
                zip_ref.extractall(mod_path)
                os.rename(mod_path, mod_path.replace(".zip","")) # TODO: Не все переименовывает, скачивает опять
        else:
            status_text.value = f"Не удалось загрузить мод {mod_name}."
    except FileExistsError as fee:
        status_text.value = f"Мод {mod_name.split(".")[0]} уже установлен"


def check_and_install_mods(mods_folder, progress, status_text, page):
    mods_to_install = get_github_mods()
    installed_mods = os.listdir(mods_folder)
    results = []

    for mod_name, url in mods_to_install.items():
        if mod_name.split(".")[0] not in installed_mods:
            results.append(install_mod(mod_name, url, mods_folder, page, status_text))
            status_text.value = f"Мод {mod_name.split(".")[0]} установлен"
            progress.value = progress.value + (1 / len(mods_to_install.keys()))
            page.update()
        else:
            status_text.value = f"Мод {mod_name.split(".")[0]} уже установлен"
            page.update()
                
    status_text.value = f"Установка успешно завершена!"
    progress.value = 1
    progress.color = ft.colors.GREEN_100
    status_text.color = ft.colors.GREEN_500
    status_text.size = 24
    page.update()

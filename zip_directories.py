import os
import zipfile

def zip_directories_in_folder(folder_path):
    # Проверяем, существует ли указанная директория
    if not os.path.isdir(folder_path):
        print(f"Директория '{folder_path}' не найдена.")
        return

    # Обходим все элементы в указанной директории
    for item in os.listdir(folder_path):
        item_path = os.path.join(folder_path, item)

        # Если элемент является директорией, создаем для него архив
        if os.path.isdir(item_path):
            zip_name = f"{item}.zip"
            zip_path = os.path.join(folder_path, zip_name)

            # Создаем ZIP-архив
            with zipfile.ZipFile(zip_path, 'w', zipfile.ZIP_DEFLATED) as zipf:
                for root, dirs, files in os.walk(item_path):
                    for file in files:
                        file_path = os.path.join(root, file)
                        arcname = os.path.relpath(file_path, start=item_path)
                        zipf.write(file_path, arcname)

            print(f"Папка '{item}' упакована в архив '{zip_name}'")

# Укажите путь к директории, где находятся папки для архивации
folder_path = 'C:/Users/Corner/Zomboid/mods'
zip_directories_in_folder(folder_path)

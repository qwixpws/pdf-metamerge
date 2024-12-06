import os
import shutil
import glob

# Пути к файлам
names_file = "./pdfsorter/names.txt"  # Файл со списком имён
pdf_folder = "./pdfsorter/pdfs/"  # Папка с PDF-файлами
output_folder = "./pdfsorter/output/"  # Папка, куда будут созданы папки с именами

# Создаём выходную папку, если она не существует
os.makedirs(output_folder, exist_ok=True)

# Читаем список имён из файла
with open(names_file, "r", encoding="utf-8") as file:
    names = [line.strip() for line in file]

# Проходим по именам
for name in names:
    # Создаём папку для имени
    name_folder = os.path.join(output_folder, name)
    os.makedirs(name_folder, exist_ok=True)

    # Ищем PDF-файлы, содержащие имя (ФИО) в названии
    matching_files = glob.glob(os.path.join(pdf_folder, f"*{name}*.pdf"))

    if matching_files:
        for pdf_path in matching_files:
            # Копируем каждый подходящий PDF в папку
            shutil.copy(pdf_path, name_folder)
    else:
        # Если файл не найден, выводим сообщение
        print(f"Не найден файл для: {name}")

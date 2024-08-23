import tkinter as tk
from tkinter import messagebox
import os
import shutil
import ctypes
import platform
import psutil

class App:
    def __init__(self, root):
        self.root = root
        self.root.title("Secure App")
        self.root.geometry('800x600')
        self.password = "2914"
        self.desktop_path = os.path.join(os.path.expanduser("~"), "Desktop")
        self.file_prefix = "Kill"
        self.restart_clicks = 0

        self.show_login_screen()

    def show_login_screen(self):
        self.clear_frame()
        self.root.configure(bg="#1c1c1c")

        self.label = tk.Label(self.root, text="Enter Password", fg="white", bg="#1c1c1c", font=("Helvetica", 36, 'bold'))
        self.label.pack(pady=40)

        self.password_entry = tk.Entry(self.root, show="*", font=("Helvetica", 24), width=15)
        self.password_entry.pack(pady=20)
        self.password_entry.bind('<Return>', self.check_password)

        self.submit_button = tk.Button(self.root, text="Submit", command=self.check_password, bg='#4CAF50', fg='white', font=("Helvetica", 24, 'bold'), relief='flat', overrelief='raised')
        self.submit_button.pack(pady=20)

    def check_password(self, event=None):
        if self.password_entry.get() == self.password:
            self.show_lobby()
        else:
            messagebox.showerror("Error", "Incorrect Password")

    def show_lobby(self):
        self.clear_frame()
        self.create_buttons()

    def create_buttons(self):
        self.create_file_button = tk.Button(self.root, text="Появление файлов", command=self.create_files, bg='#4CAF50', fg='white', font=("Helvetica", 24), relief='flat', overrelief='raised')
        self.create_file_button.pack(pady=10, padx=20, fill='x')

        self.close_apps_button = tk.Button(self.root, text="Закрытие всех приложений", command=self.close_apps, bg='#2196F3', fg='white', font=("Helvetica", 24), relief='flat', overrelief='raised')
        self.close_apps_button.pack(pady=10, padx=20, fill='x')

        self.clean_folders_button = tk.Button(self.root, text="Очистка папок", command=self.clean_folders, bg='#FFC107', fg='white', font=("Helvetica", 24), relief='flat', overrelief='raised')
        self.clean_folders_button.pack(pady=10, padx=20, fill='x')

        self.restart_button = tk.Button(self.root, text="Перезагрузить компьютер", command=self.restart_computer, bg='#F44336', fg='white', font=("Helvetica", 24), relief='flat', overrelief='raised')
        self.restart_button.pack(pady=10, padx=20, fill='x')

    def create_files(self):
        try:
            for i in range(100):  # Создает 100 папок
                folder_name = os.path.join(self.desktop_path, f"{self.file_prefix}_{i}")
                os.makedirs(folder_name, exist_ok=True)
            messagebox.showinfo("Info", "Файлы созданы на рабочем столе")
        except Exception as e:
            messagebox.showerror("Error", f"Ошибка при создании файлов: {e}")

    def close_apps(self):
        try:
            # Закрывает все приложения
            for proc in psutil.process_iter(['pid', 'name']):
                try:
                    if proc.info['name'] != 'explorer.exe':  # Не закрывать проводник
                        proc.kill()
                except (psutil.NoSuchProcess, psutil.AccessDenied, psutil.ZombieProcess):
                    pass
            messagebox.showinfo("Info", "Все приложения закрыты")
        except Exception as e:
            messagebox.showerror("Error", f"Ошибка при закрытии приложений: {e}")

    def clean_folders(self):
        try:
            # Удаляет только папки, созданные в этом приложении
            for item in os.listdir(self.desktop_path):
                item_path = os.path.join(self.desktop_path, item)
                if os.path.isdir(item_path) and item.startswith(self.file_prefix):
                    shutil.rmtree(item_path)
            messagebox.showinfo("Info", "Папки на рабочем столе очищены")
        except Exception as e:
            messagebox.showerror("Error", f"Ошибка при очистке папок: {e}")

    def restart_computer(self):
        try:
            self.restart_clicks += 1
            if self.restart_clicks >= 3:
                messagebox.showinfo("Info", "Перезагрузка компьютера...")
                self.restart_clicks = 0
                if platform.system() == "Windows":
                    ctypes.windll.kernel32.RebootSystem(0)
                elif platform.system() == "Linux":
                    os.system("sudo reboot")
                elif platform.system() == "Darwin":
                    os.system("sudo reboot")
                else:
                    messagebox.showerror("Error", "Операционная система не поддерживается для перезагрузки")
            else:
                messagebox.showinfo("Info", f"Нажмите кнопку еще {3 - self.restart_clicks} раз(а) для перезагрузки")
        except Exception as e:
            messagebox.showerror("Error", f"Ошибка при перезагрузке: {e}")

    def clear_frame(self):
        for widget in self.root.winfo_children():
            widget.destroy()

if __name__ == "__main__":
    root = tk.Tk()
    app = App(root)
    root.mainloop()

import tkinter as tk
from tkinter import simpledialog, messagebox, scrolledtext, ttk
from datetime import datetime
import requests
import pytz

# OpenSky Network API endpoint для получения данных о самолетах
OPENSKY_API_URL = "https://opensky-network.org/api/states/all"

# OpenWeatherMap API для получения текущей погоды (Замените 'YOUR_API_KEY' на ваш ключ API)
WEATHER_API_URL = "http://api.openweathermap.org/data/2.5/weather"
WEATHER_API_KEY = 'YOUR_API_KEY'

# NewsAPI для получения текущих новостей (Замените 'YOUR_API_KEY' на ваш ключ API)
NEWS_API_URL = "https://newsapi.org/v2/top-headlines"
NEWS_API_KEY = 'YOUR_API_KEY'

class App:
    def __init__(self, root):
        self.root = root
        self.root.title("Hacker Dashboard")
        self.root.geometry('1200x800')
        self.root.configure(bg="#000000")

        self.ask_password()

    def ask_password(self):
        password = simpledialog.askstring("Пароль", "Введите пароль:", show='*')
        if password == '2914':
            self.show_main_interface()
        else:
            messagebox.showerror("Ошибка", "Неверный пароль!")
            self.root.destroy()

    def show_main_interface(self):
        self.clear_frame()

        title_label = tk.Label(self.root, text="Hacker Dashboard", font=("Courier", 24, 'bold'), bg="#000000", fg="#00FF00")
        title_label.pack(pady=20)

        frame = tk.Frame(self.root, bg="#000000")
        frame.pack(pady=20)

        flights_button = tk.Button(frame, text="Посмотреть полеты", command=self.show_flight_data, bg='#000000', fg='#00FF00', font=("Courier", 16, 'bold'), relief="flat")
        flights_button.grid(row=0, column=0, padx=10, pady=10)

        time_button = tk.Button(frame, text="Посмотреть время", command=self.show_time_data, bg='#000000', fg='#00FF00', font=("Courier", 16, 'bold'), relief="flat")
        time_button.grid(row=0, column=1, padx=10, pady=10)

        weather_button = tk.Button(frame, text="Посмотреть погоду", command=self.show_weather_data, bg='#000000', fg='#00FF00', font=("Courier", 16, 'bold'), relief="flat")
        weather_button.grid(row=0, column=2, padx=10, pady=10)

        news_button = tk.Button(frame, text="Посмотреть новости", command=self.show_news_data, bg='#000000', fg='#00FF00', font=("Courier", 16, 'bold'), relief="flat")
        news_button.grid(row=0, column=3, padx=10, pady=10)

        calculator_button = tk.Button(frame, text="Калькулятор", command=self.show_calculator, bg='#000000', fg='#00FF00', font=("Courier", 16, 'bold'), relief="flat")
        calculator_button.grid(row=0, column=4, padx=10, pady=10)

        self.text_area = scrolledtext.ScrolledText(self.root, wrap=tk.WORD, font=("Courier", 14), bg="#000000", fg="#00FF00")
        self.text_area.pack(padx=10, pady=10, expand=True, fill=tk.BOTH)

    def show_flight_data(self):
        self.text_area.delete("1.0", tk.END)
        self.text_area.insert(tk.END, "Загрузка данных о полетах...\n")
        self.root.update_idletasks()

        try:
            response = requests.get(OPENSKY_API_URL)
            response.raise_for_status()
            data = response.json()

            self.display_flight_data(data)
        except requests.RequestException as e:
            messagebox.showerror("Ошибка", f"Не удалось получить данные: {e}")

    def display_flight_data(self, data):
        self.text_area.delete("1.0", tk.END)

        if data and "states" in data:
            flights = data["states"]
            if flights:
                for flight in flights:
                    flight_info = (
                        f"Рейс: {flight[1]}\n"
                        f"Откуда: {flight[2] if flight[2] else 'Неизвестно'}, Куда: {flight[3] if flight[3] else 'Неизвестно'}\n"
                        f"Лат: {flight[6]}, Дол: {flight[5]}, Высота: {flight[7]} м\n"
                        f"Скорость: {flight[9]} м/с, Направление: {flight[10]}°\n"
                        f"--------------------------------------------\n"
                    )
                    self.text_area.insert(tk.END, flight_info)
            else:
                self.text_area.insert(tk.END, "Нет данных о полетах.\n")
        else:
            self.text_area.insert(tk.END, "Нет данных о полетах.\n")

    def show_time_data(self):
        self.text_area.delete("1.0", tk.END)
        self.text_area.insert(tk.END, "Загрузка данных о времени...\n")
        self.root.update_idletasks()

        try:
            timezones = pytz.all_timezones
            for tz in timezones:
                now = datetime.now(pytz.timezone(tz))
                time_info = f"Время в {tz}: {now.strftime('%Y-%m-%d %H:%M:%S')}\n"
                self.text_area.insert(tk.END, time_info)
        except Exception as e:
            messagebox.showerror("Ошибка", f"Не удалось получить данные о времени: {e}")

    def show_weather_data(self):
        self.text_area.delete("1.0", tk.END)
        city = simpledialog.askstring("Город", "Введите название города:")
        if city:
            self.text_area.insert(tk.END, f"Загрузка данных о погоде в {city}...\n")
            self.root.update_idletasks()
            try:
                params = {'q': city, 'appid': WEATHER_API_KEY, 'units': 'metric', 'lang': 'ru'}
                response = requests.get(WEATHER_API_URL, params=params)
                response.raise_for_status()
                data = response.json()

                weather_info = (
                    f"Погода в {city}:\n"
                    f"Температура: {data['main']['temp']}°C\n"
                    f"Ощущается как: {data['main']['feels_like']}°C\n"
                    f"Давление: {data['main']['pressure']} гПа\n"
                    f"Влажность: {data['main']['humidity']}%\n"
                    f"Описание: {data['weather'][0]['description']}\n"
                    f"--------------------------------------------\n"
                )
                self.text_area.insert(tk.END, weather_info)
            except requests.RequestException as e:
                messagebox.showerror("Ошибка", f"Не удалось получить данные о погоде: {e}")

    def show_news_data(self):
        self.text_area.delete("1.0", tk.END)
        self.text_area.insert(tk.END, "Загрузка данных о новостях...\n")
        self.root.update_idletasks()

        try:
            params = {'country': 'ru', 'apiKey': NEWS_API_KEY}
            response = requests.get(NEWS_API_URL, params=params)
            response.raise_for_status()
            data = response.json()

            self.display_news_data(data)
        except requests.RequestException as e:
            messagebox.showerror("Ошибка", f"Не удалось получить данные о новостях: {e}")

    def display_news_data(self, data):
        self.text_area.delete("1.0", tk.END)

        if data and "articles" in data:
            articles = data["articles"]
            if articles:
                for article in articles:
                    news_info = (
                        f"Заголовок: {article['title']}\n"
                        f"Источник: {article['source']['name']}\n"
                        f"Описание: {article['description']}\n"
                        f"URL: {article['url']}\n"
                        f"--------------------------------------------\n"
                    )
                    self.text_area.insert(tk.END, news_info)
            else:
                self.text_area.insert(tk.END, "Нет данных о новостях.\n")
        else:
            self.text_area.insert(tk.END, "Нет данных о новостях.\n")

    def show_calculator(self):
        self.text_area.delete("1.0", tk.END)
        self.text_area.insert(tk.END, "Калькулятор\n")

        calc_frame = tk.Frame(self.root, bg="#000000")
        calc_frame.pack(pady=10)

        self.calc_entry = tk.Entry(calc_frame, width=30, font=("Courier", 16), bg="#000000", fg="#00FF00", insertbackground="#00FF00")
        self.calc_entry.grid(row=0, column=0, columnspan=4)

        buttons = [
            ('7', 1, 0), ('8', 1, 1), ('9', 1, 2), ('/', 1, 3),
            ('4', 2, 0), ('5', 2, 1), ('6', 2, 2), ('*', 2, 3),
            ('1', 3, 0), ('2', 3, 1), ('3', 3, 2), ('-', 3, 3),
            ('0', 4, 0), ('.', 4, 1), ('+', 4, 2), ('=', 4, 3)
        ]

        for (text, row, col) in buttons:
            button = tk.Button(calc_frame, text=text, command=lambda t=text: self.on_calc_button_click(t), bg='#000000', fg='#00FF00', font=("Courier", 16), relief="flat")
            button.grid(row=row, column=col, padx=5, pady=5)

    def on_calc_button_click(self, char):
        if char == '=':
            try:
                result = eval(self.calc_entry.get())
                self.calc_entry.delete(0, tk.END)
                self.calc_entry.insert(tk.END, str(result))
            except Exception as e:
                self.calc_entry.delete(0, tk.END)
                self.calc_entry.insert(tk.END, "Error")
        else:
            self.calc_entry.insert(tk.END, char)

    def clear_frame(self):
        for widget in self.root.winfo_children():
            widget.destroy()

if __name__ == "__main__":
    root = tk.Tk()
    app = App(root)
    root.mainloop()

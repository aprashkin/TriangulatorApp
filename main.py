import tkinter as tk
from app import App

if __name__ == "__main__":
    root = tk.Tk()  # Создаем главное окно
    app = App(root)  # Инициализируем приложение
    root.mainloop()  # Запускаем главный цикл обработки событий
import tkinter as tk
from tkinter import messagebox
from towers import Tower
from devices import Devices
from triangulator import triangulate_func


class App:
    def __init__(self, root):
        self.root = root
        self.root.title("Triangulation App")  # Устанавливаем заголовок окна
        self.canvas_size = 600  # Размер холста
        self.scale = self.canvas_size / 100  # Масштаб
        self.towers = [
            Tower(20, 30, 30),
            Tower(70, 40, 40),
            Tower(50, 80, 35)
        ]  # Список башен
        self.device = Devices(50, 50)  # Устройство
        self.dragging_item = None  # Перетаскиваемый элемент
        self.init_ui()  # Инициализация пользовательского интерфейса

    def init_ui(self):
        # Создаем холст и привязываем обработчики событий мыши
        self.canvas = tk.Canvas(self.root, width=self.canvas_size, height=self.canvas_size, bg="white")
        self.canvas.grid(row=0, column=0, columnspan=4)
        self.canvas.bind("<ButtonPress-1>", self.on_mouse_down)
        self.canvas.bind("<B1-Motion>", self.on_mouse_drag)
        self.canvas.bind("<ButtonRelease-1>", self.on_mouse_up)

        # Создаем поля ввода для параметров башен
        for i, tower in enumerate(self.towers):
            tk.Label(self.root, text=f"Tower {i + 1} (x, y, r):").grid(row=1 + i, column=0)
            tower.create_entries(self.root, 1 + i)

        # Создаем кнопки для расчета координат и обновления параметров башен
        self.calc_button = tk.Button(self.root, text="GET", command=self.calculate_coordinates)
        self.calc_button.grid(row=4, column=0, columnspan=4)

        self.update_tower_params_button = tk.Button(self.root, text="UPDATE TOWERS", command=self.update_tower_params)
        self.update_tower_params_button.grid(row=5, column=0, columnspan=4)

        self.redraw()  # Перерисовываем холст

    def redraw(self):
        self.canvas.delete("all")  # Очищаем холст
        self.canvas.create_rectangle(0, 0, self.canvas_size, self.canvas_size, outline="black")  # Рисуем границы карты

        # Рисуем башни
        for i, tower in enumerate(self.towers):
            self.draw_circle(tower.x, tower.y, tower.r, f"Tower {i + 1}")

        # Рисуем устройство
        self.draw_device(self.device.x, self.device.y)

    def draw_circle(self, x, y, r, label):
        # Рисуем круг для башни
        x, y, r = x * self.scale, y * self.scale, r * self.scale
        self.canvas.create_oval(x - r, self.canvas_size - (y - r), x + r, self.canvas_size - (y + r), outline="blue",
                                tags="tower")
        self.canvas.create_text(x, self.canvas_size - y, text=label, fill="black")

    def draw_device(self, x, y):
        # Рисуем устройство
        x, y = x * self.scale, y * self.scale
        self.canvas.create_oval(x - 5, self.canvas_size - (y - 5), x + 5, self.canvas_size - (y + 5), fill="red",
                                tags="device", outline="black")
        self.canvas.tag_raise("device")  # Убедиться, что устройство находится на верхнем слое
        self.canvas.create_text(x + 10, self.canvas_size - y, text="Device", fill="black")

    def on_mouse_down(self, event):
        # Обработчик нажатия мыши
        x, y = event.x / self.scale, (self.canvas_size - event.y) / self.scale
        if self.device.is_clicked(x, y):
            self.dragging_item = ('device', None)
            return
        for i, tower in enumerate(self.towers):
            if tower.is_clicked(x, y):
                self.dragging_item = ('tower', i)
                return

    def on_mouse_drag(self, event):
        # Обработчик перетаскивания мыши
        if not self.dragging_item:
            return

        x, y = event.x / self.scale, (self.canvas_size - event.y) / self.scale
        x, y = max(0, min(100, x)), max(0, min(100, y))

        if self.dragging_item[0] == 'tower':
            index = self.dragging_item[1]
            self.towers[index].x, self.towers[index].y = x, y
        elif self.dragging_item[0] == 'device':
            self.device.x, self.device.y = x, y

        self.redraw()

    def on_mouse_up(self, event):
        # Обработчик отпускания мыши
        self.dragging_item = None

    def update_tower_params(self):
        # Обновление параметров башен
        try:
            for tower in self.towers:
                tower.update_params()
            self.redraw()
        except ValueError:
            messagebox.showerror("Error", "Invalid input. Please try again")

    def calculate_coordinates(self):
        # Расчет координат устройства
        try:
            if self.device.is_inside_all_towers(self.towers):
                x_calc, y_calc = triangulate_func(self.towers)
                messagebox.showinfo("RESULT", f"Get coordinates:\nX: {x_calc:.2f}, Y: {y_calc:.2f}")

                # Обновляем координаты устройства
                self.device.x = x_calc
                self.device.y = y_calc

                # Перерисовываем холст
                self.redraw()
            else:
                messagebox.showwarning("ERROR", "Device outside the three towers area")
        except ValueError:
            messagebox.showerror("ERROR", "Incorrect input values")

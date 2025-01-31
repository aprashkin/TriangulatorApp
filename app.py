import tkinter as tk
from tkinter import messagebox, ttk
from towers import Tower
from devices import Devices
from triangulator import triangulate_func

class ScrollableFrame(tk.Frame):
    def __init__(self, container, *args, **kwargs):
        super().__init__(container, *args, **kwargs)
        self.canvas = tk.Canvas(self)
        self.scrollbar = ttk.Scrollbar(self, orient="vertical", command=self.canvas.yview)
        self.scrollable_frame = tk.Frame(self.canvas)

        self.scrollable_frame.bind(
            "<Configure>",
            lambda e: self.canvas.configure(
                scrollregion=self.canvas.bbox("all")
            )
        )

        self.canvas.create_window((0, 0), window=self.scrollable_frame, anchor="nw")
        self.canvas.configure(yscrollcommand=self.scrollbar.set)

        self.canvas.pack(side="left", fill="both", expand=True)
        self.scrollbar.pack(side="right", fill="y")

class App:
    def __init__(self, root):
        self.root = root
        self.root.title("Triangulation App")  # Устанавливаем заголовок окна
        self.canvas_size = 800  # Размер холста
        self.scale = self.canvas_size / 100  # Масштаб
        self.towers = [
            Tower(20, 30, 15),  # Уменьшенный начальный радиус
            Tower(70, 40, 15),  # Уменьшенный начальный радиус
            Tower(50, 80, 15)   # Уменьшенный начальный радиус
        ]  # Список башен
        self.device = Devices(50, 50)  # Устройство
        self.dragging_item = None  # Перетаскиваемый элемент
        self.init_ui()  # Инициализация пользовательского интерфейса

    def init_ui(self):
        # Создаем холст и привязываем обработчики событий мыши
        self.canvas = tk.Canvas(self.root, width=self.canvas_size, height=600, bg="white")
        self.canvas.grid(row=0, column=0, rowspan=2, sticky="nsew")
        self.canvas.bind("<ButtonPress-1>", self.on_mouse_down)
        self.canvas.bind("<B1-Motion>", self.on_mouse_drag)
        self.canvas.bind("<ButtonRelease-1>", self.on_mouse_up)

        # Создаем фрейм для полей ввода и кнопок
        self.control_frame = tk.Frame(self.root, bg="lightgrey")
        self.control_frame.grid(row=0, column=1, rowspan=2, sticky="nsew")

        # Создаем scrollable frame для полей ввода башен
        self.tower_frame = ScrollableFrame(self.control_frame)
        self.tower_frame.grid(row=0, column=0, sticky="nsew")

        # Создаем поля ввода для параметров башен
        self.entry_fields = []
        for i, tower in enumerate(self.towers):
            tk.Label(self.tower_frame.scrollable_frame, text=f"Tower {i + 1} (x, y, r):").grid(row=i, column=0, sticky="w", padx=5, pady=2)
            entry_fields = tower.create_entries(self.tower_frame.scrollable_frame, i)
            self.entry_fields.append(entry_fields)

        # Создаем поля ввода для параметров устройства
        tk.Label(self.control_frame, text=f"Device (x, y):").grid(row=1, column=0, sticky="w", padx=5, pady=2)
        self.device_entry_fields = self.device.create_entries(self.control_frame, 1)

        # Создаем кнопки
        self.update_tower_params_button = tk.Button(self.control_frame, text="UPDATE TOWERS", command=self.update_tower_params)
        self.update_tower_params_button.grid(row=2, column=0, columnspan=4, sticky="w", padx=5, pady=5)

        self.add_tower_button = tk.Button(self.control_frame, text="ADD TOWER", command=self.add_tower)
        self.add_tower_button.grid(row=3, column=0, columnspan=4, sticky="w", padx=5, pady=5)

        # Создаем scrollable frame для progress bars
        self.signal_frame = ScrollableFrame(self.control_frame)
        self.signal_frame.grid(row=4, column=0, columnspan=4, sticky="nsew")

        # Создаем progress bars для уровня сигнала от каждой башни
        self.signal_bars = []
        self.signal_labels = []
        for i in range(len(self.towers)):
            label = tk.Label(self.signal_frame.scrollable_frame, text=f"Signal from Tower {i + 1}:")
            label.grid(row=i, column=0, sticky="w", padx=5, pady=2)
            self.signal_labels.append(label)
            progress_bar = ttk.Progressbar(self.signal_frame.scrollable_frame, orient=tk.HORIZONTAL, length=200, mode='determinate')
            progress_bar.grid(row=i, column=1, columnspan=3, sticky="w", padx=5, pady=2)
            self.signal_bars.append(progress_bar)

        # Настраиваем веса строк и столбцов для правильного растяжения
        self.root.grid_rowconfigure(0, weight=1)
        self.root.grid_columnconfigure(0, weight=1)
        self.root.grid_columnconfigure(1, weight=1)
        self.control_frame.grid_rowconfigure(4, weight=1)

        self.redraw()  # Перерисовываем холст

    def redraw(self):
        self.canvas.delete("all")  # Очищаем холст
        self.canvas.create_rectangle(0, 0, self.canvas_size, 600, outline="black")  # Рисуем границы карты

        # Рисуем башни
        for i, tower in enumerate(self.towers):
            self.draw_tower(tower.x, tower.y, tower.r, f"Tower {i + 1}")

        # Рисуем устройство
        self.draw_device(self.device.x, self.device.y)

        # Рисуем линии между вышками и устройством
        self.draw_lines()

        # Обновляем progress bars сигнала
        self.update_signal_bars()

    def draw_tower(self, x, y, r, label):
        # Рисуем круг для башни
        x, y, r = x * self.scale, y * self.scale, r * self.scale
        self.canvas.create_oval(x - r, 600 - (y - r), x + r, 600 - (y + r), outline="blue",
                                fill="", stipple="gray25", tags="tower")
        self.canvas.create_text(x, 600 - y, text=label, fill="black")

    def draw_device(self, x, y):
        # Рисуем устройство
        x, y = x * self.scale, y * self.scale
        self.canvas.create_oval(x - 5, 600 - (y - 5), x + 5, 600 - (y + 5), fill="red",
                                tags="device", outline="black")
        self.canvas.tag_raise("device")  # Убедиться, что устройство находится на верхнем слое
        self.canvas.create_text(x + 10, 600 - y, text="Device", fill="black")

    def draw_lines(self):
        # Рисуем линии между вышками и устройством
        device_x, device_y = self.device.x * self.scale, self.device.y * self.scale
        closest_towers = self.get_closest_towers()
        for tower in closest_towers:
            tower_x, tower_y = tower.x * self.scale, tower.y * self.scale
            self.canvas.create_line(tower_x, 600 - tower_y, device_x, 600 - device_y,
                                    fill="green")

        # Рисуем линии между вышками
        for i in range(len(closest_towers)):
            for j in range(i + 1, len(closest_towers)):
                tower1 = closest_towers[i]
                tower2 = closest_towers[j]
                tower1_x, tower1_y = tower1.x * self.scale, tower1.y * self.scale
                tower2_x, tower2_y = tower2.x * self.scale, tower2.y * self.scale
                self.canvas.create_line(tower1_x, 600 - tower1_y, tower2_x, 600 - tower2_y,
                                        fill="purple")

    def on_mouse_down(self, event):
        # Обработчик нажатия мыши
        x, y = event.x / self.scale, (600 - event.y) / self.scale
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

        x, y = event.x / self.scale, (600 - event.y) / self.scale
        x, y = max(0, min(100, x)), max(0, min(100, y))

        if self.dragging_item[0] == 'tower':
            index = self.dragging_item[1]
            self.towers[index].x, self.towers[index].y = x, y
            # Update the entry fields for the tower
            self.entry_fields[index][0].delete(0, tk.END)
            self.entry_fields[index][0].insert(0, f"{x:.2f}")
            self.entry_fields[index][1].delete(0, tk.END)
            self.entry_fields[index][1].insert(0, f"{y:.2f}")
        elif self.dragging_item[0] == 'device':
            self.device.x, self.device.y = x, y
            # Update the entry fields for the device
            self.device_entry_fields[0].delete(0, tk.END)
            self.device_entry_fields[0].insert(0, f"{x:.2f}")
            self.device_entry_fields[1].delete(0, tk.END)
            self.device_entry_fields[1].insert(0, f"{y:.2f}")

        self.redraw()

    def on_mouse_up(self, event):
        # Обработчик отпускания мыши
        self.dragging_item = None

    def update_tower_params(self):
        # Обновление параметров башен
        try:
            for i, tower in enumerate(self.towers):
                tower.x = float(self.entry_fields[i][0].get())
                tower.y = float(self.entry_fields[i][1].get())
                tower.r = float(self.entry_fields[i][2].get())
            self.redraw()
        except ValueError:
            messagebox.showerror("Error", "Invalid input. Please try again")

    def add_tower(self):
        # Добавление новой башни
        new_tower = Tower(50, 50, 15)  # Default values with smaller radius
        self.towers.append(new_tower)

        # Update the entry fields for the new tower
        tk.Label(self.tower_frame.scrollable_frame, text=f"Tower {len(self.towers)} (x, y, r):").grid(row=len(self.towers) - 1, column=0, sticky="w", padx=5, pady=2)
        entry_fields = new_tower.create_entries(self.tower_frame.scrollable_frame, len(self.towers) - 1)
        self.entry_fields.append(entry_fields)

        # Update the signal bars for the new tower
        label = tk.Label(self.signal_frame.scrollable_frame, text=f"Signal from Tower {len(self.towers)}:")
        label.grid(row=len(self.towers) - 1, column=0, sticky="w", padx=5, pady=2)
        self.signal_labels.append(label)
        progress_bar = ttk.Progressbar(self.signal_frame.scrollable_frame, orient=tk.HORIZONTAL, length=200, mode='determinate')
        progress_bar.grid(row=len(self.towers) - 1, column=1, columnspan=3, sticky="w", padx=5, pady=2)
        self.signal_bars.append(progress_bar)

        self.redraw()

    def get_closest_towers(self):
        # Получение трех ближайших башен
        distances = [(tower, ((self.device.x - tower.x) ** 2 + (self.device.y - tower.y) ** 2) ** 0.5) for tower in self.towers]
        distances.sort(key=lambda x: x[1])
        return [tower for tower, distance in distances[:3]]

    def calculate_coordinates(self):
        # Расчет координат устройства
        try:
            closest_towers = self.get_closest_towers()
            if self.device.is_inside_all_towers(closest_towers):
                x_calc, y_calc = triangulate_func(closest_towers)
                messagebox.showinfo("RESULT", f"Get coordinates:\nX: {x_calc:.2f}, Y: {y_calc:.2f}")

                # Обновляем координаты устройства
                self.device.x = x_calc
                self.device.y = y_calc

                # Обновляем поля ввода для устройства
                self.device_entry_fields[0].delete(0, tk.END)
                self.device_entry_fields[0].insert(0, f"{x_calc:.2f}")
                self.device_entry_fields[1].delete(0, tk.END)
                self.device_entry_fields[1].insert(0, f"{y_calc:.2f}")

                # Перерисовываем холст
                self.redraw()
            else:
                messagebox.showwarning("ERROR", "Device outside the three towers area")
        except ValueError:
            messagebox.showerror("ERROR", "Incorrect input values")

    def update_signal_bars(self):
        # Обновление progress bars сигнала
        closest_towers = self.get_closest_towers()
        for i, tower in enumerate(closest_towers):
            distance = ((self.device.x - tower.x) ** 2 + (self.device.y - tower.y) ** 2) ** 0.5
            if distance > tower.r:
                signal_strength = 0  # Сигнал равен 0, если устройство вышло из радиуса покрытия
            else:
                signal_strength = 100 * (1 - distance / tower.r)  # Нормализуем сигнал от 0 до 100
            self.signal_bars[i]['value'] = signal_strength
            self.signal_labels[i].config(text=f"Signal from Tower {self.towers.index(tower) + 1}:")

if __name__ == "__main__":
    root = tk.Tk()
    root.geometry("1000x600")  # Устанавливаем размер окна
    app = App(root)
    root.mainloop()

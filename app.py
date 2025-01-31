import tkinter as tk
from tkinter import messagebox, ttk
from towers import Tower
from devices import Devices
from triangulator import triangulate_func
from scrollable_frame import ScrollableFrame

class App:
    def __init__(self, root):
        self.root = root
        self.root.title("Triangulation App")
        self.canvas_size = 800
        self.scale = self.canvas_size / 100
        self.towers = [
            Tower(20, 30, 15),
            Tower(70, 40, 15),
            Tower(50, 80, 15)
        ]
        self.device = Devices(50, 50)
        self.dragging_item = None
        self.init_ui()

    def init_ui(self):
        self.canvas = tk.Canvas(self.root, width=self.canvas_size, height=600, bg="white")
        self.canvas.grid(row=0, column=0, rowspan=2, sticky="nsew")
        self.canvas.bind("<ButtonPress-1>", self.on_mouse_down)
        self.canvas.bind("<B1-Motion>", self.on_mouse_drag)
        self.canvas.bind("<ButtonRelease-1>", self.on_mouse_up)

        self.control_frame = tk.Frame(self.root, bg="lightgrey")
        self.control_frame.grid(row=0, column=1, rowspan=2, sticky="nsew")

        self.tower_frame = ScrollableFrame(self.control_frame)
        self.tower_frame.grid(row=0, column=0, sticky="nsew")

        self.entry_fields = []
        self.create_tower_entries()

        tk.Label(self.control_frame, text="Device (x, y):").grid(row=1, column=0, sticky="w", padx=5, pady=2)
        self.device_entry_fields = self.device.create_entries(self.control_frame, 1)

        self.create_buttons()

        self.signal_frame = ScrollableFrame(self.control_frame)
        self.signal_frame.grid(row=4, column=0, columnspan=4, sticky="nsew")

        self.signal_bars = []
        self.signal_labels = []
        self.create_signal_bars()

        self.root.grid_rowconfigure(0, weight=1)
        self.root.grid_columnconfigure(0, weight=1)
        self.root.grid_columnconfigure(1, weight=1)
        self.control_frame.grid_rowconfigure(4, weight=1)

        self.redraw()

    def create_tower_entries(self):
        for i, tower in enumerate(self.towers):
            tk.Label(self.tower_frame.scrollable_frame, text=f"Tower {i + 1} (x, y, r):").grid(row=i, column=0, sticky="w", padx=5, pady=2)
            entry_fields = tower.create_entries(self.tower_frame.scrollable_frame, i)
            self.entry_fields.append(entry_fields)

    def create_buttons(self):
        self.update_tower_params_button = tk.Button(self.control_frame, text="UPDATE TOWERS", command=self.update_tower_params)
        self.update_tower_params_button.grid(row=2, column=0, columnspan=4, sticky="w", padx=5, pady=5)

        self.add_tower_button = tk.Button(self.control_frame, text="ADD TOWER", command=self.add_tower)
        self.add_tower_button.grid(row=3, column=0, columnspan=4, sticky="w", padx=5, pady=5)

        self.calculate_button = tk.Button(self.control_frame, text="CALCULATE COORDINATES", command=self.calculate_coordinates)
        self.calculate_button.grid(row=5, column=0, columnspan=4, sticky="w", padx=5, pady=5)

    def create_signal_bars(self):
        for i in range(len(self.towers)):
            label = tk.Label(self.signal_frame.scrollable_frame, text=f"Signal from Tower {i + 1}:")
            label.grid(row=i, column=0, sticky="w", padx=5, pady=2)
            self.signal_labels.append(label)
            progress_bar = ttk.Progressbar(self.signal_frame.scrollable_frame, orient=tk.HORIZONTAL, length=200, mode='determinate')
            progress_bar.grid(row=i, column=1, columnspan=3, sticky="w", padx=5, pady=2)
            self.signal_bars.append(progress_bar)

    def redraw(self):
        self.canvas.delete("all")
        self.canvas.create_rectangle(0, 0, self.canvas_size, 600, outline="black")

        for i, tower in enumerate(self.towers):
            self.draw_tower(tower.x, tower.y, tower.r, f"Tower {i + 1}")

        self.draw_device(self.device.x, self.device.y)
        self.draw_lines()
        self.update_signal_bars()

    def draw_tower(self, x, y, r, label):
        x, y, r = x * self.scale, y * self.scale, r * self.scale
        self.canvas.create_oval(x - r, 600 - (y - r), x + r, 600 - (y + r), outline="blue", fill="", stipple="gray25", tags="tower")
        self.canvas.create_text(x, 600 - y, text=label, fill="black")

    def draw_device(self, x, y):
        x, y = x * self.scale, y * self.scale
        self.canvas.create_oval(x - 5, 600 - (y - 5), x + 5, 600 - (y + 5), fill="red", tags="device", outline="black")
        self.canvas.tag_raise("device")
        self.canvas.create_text(x + 10, 600 - y, text="Device", fill="black")

    def draw_lines(self):
        device_x, device_y = self.device.x * self.scale, self.device.y * self.scale
        closest_towers = self.get_closest_towers()
        for tower in closest_towers:
            tower_x, tower_y = tower.x * self.scale, tower.y * self.scale
            distance = ((self.device.x - tower.x) ** 2 + (self.device.y - tower.y) ** 2) ** 0.5
            if distance <= tower.r:
                self.canvas.create_line(tower_x, 600 - tower_y, device_x, 600 - device_y, fill="green")

        for i in range(len(closest_towers)):
            for j in range(i + 1, len(closest_towers)):
                tower1 = closest_towers[i]
                tower2 = closest_towers[j]
                tower1_x, tower1_y = tower1.x * self.scale, tower1.y * self.scale
                tower2_x, tower2_y = tower2.x * self.scale, tower2.y * self.scale
                self.canvas.create_line(tower1_x, 600 - tower1_y, tower2_x, 600 - tower2_y, fill="purple")

    def on_mouse_down(self, event):
        x, y = event.x / self.scale, (600 - event.y) / self.scale
        if self.device.is_clicked(x, y):
            self.dragging_item = ('device', None)
            return
        for i, tower in enumerate(self.towers):
            if tower.is_clicked(x, y):
                self.dragging_item = ('tower', i)
                return

    def on_mouse_drag(self, event):
        if not self.dragging_item:
            return

        x, y = event.x / self.scale, (600 - event.y) / self.scale
        x, y = max(0, min(100, x)), max(0, min(100, y))

        if self.dragging_item[0] == 'tower':
            index = self.dragging_item[1]
            self.update_tower_position(index, x, y)
        elif self.dragging_item[0] == 'device':
            self.update_device_position(x, y)

        self.redraw()

    def on_mouse_up(self, event):
        self.dragging_item = None

    def update_tower_position(self, index, x, y):
        self.towers[index].x, self.towers[index].y = x, y
        self.update_entry_fields(index, x, y)

    def update_device_position(self, x, y):
        self.device.x, self.device.y = x, y
        self.update_device_entry_fields(x, y)

    def update_entry_fields(self, index, x, y):
        self.entry_fields[index][0].delete(0, tk.END)
        self.entry_fields[index][0].insert(0, f"{x:.2f}")
        self.entry_fields[index][1].delete(0, tk.END)
        self.entry_fields[index][1].insert(0, f"{y:.2f}")

    def update_device_entry_fields(self, x, y):
        self.device_entry_fields[0].delete(0, tk.END)
        self.device_entry_fields[0].insert(0, f"{x:.2f}")
        self.device_entry_fields[1].delete(0, tk.END)
        self.device_entry_fields[1].insert(0, f"{y:.2f}")

    def update_tower_params(self):
        try:
            for i, tower in enumerate(self.towers):
                tower.x = float(self.entry_fields[i][0].get())
                tower.y = float(self.entry_fields[i][1].get())
                tower.r = float(self.entry_fields[i][2].get())
            self.redraw()
        except ValueError:
            messagebox.showerror("Error", "Invalid input. Please try again")

    def add_tower(self):
        new_tower = Tower(50, 50, 15)
        self.towers.append(new_tower)
        self.update_tower_entries(new_tower, len(self.towers) - 1)
        self.update_signal_bars_for_new_tower(new_tower, len(self.towers) - 1)
        self.redraw()

    def update_tower_entries(self, new_tower, index):
        tk.Label(self.tower_frame.scrollable_frame, text=f"Tower {index + 1} (x, y, r):").grid(row=index, column=0, sticky="w", padx=5, pady=2)
        entry_fields = new_tower.create_entries(self.tower_frame.scrollable_frame, index)
        self.entry_fields.append(entry_fields)

    def update_signal_bars_for_new_tower(self, new_tower, index):
        label = tk.Label(self.signal_frame.scrollable_frame, text=f"Signal from Tower {index + 1}:")
        label.grid(row=index, column=0, sticky="w", padx=5, pady=2)
        self.signal_labels.append(label)
        progress_bar = ttk.Progressbar(self.signal_frame.scrollable_frame, orient=tk.HORIZONTAL, length=200, mode='determinate')
        progress_bar.grid(row=index, column=1, columnspan=3, sticky="w", padx=5, pady=2)
        self.signal_bars.append(progress_bar)

    def get_closest_towers(self):
        distances = [(tower, ((self.device.x - tower.x) ** 2 + (self.device.y - tower.y) ** 2) ** 0.5) for tower in self.towers]
        distances.sort(key=lambda x: x[1])
        return [tower for tower, distance in distances[:3]]

    def calculate_coordinates(self):
        try:
            closest_towers = self.get_closest_towers()
            coordinates = triangulate_func(closest_towers, self.device.x, self.device.y)
            if coordinates:
                x_calc, y_calc = coordinates
                messagebox.showinfo("RESULT", f"Get coordinates:\nX: {x_calc:.2f}, Y: {y_calc:.2f}")
                self.update_device_position(x_calc, y_calc)
                self.redraw()
            else:
                messagebox.showwarning("ERROR", "Device outside the three towers area")
        except ValueError:
            messagebox.showerror("ERROR", "Incorrect input values")

    def update_signal_bars(self):
        closest_towers = self.get_closest_towers()
        for i, tower in enumerate(closest_towers):
            distance = ((self.device.x - tower.x) ** 2 + (self.device.y - tower.y) ** 2) ** 0.5
            signal_strength = 0 if distance > tower.r else 100 * (1 - distance / tower.r)
            self.signal_bars[i]['value'] = signal_strength
            self.signal_labels[i].config(text=f"Signal from Tower {self.towers.index(tower) + 1}:")

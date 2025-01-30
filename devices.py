import tkinter as tk

class Devices:
    def __init__(self, x, y):
        self.x = x
        self.y = y

    def create_entries(self, root, row):
        x_entry = tk.Entry(root)
        x_entry.grid(row=row, column=1)
        x_entry.insert(0, f"{self.x:.2f}")

        y_entry = tk.Entry(root)
        y_entry.grid(row=row, column=2)
        y_entry.insert(0, f"{self.y:.2f}")

        return [x_entry, y_entry]

    def update_params(self):
        self.x = float(self.entry_fields[0].get())
        self.y = float(self.entry_fields[1].get())

    def is_clicked(self, x, y):
        distance_squared = (self.x - x) ** 2 + (self.y - y) ** 2
        return distance_squared <= 25  # Assuming a click radius of 5 units

    def is_inside_all_towers(self, towers):
        for tower in towers:
            distance_squared = (self.x - tower.x) ** 2 + (self.y - tower.y) ** 2
            if distance_squared > (tower.r ** 2):
                return False
        return True

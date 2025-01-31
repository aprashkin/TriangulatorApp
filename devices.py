import tkinter as tk

class Devices:
    def __init__(self, x, y):
        self.x = x
        self.y = y

    def create_entries(self, parent, row):
        x_entry = tk.Entry(parent)
        x_entry.grid(row=row, column=1, padx=5, pady=2)
        x_entry.insert(0, f"{self.x:.2f}")

        y_entry = tk.Entry(parent)
        y_entry.grid(row=row, column=2, padx=5, pady=2)
        y_entry.insert(0, f"{self.y:.2f}")

        return [x_entry, y_entry]

    def is_clicked(self, x, y):
        return abs(x - self.x) < 5 and abs(y - self.y) < 5

    def is_inside_all_towers(self, towers):
        return all((self.x - tower.x) ** 2 + (self.y - tower.y) ** 2 <= tower.r ** 2 for tower in towers)

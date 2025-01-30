import tkinter as tk


class Tower:
    def __init__(self, x, y, r):
        self.x = x
        self.y = y
        self.r = r

    def create_entries(self, root, row):
        x_entry = tk.Entry(root)
        x_entry.grid(row=row, column=1)
        x_entry.insert(0, f"{self.x:.2f}")

        y_entry = tk.Entry(root)
        y_entry.grid(row=row, column=2)
        y_entry.insert(0, f"{self.y:.2f}")

        r_entry = tk.Entry(root)
        r_entry.grid(row=row, column=3)
        r_entry.insert(0, f"{self.r:.2f}")

        return [x_entry, y_entry, r_entry]

    def update_params(self):
        self.x = float(self.entry_fields[0].get())
        self.y = float(self.entry_fields[1].get())
        self.r = float(self.entry_fields[2].get())

    def is_clicked(self, x, y):
        distance_squared = (self.x - x) ** 2 + (self.y - y) ** 2
        return distance_squared <= (self.r ** 2)

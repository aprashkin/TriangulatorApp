import tkinter as tk

class Tower:
    def __init__(self, x, y, r):
        self.x = x
        self.y = y
        self.r = r

    def create_entries(self, parent, row):
        x_entry = tk.Entry(parent)
        x_entry.grid(row=row, column=1, padx=5, pady=2)
        x_entry.insert(0, f"{self.x:.2f}")

        y_entry = tk.Entry(parent)
        y_entry.grid(row=row, column=2, padx=5, pady=2)
        y_entry.insert(0, f"{self.y:.2f}")

        r_entry = tk.Entry(parent)
        r_entry.grid(row=row, column=3, padx=5, pady=2)
        r_entry.insert(0, f"{self.r:.2f}")

        return [x_entry, y_entry, r_entry]

    def is_clicked(self, x, y):
        return (x - self.x) ** 2 + (y - self.y) ** 2 <= self.r ** 2

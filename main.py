import tkinter as tk
from app import App

if __name__ == "__main__":
    root = tk.Tk()
    root.geometry("1000x600")
    app = App(root)
    root.mainloop()

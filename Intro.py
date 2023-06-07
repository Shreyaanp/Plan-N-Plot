import tkinter as tk
import threading
import os
from PIL import Image, ImageTk
from itertools import cycle

def select_map():
    threading.Thread(target=run_test).start()

def run_test():
    os.system("python map.py")

root = tk.Tk()
root.title("Innovative GUI")
root.geometry("1980x1080")
#use a background image
bg = Image.open("Slide1.png")
bg = bg.resize((1980, 1080))
background_image = ImageTk.PhotoImage(bg)
background_label = tk.Label(root, image=background_image)
background_label.place(x=0, y=0, relwidth=1, relheight=1)


canvas_button = tk.Button(root, text="Select Map", command=select_map, width=15, font=("Arial", 14))
canvas_button.place(relx=0.2, rely=0.85, anchor=tk.E)

gui_button = tk.Button(root, text="Open gui.py", command=lambda: threading.Thread(target=run_gui).start(), width=15, font=("Arial", 14), bg="#fca311", padx=10, pady=10)
gui_button.place(relx=0.5, rely=0.85, anchor=tk.CENTER)

select_map_button = tk.Button(root, text="Open Canvas", command=lambda: threading.Thread(target=run_canvas).start(), width=15, font=("Arial", 14))
select_map_button.place(relx=0.8, rely=0.85, anchor=tk.W)

class LoadingScreen(tk.Toplevel):
    def __init__(self):
        super().__init__()
        self.title("Loading")
        self.geometry("200x150")
        self.configure(bg="#ffffff")

        self.loading_label = tk.Label(self, text="Loading", font=("Arial", 14), bg="#ffffff")
        self.loading_label.pack(pady=20)

        self.animation_frames = cycle(["|", "/", "-", "\\"])
        self.animation_label = tk.Label(self, text="", font=("Arial", 14), bg="#ffffff")
        self.animation_label.pack()
        self.animate()

    def animate(self):
        frame = next(self.animation_frames)
        self.animation_label.config(text=frame)
        self.after(100, self.animate)

def run_canvas():
    loading_screen = LoadingScreen()
    root.after(5000, loading_screen.destroy)  # Simulate a 5-second loading process
    os.system("python Canvas.py")

def run_gui():
    os.system("python GUI.py")

root.mainloop()

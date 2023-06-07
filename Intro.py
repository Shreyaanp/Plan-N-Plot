import tkinter as tk
import os

def select_map():
    os.system("python test.py")

root = tk.Tk()
root.title("Innovative GUI")
root.geometry("1980x1080")

bg_image = tk.PhotoImage(file="background.png")
bg_label = tk.Label(root, image=bg_image)
bg_label.place(x=0, y=0, relwidth=1, relheight=1)

canvas_button = tk.Button(root, text="Open Canvas.py", command=lambda: os.system("python Canvas.py"), width=15, font=("Arial", 14))
canvas_button.place(relx=0.2, rely=0.82, anchor=tk.E)

gui_button = tk.Button(root, text="Open gui.py", command=lambda: os.system("python GUI.py"), width=15, font=("Arial", 14))
gui_button.place(relx=0.5, rely=0.85, anchor=tk.CENTER)

select_map_button = tk.Button(root, text="Select Map", command=select_map, width=15, font=("Arial", 14))
select_map_button.place(relx=0.8, rely=0.85, anchor=tk.W)

root.mainloop()

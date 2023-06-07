import tkinter as tk
import os
import webbrowser

def open_canvas():
    os.system("python Canvas.py")

def open_gui():
    os.system("python GUI.py")

def open_website():
    webbrowser.open("https://github.com/Shreyaanp/EchoSpectra.git")

def button_hover(event):
    event.widget.configure(background="#FFD700")

def button_leave(event):
    event.widget.configure(background="SystemButtonFace")

root = tk.Tk()
root.title("Innovative GUI")
root.geometry("1980x1080")

bg_image = tk.PhotoImage(file="background.png")
bg_label = tk.Label(root, image=bg_image)
bg_label.place(x=0, y=0, relwidth=1, relheight=1)

canvas_button = tk.Button(root, text="Open Canvas.py", command=open_canvas, width=15, font=("Arial", 14))
canvas_button.place(relx=0.2, rely=0.9, anchor=tk.E)
canvas_button.bind("<Enter>", button_hover)
canvas_button.bind("<Leave>", button_leave)

gui_button = tk.Button(root, text="Open gui.py", command=open_gui, width=15, font=("Arial", 14))
gui_button.place(relx=0.5, rely=0.9, anchor=tk.CENTER)
gui_button.bind("<Enter>", button_hover)
gui_button.bind("<Leave>", button_leave)

website_link = tk.Label(root, text="Visit Example Website", fg="blue", cursor="hand2", font=("Arial", 12))
website_link.place(relx=0.8, rely=0.9, anchor=tk.W)
website_link.bind("<Button-1>", lambda e: open_website())

root.mainloop()

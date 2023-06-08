from tkinter import Tk, LabelFrame, Button
from PIL import ImageGrab
import tkintermapview
import subprocess

root = Tk()
root.title('Select Area')
root.geometry("900x700")
root.configure(bg="black")  # Set the background color of the root window to black

def capture_map():
    x = root.winfo_rootx() + my_label.winfo_x() + map_widget.winfo_x()
    y = root.winfo_rooty() + my_label.winfo_y() + map_widget.winfo_y()
    width = map_widget.winfo_width()
    height = map_widget.winfo_height()
    screenshot = ImageGrab.grab(bbox=(x, y, x + width, y + height))
    screenshot.save("background.png")
    root.destroy()  # Close the current window
    subprocess.call(["python", "GUI.py"])  # Open another Python file

my_label = LabelFrame(root)
my_label.pack(pady=20)
my_label.configure(bg="black")  # Set the background color of the label frame to black

map_widget = tkintermapview.TkinterMapView(my_label, width=800, height=600, corner_radius=0)
map_widget.set_position(12.9165, 79.1325)
map_widget.set_zoom(12)
map_widget.pack(side="left")

capture_button = Button(root, text="Capture", command=capture_map, width=15, font=("Arial", 14))
capture_button.pack(side="right", padx=90)

root.mainloop()

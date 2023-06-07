import tkintermapview
from tkinter import *
from PIL import ImageGrab

root = Tk()
root.title('Select Area')
root.geometry("900x700")

def capture_map():
    x = root.winfo_rootx() + my_label.winfo_x() + map_widget.winfo_x()
    y = root.winfo_rooty() + my_label.winfo_y() + map_widget.winfo_y()
    width = map_widget.winfo_width()
    height = map_widget.winfo_height()
    screenshot = ImageGrab.grab(bbox=(x, y, x + width, y + height))
    screenshot.save("background.jpg")

my_label = LabelFrame(root)
my_label.pack(pady=20)

map_widget = tkintermapview.TkinterMapView(my_label, width=800, height=600, corner_radius=0)
map_widget.set_position(12.9165, 79.1325)
map_widget.set_zoom(12)
map_widget.pack(side=LEFT)

capture_button = Button(root, text="Capture", command=capture_map, width=15, font=("Arial", 14))
capture_button.pack(side=LEFT, padx=10)

root.mainloop()

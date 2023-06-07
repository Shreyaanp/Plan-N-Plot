import tkinter as tk
from itertools import cycle

class LoadingScreen(tk.Toplevel):
    def __init__(self):
        super().__init__()
        self.title("Loading")
        self.geometry("200x100")
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

# Example usage
root = tk.Tk()

def start_loading():
    loading_screen = LoadingScreen()
    root.after(5000, loading_screen.destroy)  # Simulate a 5-second loading process

start_button = tk.Button(root, text="Start Loading", command=start_loading)
start_button.pack(pady=50)

root.mainloop()

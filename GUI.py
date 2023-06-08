import tkinter as tk
import os


class UrbanPlannerApp:
    def __init__(self, root):
        self.root = root
        self.root.configure(bg="#14213d")  # Set background color of the root window

        self.left_button_frame = tk.Frame(self.root, bg="#14213d")  # Set background color of the left frame
        self.left_button_frame.pack(side=tk.LEFT, fill=tk.Y, anchor='center')

        self.canvas = tk.Canvas(self.root, width=800, height=600, bg="#14213d")  # Set background color of the canvas
        self.canvas.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)

        self.components = []

        # testing the button
        self.canvas.bind("<ButtonPress-1>", self.start_drag)
        self.canvas.bind("<B1-Motion>", self.drag)

        # Resizing
        self.canvas.bind("<ButtonPress-3>", self.start_resize)
        self.canvas.bind("<B3-Motion>", self.resize)

        # components to the left, add here for more components to the canvas.
        # add label to the left frame
        self.label = tk.Label(self.left_button_frame, text="Components", font=("Arial", 14), bg="#14213d", fg="white")
        self.label.pack(side=tk.TOP, padx=5, pady=5)
        self.create_button("House", self.add_house_component, width=15, height=2, parent_frame=self.left_button_frame)
        self.create_button("Park", self.add_park_component, width=15, height=2, parent_frame=self.left_button_frame)
        self.create_button("Office", self.add_office_component, width=15, height=2, parent_frame=self.left_button_frame)
        self.create_button("School", self.add_school_component, width=15, height=2, parent_frame=self.left_button_frame)
        self.create_button("Save", self.save_components, width=15, height=2, parent_frame=self.left_button_frame)
        self.create_button("Delete", self.delete_component, width=15, height=2, parent_frame=self.left_button_frame)

        self.right_button_frame = tk.Frame(self.root, bg="#14213d")  # Set background color of the right frame
        self.right_button_frame.pack(side=tk.RIGHT, fill=tk.Y, anchor='center')

        # right components
        self.label = tk.Label(self.right_button_frame, text="Tools", font=("Arial", 14), bg="#14213d", fg="white")
        self.label.pack(side=tk.TOP, padx=5, pady=5)
        self.create_button("Pencil", self.use_pencil, width=15, height=2, parent_frame=self.right_button_frame)
        self.create_button("Eraser", self.use_eraser, width=15, height=2, parent_frame=self.right_button_frame)
        self.create_button("Highlighter", self.use_highlighter, width=15, height=2, parent_frame=self.right_button_frame)
        self.create_button("Text Box", self.use_text_box, width=15, height=2, parent_frame=self.right_button_frame)
        self.create_button("Create Prompt", self.run_prompt, width=15, height=2, parent_frame=self.right_button_frame)
        self.create_button("Generate", self.run_generate, width=15, height=2, parent_frame=self.right_button_frame)

        # load an image
        self.background_image = tk.PhotoImage(file="background.png")
        self.canvas.create_image(0, 0, anchor=tk.NW, image=self.background_image)

    def create_button(self, text, command, width=10, height=1, parent_frame=None):
        if parent_frame is None:
            parent_frame = self.root

        button = tk.Button(
            parent_frame,
            text=text,
            command=command,
            width=width,
            height=height,
            relief=tk.RAISED,
            bd=3,
        )
        button.pack(side=tk.TOP, padx=5, pady=5)
        button.bind("<ButtonPress-1>", self.start_drag)
        button.bind("<B1-Motion>", self.drag)
        button.bind("<ButtonPress-3>", self.start_resize)
        button.bind("<B3-Motion>", self.resize)

    def add_component(self, component):
        x1, y1, x2, y2 = component["x1"], component["y1"], component["x2"], component["y2"]
        self.components.append(component)
        self.canvas.create_rectangle(
            x1, y1, x2, y2, fill=component["color"], outline="black"
        )
        self.canvas.create_oval(x2 - 5, y2 - 5, x2 + 5, y2 + 5, fill="red")

    def add_house_component(self):
        component = {"x1": 100, "y1": 100, "x2": 200, "y2": 200, "color": "blue"}
        self.add_component(component)
        self.canvas.create_image(0, 0, anchor=tk.NW, image=self.background_image)

    def add_park_component(self):
        component = {"x1": 300, "y1": 100, "x2": 500, "y2": 300, "color": "green"}
        self.add_component(component)
        self.canvas.create_image(0, 0, anchor=tk.NW, image=self.background_image)

    def add_office_component(self):
        component = {"x1": 100, "y1": 300, "x2": 300, "y2": 400, "color": "yellow"}
        self.add_component(component)
        self.canvas.create_image(0, 0, anchor=tk.NW, image=self.background_image)

    def add_school_component(self):
        component = {"x1": 400, "y1": 400, "x2": 600, "y2": 500, "color": "orange"}
        self.add_component(component)
        self.canvas.create_image(0, 0, anchor=tk.NW, image=self.background_image)

    def start_drag(self, event):
        self.drag_data = {"x": event.x, "y": event.y, "component": None}
        for component in self.components:
            if (
                component["x1"] <= event.x <= component["x2"]
                and component["y1"] <= event.y <= component["y2"]
            ):
                self.drag_data["component"] = component
                break

    def drag(self, event):
        if self.drag_data["component"] is not None:
            dx = event.x - self.drag_data["x"]
            dy = event.y - self.drag_data["y"]
            new_x1 = self.drag_data["component"]["x1"] + dx
            new_y1 = self.drag_data["component"]["y1"] + dy
            new_x2 = self.drag_data["component"]["x2"] + dx
            new_y2 = self.drag_data["component"]["y2"] + dy
            if 0 <= new_x1 <= 800 and 0 <= new_y1 <= 600 and 0 <= new_x2 <= 800 and 0 <= new_y2 <= 600:
                self.drag_data["component"]["x1"] = new_x1
                self.drag_data["component"]["y1"] = new_y1
                self.drag_data["component"]["x2"] = new_x2
                self.drag_data["component"]["y2"] = new_y2
                self.redraw_canvas()

            self.drag_data["x"] = event.x
            self.drag_data["y"] = event.y

    def start_resize(self, event):
        self.resize_data = {"x": event.x, "y": event.y, "component": None}
        for component in self.components:
            if (
                component["x1"] <= event.x <= component["x2"]
                and component["y1"] <= event.y <= component["y2"]
            ):
                self.resize_data["component"] = component
                break

    def resize(self, event):
        if self.resize_data["component"] is not None:
            dx = event.x - self.resize_data["x"]
            dy = event.y - self.resize_data["y"]
            new_x2 = self.resize_data["component"]["x2"] + dx
            new_y2 = self.resize_data["component"]["y2"] + dy

            # Restrict resizing within the canvas boundaries
            if 0 <= new_x2 <= 800 and 0 <= new_y2 <= 600:
                self.resize_data["component"]["x2"] = new_x2
                self.resize_data["component"]["y2"] = new_y2
                self.redraw_canvas()

            self.resize_data["x"] = event.x
            self.resize_data["y"] = event.y

    def use_pencil(self):
        self.canvas.config(cursor="pencil")
        self.canvas.bind("<Button-1>", self.draw_pencil)
        self.canvas.bind("<B1-Motion>", self.draw_pencil)

    def draw_pencil(self, event):
        x, y = event.x, event.y
        self.canvas.create_oval(x - 1, y - 1, x + 1, y + 1, fill="black", outline="black")

    def use_eraser(self):
        self.canvas.config(cursor="circle")
        self.canvas.bind("<Button-1>", self.erase)
        self.canvas.bind("<B1-Motion>", self.erase)

    def erase(self, event):
        x, y = event.x, event.y
        self.canvas.create_oval(x - 5, y - 5, x + 5, y + 5, fill="#14213d", outline="#14213d")

    def use_highlighter(self):
        self.canvas.config(cursor="dotbox")
        self.canvas.bind("<Button-1>", self.highlight)
        self.canvas.bind("<B1-Motion>", self.highlight)

    def highlight(self, event):
        x, y = event.x, event.y
        self.canvas.create_rectangle(x - 3, y - 3, x + 3, y + 3, fill="yellow", outline="yellow")

    def use_text_box(self):
        self.canvas.config(cursor="X_cursor")
        self.canvas.bind("<Button-1>", self.create_text_box)

    def create_text_box(self, event):
        x, y = event.x, event.y
        text = tk.Text(self.canvas, width=10, height=2, bg="#14213d", fg="white", insertbackground="white")
        text_window = self.canvas.create_window(x, y, anchor=tk.NW, window=text)
        text.focus_set()
        self.canvas.bind("<Button-1>", lambda event: None)  # Disable further text box creation

    def run_prompt(self):
        os.system("python prompt.py")

    def redraw_canvas(self):
        self.canvas.delete("all")
        self.canvas.create_image(0, 0, anchor=tk.NW, image=self.background_image)
        for component in self.components:
            x1, y1, x2, y2 = (
                component["x1"],
                component["y1"],
                component["x2"],
                component["y2"],
            )
            self.canvas.create_rectangle(
                x1, y1, x2, y2, fill=component["color"], outline="black"
            )
            self.canvas.create_oval(x2 - 5, y2 - 5, x2 + 5, y2 + 5, fill="red")

    def save_components(self):
        with open("components.txt", "w") as file:
            for component in self.components:
                file.write(
                    f"{component['x1']} {component['y1']} {component['x2']} {component['y2']} {component['color']}\n"
                )

    def delete_component(self):
        if self.components:
            self.components.pop()
            self.redraw_canvas()

    def run_generate(self):
        os.system("python sdiff.py")


root = tk.Tk()
root.title("Urban Planner")

root.columnconfigure(0, weight=1)
root.rowconfigure(0, weight=1)

app = UrbanPlannerApp(root)

root.mainloop()

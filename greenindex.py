import cv2
import numpy as np
import tkinter as tk
from PIL import ImageTk, Image


def calculate_green_index(image):
    # Convert the image to the HSV color space
    hsv_image = cv2.cvtColor(image, cv2.COLOR_BGR2HSV)

    lower_green = np.array([40, 40, 40])   # Adjust these values based on your image
    upper_green = np.array([70, 255, 255])  # Adjust these values based on your image
    mask = cv2.inRange(hsv_image, lower_green, upper_green)

    green_pixels = np.count_nonzero(mask)
    total_pixels = image.shape[0] * image.shape[1]
    green_index = (green_pixels / total_pixels) * 100

    return green_index


def display_images(image1, image2, green_index1, green_index2):
    root = tk.Tk()
    root.title("Image Comparison")

    # Display the first image
    image1 = cv2.cvtColor(image1, cv2.COLOR_BGR2RGB)
    image1 = Image.fromarray(image1)
    image1 = ImageTk.PhotoImage(image1)
    label1 = tk.Label(root, image=image1)
    label1.pack(side="left", padx=10, pady=10)

    # Display the second image
    image2 = cv2.cvtColor(image2, cv2.COLOR_BGR2RGB)
    image2 = Image.fromarray(image2)
    image2 = ImageTk.PhotoImage(image2)
    label2 = tk.Label(root, image=image2)
    label2.pack(side="right", padx=10, pady=10)

    # Display the green index values
    green_index_text = "Green Index:\n\nImage 1: {:.2f}\nImage 2: {:.2f}\n\nDifference: {:.2f}\nPercentage Difference: {:.2f}%".format(
        green_index1, green_index2, green_index1 - green_index2, (green_index1 - green_index2) / green_index1 * 100)
    green_index_label = tk.Label(root, text=green_index_text, font=("Arial", 12), bg="white", padx=10, pady=10)
    green_index_label.pack(pady=10)

    #save the green index values in a text file
    f = open("greenindex.txt", "w")
    f.write(green_index_text)
    f.close()
    

    root.mainloop()


image1 = cv2.imread('dr.sandhya map satellite.png')
image2 = cv2.imread('Output.png')
green_index1 = calculate_green_index(image1)
green_index2 = calculate_green_index(image2)

display_images(image1, image2, green_index1, green_index2)

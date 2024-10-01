import tkinter as tk
from tkinter import filedialog
from PIL import Image, ImageTk
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.backends.backend_agg import FigureCanvasAgg as FigureCanvas
# import matplotlib.pyplot as plt
# from matplotlib.backends.backend_agg import FigureCanvasAgg as FigureCanvas

root = tk.Tk()
root.geometry('800x400')
root.title("API_61147077S")

original_image = None
rotated_image = None

def load_image():
    global original_image  
    file_path = filedialog.askopenfilename()
    if file_path:
        original_image = Image.open(file_path)
        original_image.thumbnail((300, 300))
        photo = ImageTk.PhotoImage(original_image)  
        original_label.config(image=photo)
        original_label.image = photo
        rotate_image()

def rotate_image():
    global rotated_image  
    if original_image:
        rotated_image = original_image.rotate(180)
        save_path = "rotated_image.bmp"
        rotated_image.save(save_path, "BMP") 
        photo = ImageTk.PhotoImage(rotated_image)  
        rotated_label.config(image=photo)
        rotated_label.image = photo

def plot_histogram():
    if original_image:
        gray_image = original_image.convert('L')
        gray_array = np.array(gray_image)  # Convert to NumPy array
        plt.hist(gray_array.ravel(), bins=256, range=(0, 256), density=True, color='gray', alpha=0.7)
        plt.xlabel('Pixel Value')
        plt.ylabel('Normalized Frequency')
        plt.title('Grayscale Histogram')
        plt.grid(True)
        plt.show()


load_button = tk.Button(root, text="讀取", command=load_image)
rotate_button = tk.Button(root, text="選轉影像", command=rotate_image)
histogram_button = tk.Button(root, text="灰階直方圖", command=plot_histogram)

frame_left = tk.Frame(root)
frame_right = tk.Frame(root)

original_label = tk.Label(frame_left)
rotated_label = tk.Label(frame_right)

load_button.grid(row=0, column=0, pady=10)
rotate_button.grid(row=0, column=1, pady=10)
histogram_button.grid(row=0, column=2, pady=10)
frame_left.grid(row=11, column=0, padx=10)
frame_right.grid(row=11, column=1, padx=10)

original_label.pack()
rotated_label.pack()

root.mainloop()  
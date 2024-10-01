import tkinter as tk
from tkinter import filedialog
from PIL import Image, ImageTk
import numpy as np

root = tk.Tk()
root.geometry('800x400')
root.title("API_61147077S")

original_image = None

def load_image():
    global original_image
    file_path = filedialog.askopenfilename()
    if file_path:
        original_image = Image.open(file_path).convert('L')  # Load and convert the image to grayscale
        original_image = original_image.resize((300, 300))
        photo = ImageTk.PhotoImage(original_image)
        original_label.config(image=photo)
        original_label.image = photo

def convolution(image, kernel):
    width, height = image.size
    data = list(image.getdata())
    kernel = np.array(kernel)
    kernel_size = len(kernel)
    
    # Ensure the kernel size is odd for proper centering
    if kernel_size % 2 == 0:
        raise ValueError("Kernel size should be odd for proper centering")

    new_data = []
    kernel_center = kernel_size // 2

    for y in range(height):
        for x in range(width):
            pixel = 0
            for i in range(kernel_size):
                for j in range(kernel_size):
                    image_x = x - kernel_center + j
                    image_y = y - kernel_center + i
                    if 0 <= image_x < width and 0 <= image_y < height:
                        pixel += data[image_y * width + image_x] * kernel[i][j]
            new_data.append(int(pixel))

    new_image = Image.new('L', (width, height))
    new_image.putdata(new_data)
    return new_image

def smooth_image():
    if original_image is not None:
        kernel = np.array([[5, 5, 5, 5, 5],
                            [5, 5, 5, 5, 5],
                            [5, 5, 5, 5, 5],
                            [5, 5, 5, 5, 5],
                            [5, 5, 5, 5, 5]], dtype=float)/125

        smoothed_image = convolution(original_image,kernel)
        show_image(smoothed_image, processed_label)

def edge_detect_image():
    if original_image is not None:
        kernel = np.array([[-2, -2, -2, -2, -2],
                            [-2, -2, -2, -2, -2],
                            [0, 0, 0, 0, 0],
                            [2, 2, 2, 2, 2],
                            [2, 2, 2, 2, 2]])

        edge_image = convolution(original_image, kernel)
        show_image(edge_image, processed_label)

def show_image(image_data, label):
    photo = ImageTk.PhotoImage(image_data)
    label.config(image=photo)
    label.image = photo

load_button = tk.Button(root, text="讀取圖片", command=load_image)
smooth_button = tk.Button(root, text="平滑化", command=smooth_image)
edge_detect_button = tk.Button(root, text="邊緣偵測", command=edge_detect_image)
exit_button = tk.Button(root, text="結束", command=root.quit)
exit_button.grid(row=0, column=3, columnspan=10, padx=10, pady=10)

frame_left = tk.Frame(root)
frame_right = tk.Frame(root)

original_label = tk.Label(frame_left)
processed_label = tk.Label(frame_right)

load_button.grid(row=0, column=0, pady=10)
smooth_button.grid(row=0, column=1, pady=10)
edge_detect_button.grid(row=0, column=2, pady=10)
frame_left.grid(row=1, column=0, padx=10)
frame_right.grid(row=1, column=1, padx=10)
original_label.pack()
processed_label.pack()

root.mainloop()

import tkinter as tk
from tkinter import filedialog
from PIL import Image, ImageTk
import numpy as np
import math
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg

def add_gaussian_noise(image, std_dev):
    img_array = np.array(image.convert('L'))
    height, width = img_array.shape
    noisy_image = np.zeros((height, width), dtype=np.uint8)

    for y in range(height):
        for x in range(width):
            r1, r2 = np.random.rand(), np.random.rand()
            z1 = std_dev * math.cos(2 * math.pi * r2) * math.sqrt(-2 * math.log(r1))
            noisy_pixel = img_array[y, x] + z1
            noisy_pixel = np.clip(noisy_pixel, 0, 255)
            noisy_image[y, x] = noisy_pixel

    return Image.fromarray(noisy_image)

def add_salt_and_pepper_noise(image, percentage):
    img_array = np.array(image)
    height, width, _ = img_array.shape
    noisy_image = img_array.copy()

    num_pixels = int(percentage * height * width)
    salt_pixels = np.random.randint(0, height, num_pixels)
    pepper_pixels = np.random.randint(0, width, num_pixels)

    noisy_image[salt_pixels, pepper_pixels] = 255  # Salt noise
    noisy_image[salt_pixels, pepper_pixels] = 0    # Pepper noise

    return Image.fromarray(noisy_image)

def calculate_histogram(image):
    img_array = np.array(image.convert('L'))
    histogram = np.histogram(img_array.ravel(), bins=256, range=(0, 256), density=True)
    return histogram


def load_image():
    global original_image, rotated_image, histograms_generated
    file_path = filedialog.askopenfilename()
    if file_path:
        original_image = Image.open(file_path)
        original_image.thumbnail((300, 300))
        photo = ImageTk.PhotoImage(original_image)
        original_label.config(image=photo)
        original_label.image = photo
        rotated_image = None
        histograms_generated = False

def rotate_image():
    global rotated_image
    if original_image:
        rotated_image = original_image.rotate(180)
        photo = ImageTk.PhotoImage(rotated_image)
        rotated_label.config(image=photo)
        rotated_label.image = photo

def generate_gaussian_noise_image():
    global original_image, pure_noise_image, noisy_image
    if original_image:
        std_dev = float(std_dev_entry.get())

        pure_noise_array = np.random.normal(0, std_dev, original_image.size)
        pure_noise_array = np.clip(pure_noise_array, 0, 255).astype(np.uint8)
        pure_noise_image = Image.fromarray(pure_noise_array)
        photo = ImageTk.PhotoImage(pure_noise_image)
        pure_noise_label.config(image=photo)
        pure_noise_label.image = photo

        noisy_image = add_gaussian_noise(original_image, std_dev)
        photo = ImageTk.PhotoImage(noisy_image)
        noisy_label.config(image=photo)
        noisy_label.image = photo
def generate_salt_and_pepper_noise_image():
    global original_image, rotated_image, pure_noise_image, noisy_image, histograms_generated
    if original_image:
        percentage = float(percentage_entry.get()) / 100.0

        pure_noise_array = np.random.normal(0, 1, original_image.size)
        pure_noise_array = np.clip(pure_noise_array, 0, 255).astype(np.uint8)
        pure_noise_image = Image.fromarray(pure_noise_array)
        photo = ImageTk.PhotoImage(pure_noise_image)
        pure_noise_label.config(image=photo)
        pure_noise_label.image = photo

        noisy_image = add_salt_and_pepper_noise(original_image, percentage)
        photo = ImageTk.PhotoImage(noisy_image)
        noisy_label.config(image=photo)
        noisy_label.image = photo
        histograms_generated = False

def plot_histograms():
    global original_image, pure_noise_image, noisy_image, histograms_generated
    if noisy_image:
        plot_histogram(original_image, "Original Histogram", 3, 1)
        plot_histogram(pure_noise_image, "Pure Noise Histogram", 3, 2)
        plot_histogram(noisy_image, "Noisy Image Histogram", 3, 3)
        histograms_generated = True

def plot_histogram(image, label, row, col):
    if image:
        img_array = np.array(image.convert('L'))
        histogram = calculate_histogram(image)

        plt.figure(figsize=(4, 3))
        plt.hist(img_array.ravel(), bins=256, range=(0, 256), density=True, color='gray', alpha=0.7)
        plt.xlabel('Pixel Value')
        plt.ylabel('Normalized Frequency')
        plt.title(label)

        canvas = FigureCanvasTkAgg(plt.gcf(), master=frame_histograms)
        canvas.get_tk_widget().grid(row=row, column=col, padx=5, pady=5)

root = tk.Tk()
root.geometry('2000x1200') 
root.title("AIP_61147077s")

original_image = None
rotated_image = None
pure_noise_image = None
noisy_image = None
histograms_generated = False

load_button = tk.Button(root, text="讀取圖片", command=load_image)
rotate_button = tk.Button(root, text="選轉", command=rotate_image)
generate_gaussian_noise_button = tk.Button(root, text="高斯雜訊", command=generate_gaussian_noise_image)
generate_salt_and_pepper_noise_button = tk.Button(root, text="椒鹽雜訊", command=generate_salt_and_pepper_noise_image)  # 新增椒盐噪声按鈕
plot_histogram_button = tk.Button(root, text="繪製直方圖", command=plot_histograms)  # 新增绘制直方图按钮

# std_dev_label = tk.Label(root, text="輸入高斯標準差:")
# std_dev_entry = tk.Entry(root, width=3)
# std_dev_label.grid(row=0, column=5, padx=2, pady=2)
# std_dev_entry.grid(row=0, column=6, padx=2, pady=2)

percentage_label = tk.Label(root, text="輸入椒鹽百分比:")
percentage_entry = tk.Entry(root, width=3)
percentage_label.grid(row=0, column=5, padx=2, pady=2)
percentage_entry.grid(row=0, column=6, padx=2, pady=2)

load_button.grid(row=0, column=0, padx=5, pady=5)
rotate_button.grid(row=0, column=1, padx=5, pady=5)
generate_gaussian_noise_button.grid(row=0, column=2, padx=5, pady=5)
generate_salt_and_pepper_noise_button.grid(row=0, column=3, padx=5, pady=5)  # 放在第
plot_histogram_button.grid(row=0, column=4, padx=5, pady=5)
exit_button = tk.Button(root, text="結束程式", command=root.quit)
exit_button.grid(row=5, column=0, columnspan=10, padx=10, pady=10)

original_label = tk.Label(root)
rotated_label = tk.Label(root)
pure_noise_label = tk.Label(root)
noisy_label = tk.Label(root)

original_label.grid(row=1, column=0, padx=5, pady=5)
rotated_label.grid(row=1, column=1, padx=5, pady=5)
pure_noise_label.grid(row=1, column=2, padx=5, pady=5)
noisy_label.grid(row=1, column=3, padx=5, pady=5)

frame_histograms = tk.Frame(root)
frame_histograms.grid(row=3, column=0, columnspan=4, padx=5, pady=5)

root.mainloop()

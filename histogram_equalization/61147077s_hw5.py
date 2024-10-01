import tkinter as tk
from tkinter import filedialog
from PIL import Image, ImageTk, ImageOps
import numpy as np
import matplotlib.pyplot as plt

# Function to perform histogram equalization
def histogram_equalization(im):
    # Convert image to numpy array
    img_array = np.asarray(im)
    # Flatten the image array and calculate the histogram
    hist, _ = np.histogram(img_array.flatten(), bins=256, range=[0,256])
    # Calculate the cumulative distribution function
    cdf = hist.cumsum()
    cdf_m = np.ma.masked_equal(cdf, 0)  # Mask the zeros since log(0) is undefined
    cdf_m = (cdf_m - cdf_m.min())*255/(cdf_m.max()-cdf_m.min())  # Normalize
    cdf = np.ma.filled(cdf_m, 0).astype('uint8')
    img_eq = cdf[img_array]
    return Image.fromarray(img_eq)

# Function to update the image on the GUI
def update_image_panel(image, img_label):
    tk_image = ImageTk.PhotoImage(image)
    img_label.configure(image=tk_image)
    img_label.image = tk_image  # keep a reference!

def upload_action():
    file_path = filedialog.askopenfilename()
    if file_path:
        im = Image.open(file_path).convert('L')
        update_image_panel(im, image_label)  # Corrected this line
        original_image[0] = im
        # Clear the histogram panels
        hist_label.config(image='')  # Clear the histogram label
        hist_eq_label.config(image='')  # Clear the equalized histogram label


def histogram_action():
    if original_image[0]:
        # Display histogram
        hist = original_image[0].histogram()
        plt.figure(figsize=(5,2))
        plt.bar(range(256), hist, width=1)
        plt.savefig('histogram.png', bbox_inches='tight')
        plt.close()
        hist_image = Image.open('histogram.png')
        update_image_panel(hist_image, hist_label)  # Updated to use two arguments


def equalization_action():
    if original_image[0]:
        # Perform and display histogram equalization
        eq_image = histogram_equalization(original_image[0])
        update_image_panel(eq_image, image_eq_label)  # Updated to use two arguments
        # Display equalized histogram
        hist = eq_image.histogram()
        plt.figure(figsize=(5,2))
        plt.bar(range(256), hist, width=1)
        plt.savefig('histogram_eq.png', bbox_inches='tight')
        plt.close()
        hist_eq_image = Image.open('histogram_eq.png')
        update_image_panel(hist_eq_image, hist_eq_label)  # Updated to use two a
# root = tk.Tk()
# root.geometry('1800x1200')  
# root.title("AIP_61147077s")

app = tk.Tk()
app.geometry('1800x1200')  

app.title('AIP_61147077s')

# Placeholder for the original image
original_image = [None]

# Configure grid layout
app.grid_columnconfigure(0, weight=1)
app.grid_columnconfigure(1, weight=1)

# Buttons
upload_button = tk.Button(app, text='Load Image', command=upload_action)
upload_button.grid(row=0, column=0,padx=10)

histogram_button = tk.Button(app, text='Show Histogram', command=histogram_action)
histogram_button.grid(row=0, column=1,padx=10)

equalize_button = tk.Button(app, text='histogram equalizationm', command=equalization_action,)
equalize_button.grid(row=0, column=2,pady=10)

exit_button = tk.Button(app, text="結束程式", command=app.quit)
exit_button.grid(row=5, column=0, columnspan=10, padx=10, pady=10)
# Image Labels
image_label = tk.Label(app)
image_label.grid(row=1, column=0, sticky='nsew')

image_eq_label = tk.Label(app)
image_eq_label.grid(row=1, column=2, sticky='nsew')

# Histogram Labels
hist_label = tk.Label(app)
hist_label.grid(row=2, column=0, sticky='nsew')

hist_eq_label = tk.Label(app)
hist_eq_label.grid(row=2, column=2, sticky='nsew')

app.mainloop()

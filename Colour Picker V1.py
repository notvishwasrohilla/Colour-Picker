import tkinter as tk
from tkinter import filedialog
from PIL import Image, ImageTk

def open_image():
    # Ask user to select an image file
    file_path = filedialog.askopenfilename(filetypes=[("Image files", "*.png;*.jpg;*.jpeg;*.bmp")])
    if not file_path:
        return

    global img, photo_img, canvas_image
    img = Image.open(file_path)
    photo_img = ImageTk.PhotoImage(img)

    canvas.config(width=photo_img.width(), height=photo_img.height())
    canvas_image = canvas.create_image(0, 0, image=photo_img, anchor="nw")

def get_color(event):
    if img:
        x, y = event.x, event.y
        try:
            r, g, b = img.getpixel((x, y))
            hex_color = f'#{r:02x}{g:02x}{b:02x}'
            color_label.config(text=f"RGB: ({r}, {g}, {b}) | HEX: {hex_color}", bg=hex_color)
        except IndexError:
            color_label.config(text="Clicked outside image")

# GUI setup
window = tk.Tk()
window.title("Image Color Picker")

btn = tk.Button(window, text="Open Image", command=open_image)
btn.pack()

canvas = tk.Canvas(window, cursor="cross")
canvas.pack()
canvas.bind("<Button-1>", get_color)

color_label = tk.Label(window, text="Click on the image to get color", bg="white", font=("Arial", 12))
color_label.pack(fill="x")

img = None
photo_img = None
canvas_image = None

window.mainloop()

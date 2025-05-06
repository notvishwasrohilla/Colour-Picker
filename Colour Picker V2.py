import tkinter as tk
from tkinter import filedialog
from PIL import Image, ImageTk

# GUI setup
window = tk.Tk()
window.title("Image Color Picker")
canvas = tk.Canvas(window, cursor="cross")
canvas.pack()

# Globals
img = None
photo_img = None
canvas_image = None
scale_x = 1
scale_y = 1
corner_positions = ['top-left', 'top-right', 'bottom-right', 'bottom-left']
current_corner = 0

def open_image_on_start():
    file_path = filedialog.askopenfilename(filetypes=[("Image files", "*.png;*.jpg;*.jpeg;*.bmp")])
    if not file_path:
        window.destroy()
        return

    global img, photo_img, canvas_image, scale_x, scale_y

    img = Image.open(file_path)

    screen_w = window.winfo_screenwidth()
    screen_h = window.winfo_screenheight()
    img_w, img_h = img.size

    max_w = int(screen_w * 0.9)
    max_h = int(screen_h * 0.9)

    scale = min(max_w / img_w, max_h / img_h, 1.0)
    new_w = int(img_w * scale)
    new_h = int(img_h * scale)

    scale_x = img_w / new_w
    scale_y = img_h / new_h

    resized_img = img.resize((new_w, new_h), Image.LANCZOS)
    photo_img = ImageTk.PhotoImage(resized_img)

    canvas.config(width=new_w, height=new_h)
    canvas_image = canvas.create_image(0, 0, image=photo_img, anchor="nw")

    window.update_idletasks()
    reposition_colorbox()
    show_color_at(0, 0)

def show_color_at(x, y):
    try:
        r, g, b = img.getpixel((x, y))
        hex_color = f'#{r:02x}{g:02x}{b:02x}'
        color_display.config(bg=hex_color)
        color_label.config(text=f"RGB: {r},{g},{b} | {hex_color}")
    except IndexError:
        color_label.config(text="Out of bounds")

def reposition_colorbox():
    margin = 10
    box_w = info_frame.winfo_width()
    box_h = info_frame.winfo_height()
    canvas_w = canvas.winfo_width()
    canvas_h = canvas.winfo_height()

    positions = {
        'top-left': (margin, margin),
        'top-right': (canvas_w - box_w - margin, margin),
        'bottom-right': (canvas_w - box_w - margin, canvas_h - box_h - margin),
        'bottom-left': (margin, canvas_h - box_h - margin),
    }
    corner = corner_positions[current_corner]
    info_frame.place(x=positions[corner][0], y=positions[corner][1])

def switch_colorbox_position():
    global current_corner
    current_corner = (current_corner + 1) % len(corner_positions)
    reposition_colorbox()

def track_cursor(event):
    if img:
        x = int(event.x * scale_x)
        y = int(event.y * scale_y)
        if 0 <= x < img.width and 0 <= y < img.height:
            show_color_at(x, y)
            avoid_cursor_overlap(event.x, event.y)

def avoid_cursor_overlap(cursor_x, cursor_y):
    buffer = 80  # pixel distance to trigger move
    box_x = info_frame.winfo_x()
    box_y = info_frame.winfo_y()
    box_w = info_frame.winfo_width()
    box_h = info_frame.winfo_height()

    if (box_x - buffer < cursor_x < box_x + box_w + buffer and
        box_y - buffer < cursor_y < box_y + box_h + buffer):
        switch_colorbox_position()

# UI elements (Colorbox)
info_frame = tk.Frame(window, bg="white", bd=1, relief="solid")
info_frame.place(x=20, y=20)

color_display = tk.Label(info_frame, width=6, height=3, bg="white", relief="solid", bd=1)
color_display.pack(side="left", padx=(0, 10))

color_label = tk.Label(info_frame, text="", bg="white", font=("Arial", 10), anchor="w")
color_label.pack(side="left")

# Bind cursor motion to canvas
canvas.bind("<Motion>", track_cursor)

# Load image
window.after(100, open_image_on_start)
window.mainloop()

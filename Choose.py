import tkinter as tk
from PIL import Image, ImageTk

def select_avatar(avatar):
    global sp
    if avatar == "Mr Pacman":
        sp = "spritesheet.png"
    elif avatar == "Mrs Pacman":
        sp = "spritesheet_mspacman.png"
    elif avatar == "Baby Pacman":
        sp = "spritesheet_b.png"
    print("You selected:", avatar)
def close_window():
    root.destroy()

root = tk.Tk()
root.title("Choose Your Pacman")
root.configure(bg="black")
sp = ""
# Function to create a button with a resized image
def create_button_with_resized_image(image_path, avatar):
    image = Image.open(image_path)
    image = image.resize((100, 100), Image.LANCZOS)
    photo = ImageTk.PhotoImage(image)
    button = tk.Button(root, image=photo, command=lambda av=avatar: select_avatar(av))
    button.image = photo
    return button

# Images
images = [
    ("pacmanmr.png", "Mr Pacman"),
    ("mrspacman.png", "Mrs Pacman"),
    ("bpacman.png", "Baby Pacman")
]
# Create buttons with resized images
buttons = []
for img_path, avatar in images:
    button = create_button_with_resized_image(img_path, avatar)
    buttons.append(button)

# Display buttons
for i, button in enumerate(buttons):
    button.grid(row=0, column=i, padx=10, pady=10)

# Add OK button
ok_button = tk.Button(root, text="OK", command=close_window)
ok_button.grid(row=1, columnspan=len(buttons), pady=10)

root.mainloop()

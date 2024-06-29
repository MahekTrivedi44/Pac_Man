from tkinter import *
from tkinter import messagebox  
from PIL import Image, ImageTk
import subprocess
import random
import pygame

SCORE_FILE = "score.txt"

def update_image(count):
    frame = frames[count]
    img = ImageTk.PhotoImage(frame.resize((450, 550)))
    label.config(image=img)
    label.image = img
    count += 1
    if count == len(frames):
        count = 0
    root.after(50, update_image, count)

def start():
    stop_background_audio()
    subprocess.Popen(["python", "run.py"])
    root.destroy()

def about():
    messagebox.showinfo("Pac-Man: Classic Arcade Redux", '''
Choose Your Avatar: Select from Mr. Pac-Man, Mrs. Pac-Man, or
Baby Pac-Man for a personalized gaming experience.

Three Challenging Levels: Navigate through increasingly difficult
mazes, each with its own set of obstacles and ghostly adversaries.

Three Lives: You have three chances to conquer the maze
and achieve the highest score possible.

Strategic Gameplay: Plan your moves carefully to munch on
pellets and avoid ghosts, whose cunning increases with each level.

Timeless Fun: Experience the addictive gameplay of Pac-Man reimagined
for a new generation, offering endless hours of entertainment.''')

def exit_program():
    stop_background_audio()
    root.destroy()

def reset_score():
    with open(SCORE_FILE, "w") as file:
        file.write("0")
    messagebox.showinfo("Score Reset", "Score has been reset to 0.")

def color_change():
    new_color = "#%02x%02x%02x" % (random.randint(200, 255), random.randint(200, 255), random.randint(0, 100))
    p_button.config(fg=new_color)

def stop_background_audio():
    pygame.mixer.music.stop()

pygame.mixer.init()
pygame.mixer.music.load("pacman_beginning.wav")
pygame.mixer.music.play(loops=-1)

root = Tk()
root.geometry("500x600")
root.config(background="#000000")

gifImage = "GnS.gif"
gif = Image.open(gifImage)
frames = []
try:
    while True:
        frames.append(gif.copy().convert('RGBA'))
        gif.seek(len(frames))
except EOFError:
    pass

label = Label(root,bg="#000000")
label.place(x=0, y=0, width=500, height=600)

font_style = ('Goudy Stout', 15)
p_button = Button(root, text="PACMAN", bg="black", fg="yellow", command=color_change, font=('Goudy Stout', 18), borderwidth=0)
p_button.place(x=150, y=20)

start_button = Button(root, text="Start", command=start, font=font_style, bg="white")
start_button.place(x=169, y=200)

about_button = Button(root, text="About", command=about, font=font_style)
about_button.place(x=169, y=270)

exit_button = Button(root, text="Exit", command=exit_program, font=font_style)
exit_button.place(x=185, y=340)

reset_button = Button(root, text="Reset Score To 0?", command=reset_score, font=font_style)
reset_button.place(x=58, y=410)

update_image(0)

root.mainloop()

import os
import numpy as np
from astropy.io import fits
import math
import turtle


# Sets directory to where files are held
os.chdir("C:\\users\\wyatt\\OneDrive\\Desktop\\Research Assistance\\Image Files\\12")

#Ask user for file name
filen = input("What file would you like to read? ")


# Optional line to set directory to a name specific folder (delete if unneeded)
os.chdir("C:\\users\\wyatt\\OneDrive\\Desktop\\Research Assistance\\Image Files\\12\\" + filen)


filename = filen
r_or_b = input("Is this red or blue shifted? ")

if(r_or_b == "b" or r_or_b == "B" or r_or_b == "blue" or r_or_b == "Blue"):
    filen += ".blue.pixel_map.fits"
    filename += ".blue.pixel_map.chopped.fits"
elif(r_or_b == "r" or r_or_b == "R" or r_or_b == "red" or r_or_b == "Red"):
    filen += ".red.pixel_map.fits"
    filename += ".red.pixel_map.chopped.fits"
else:
    filen += "error"


#Open file
file = fits.open(filen)

# Extract Data
new_image = file[0].data
header = file[0].header.copy()




# Mirror vertical axis so that the image look like it will in ds9
new_image = new_image[::-1]

# These are variables to adjust
pixel_size = 4  # Adjust for bigger/smaller pixels (4 is good for a 200x200 array, if the image is not drawing properly, pixels may be too large)
erase_radius = 3  # Radius of cells to erase (1 means 3x3 area, 2 means 5x5 area)

# Initialize Turtle screen
screen = turtle.Screen()
screen.title("Interactive Pixel Map")
rows = len(new_image)
cols = len(new_image[0])
screen.setup(width=cols * pixel_size + 100, height=rows * pixel_size + 100)
screen.tracer(0)

# Turtle for drawing
drawer = turtle.Turtle()
drawer.hideturtle()
drawer.speed(0)
drawer.penup()

# Draw a single cell at specified x and y value
def draw_cell(row_idx, col_idx):
    x = col_idx * pixel_size - (cols * pixel_size) / 2
    y = -(row_idx * pixel_size) + (rows * pixel_size) / 2
    drawer.goto(x, y)
    color = ""
    if new_image[row_idx][col_idx] == 1:
        color = "white"
    else:
        color = "black"
    drawer.fillcolor(color)
    drawer.begin_fill()
    for _ in range(4):
        drawer.forward(pixel_size)
        drawer.right(90)
    drawer.end_fill()

# Draw entire grid
def draw_grid():
    for row_idx, row in enumerate(new_image):
        for col_idx, _ in enumerate(row):
            draw_cell(row_idx, col_idx)
    screen.update()

# Toggle multiple pixels around the clicked cell
def on_click(x, y):
    col_center = int((x + (cols * pixel_size) / 2) // pixel_size)
    row_center = int(((rows * pixel_size) / 2 - y) // pixel_size)

    for dr in range(-erase_radius, erase_radius + 1):
        for dc in range(-erase_radius, erase_radius + 1):
            r = row_center + dr
            c = col_center + dc
            if 0 <= r < rows and 0 <= c < len(new_image[r]):
                new_image[r][c] = 1
                draw_cell(r, c)

    screen.update()

screen.onscreenclick(on_click)

# Draw initial grid (indiviual pixels will be drawn from here)
draw_grid()

# Keep window open
screen.mainloop()


# Mirror vertical axis back for writing out image
new_image = new_image[::-1]





#Overwrite file
new_file = fits.PrimaryHDU()
new_file.data = new_image
new_file.header = header
new_file.writeto(filename, overwrite = True)
print("File written successfully!")
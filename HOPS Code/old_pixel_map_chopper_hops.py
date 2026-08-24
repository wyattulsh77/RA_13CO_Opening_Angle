import os
import numpy as np
from astropy.io import fits
import math


'''
Cuts pixels from either side of a vertical or horizontal line defiend by coordinates
Things to edit:
1. Set directory (line 17)
2. Add directory to line 24 (or remove if unneeded)
'''




directory = "C:\\users\\wyatt\\OneDrive\\Desktop\\Research Assistance\\" 

cl = input("What is the class of the object? ")
if cl == "1" or  cl == "I":
    directory += "ClassI"
elif cl == "0":
    directory += "Class0"
else:
    directory += "Flat"


filen = input("What is the name of the object? ")
directory += "\\" + filen


iso = input("12CO or 13CO? ")
if iso == "12" or iso == "12CO":
    directory += "\\12CO"
elif iso == "13" or iso == "13CO":
    directory += "\\13CO"

os.chdir(directory)

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


# Asks the user how they would like to chop the image
vert_or_hori = input("Is this a horizontal (h), vertical (v), or combination (c) chop? ")

if(vert_or_hori == "h"or vert_or_hori == "c"):
    y_val = int(input("Which y-value would you like to start at? "))
    u_or_d = input("Would you like to remove up (u) or down (d) from y-value? ")
    x_val = 0
    l_or_r = "r"
if(vert_or_hori == "v" or vert_or_hori == "c"):
    x_val = int(input("Which x-value would you like to start at? "))
    l_or_r = input("Would you like to remove left (l) or right (r) from x-value? ")
    if(vert_or_hori == "v"):
        y_val = 0
        u_or_d = "u"


data = file[0].data


# Each one of the blocks removes data depending on what quadrant the user has selected

#remove up and left
if(u_or_d == "u" and l_or_r == "l"):
    for j, y in enumerate(data):
        xpos = data[j]
        for i, x in enumerate(xpos):
            if (j > y_val and i < x_val):
                data[j, i] = 0


#remove up and right
if(u_or_d == "u" and l_or_r == "r"):
    for j, y in enumerate(data):
        xpos = data[j]
        for i, x in enumerate(xpos):
            if (j > y_val and i > x_val):
                data[j, i] = 0


#remove down and left
if(u_or_d == "d" and l_or_r == "l"):
    for j, y in enumerate(data):
        xpos = data[j]
        for i, x in enumerate(xpos):
            if (j < y_val and i < x_val):
                data[j, i] = 0


#remove down and right
if(u_or_d == "d" and l_or_r == "r"):
    for j, y in enumerate(data):
        xpos = data[j]
        for i, x in enumerate(xpos):
            if (j < y_val and i > x_val):
                data[j, i] = 0


#Overwrite file
new_file = fits.PrimaryHDU()
new_file.data = data
new_file.header = file[0].header.copy()
new_file.writeto(filename, overwrite = True)
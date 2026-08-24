import os
import numpy as np
from astropy.io import fits
import math


# Set directory  (C:\\...\\... for Windows Users, /Users/... for mac)
os.chdir("C:\\")

#Ask user for file name
filen = input("What file would you like to read? ")


# Optional line to set directory to a name specific folder (delete if unneeded)
os.chdir("C:\\" + filen) # End the quotations with a \\ so that folder name is added properly


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
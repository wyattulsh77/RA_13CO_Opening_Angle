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

# Open both files
file = fits.open(filename + ".red.pixel_map.fits")
red_data = file[0].data

file = fits.open(filename + ".blue.pixel_map.fits")
blue_data = file[0].data


data = red_data

# Adds blue detected pixels to red detected pixels
for j, y in enumerate(data):
    xpos = data[j]
    for i, x in enumerate(xpos):
        if (blue_data[j, i] == 1):
            data[j, i] = 1

# Make new fits file and writes it out
new_file = fits.PrimaryHDU()
new_file.data = data
new_file.header = file[0].header.copy()
new_file.writeto(filen + ".combined.pixel_map.fits", overwrite = True)
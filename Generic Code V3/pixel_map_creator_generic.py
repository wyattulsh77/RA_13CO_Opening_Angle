import os
import numpy as np
import matplotlib.pyplot as plt
from astropy.io import fits
import math
from astropy.wcs import WCS
from astropy.coordinates import SkyCoord
from astropy.stats import sigma_clipped_stats
from astropy.modeling import models, fitting


'''
Creates a binary pixel map from an integrated intensity
Things to edit:
1. Set directory (line 23)
2. Change the cut radius if necessary
3. Add directory to line 38 (or remove if unneeded)
4. Add in object coordinates (starting at line 78)
'''


# Set directory  (C:\\...\\... for Windows Users, /Users/... for mac)
os.chdir("C:\\")


# VARIABLE TO EDIT

# How big of a radius around the object do you want to remove (standard is 4.0 arcsec)
cut_radius_arcsec = 4.0



#Ask user for file name
filen = input("What file would you like to read? ")
name = filen

# Optional line to set directory to a name specific folder (delete if unneeded)
os.chdir("C:\\" + filen) # End the quotations with a \\ so that folder name is added properly


# Determine if the file is red or blue shifted and name accordingly
filename = filen + ".integrated_intensity."
r_or_b = input("Is this red or blue shifted? ")

if(r_or_b == "b" or r_or_b == "B" or r_or_b == "blue" or r_or_b == "Blue"):
    filen += ".blue.pixel_map.fits"
    filename += "blue.fits"
elif(r_or_b == "r" or r_or_b == "R" or r_or_b == "red" or r_or_b == "Red"):
    filen += ".red.pixel_map.fits"
    filename += "red.fits"
else:
    filename += "error"


# Open and read file
file = fits.open(filename)


data = file[0].data

# Determine threshold value and create pixel map
value = float(input("What is the threshold value? "))


for j, y in enumerate(data):
    xpos = data[j]
    for i, x in enumerate(xpos):
        if (data[j, i] >= value):
            data[j, i] = 1
        elif(data[j, i] == np.nan):
            data[j, i] = np.nan
        else:
            data[j, i] = 0



# Give cordinates of objects --------------------------------------------------------------- Coordinates Here!
if(name == "HOPS10"):
    ra = "05h35m09.050s"
    dec = "-05d58m26.8s"
elif(name == "HOPS157"):
    ra = "05h37m56.574s"
    dec = "-06d56m39.47s"
else:
    ra = "00h00m00.000s"
    dec = "00d00m00.000s"
    print("NO COORIDNATES GIVEN")



# Turn RA and dec into pixel where object is
wcs_3d = WCS(file[0].header)
wcs = wcs_3d.celestial  
# Convert to SkyCoord
sky_coord = SkyCoord(ra, dec, frame='icrs')
# Convert world (RA/Dec) to pixel (x/y)
ra, dec = wcs.world_to_pixel(sky_coord)
ra = int(ra)
dec = int(dec)


# Convert cut radius to pixels
cut_radius_pixel = abs(round((cut_radius_arcsec/3600)*(1/(file[0].header['CDELT1']))))


# Remove cut radius pixels
for j, z in enumerate(data):
    xpos = z
    for i, g in enumerate(xpos):
        x = (i - ra)
        y = (j - dec)
        
        if(g == 1 and math.sqrt((x**2) + (y**2))) <= cut_radius_pixel:
            data[j, i] = 0


# Make new fits file and writes it out
new_file = fits.PrimaryHDU()
new_file.data = data
new_file.header = file[0].header.copy()
new_file.header['TRSHVAL'] = value
new_file.header['CUTRAD'] = cut_radius_arcsec
new_file.writeto(filen, overwrite = True)
print("File written successfully!")
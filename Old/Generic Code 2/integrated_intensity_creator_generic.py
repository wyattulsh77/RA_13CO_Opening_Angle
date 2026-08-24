import os
import numpy as np
from astropy.io import fits
import math


'''
How to use this code!

1) Start with this image processing file
- Flatten 3D images to 2D with this file, specifying red and blue sides with their corresponding velocity ranges

2) Then use the pixel map creator
- Review processed image to find a 3 signma value of the noise, then enter that value into this code
- You can specify a different central cut radius to control how many arcseconds around the object are ignored

3) Use the pixel map chopper if necessary
- If there are unwanted detection pixels, the pixel map chopper can remove them in most cases
- This will create a pixel map file with a .chopped extension. If you are happy with the chopped image, delete the original file and remove the .chopped extension

4) Use the red blue combiner to create a red-blue pixel map if you have both sides of the outflow

5) Finally, measure the outflow angle with the angle measurer file
- Directions on how to use this on file


Things to edit:
1. Set directory (line 39)
2. Add directory to line 47 (or remove if unneeded)
3. Change file name extensions (line 49)
'''






# Set directory  (C:\\...\\... for Windows Users, /Users/... for mac)
os.chdir("C:\\")


# Prompt user for file name and create new file name
file = input("What file would you like to read? (extensions added automatically) ")


# Optional line to change directory to a name specific one (Remove if unneeded)
os.chdir("C:\\" + file) # End the quotations with a \\ so that folder name is added properly

filename = file + ".13CO21.robust1.fits" # Change this to whatever your file extensions after object name are <------------------- Very Important!!!
newfile = file + ".integrated_intensity." # If you change this, be sure to make changes to every other instance of file names (easiest not to change, there are a lot of refences to file names!)


# Open file
file = fits.open(filename)


# Let user input velocities
lwr_vel = float(input("What is the lower velocity? (km/s) "))#9.5 red
upr_vel = float(input("What is the upper velocity? (km/s) "))#13.5
lwr_vel *= 1000
upr_vel *= 1000



# Prompt user if the values they are entering are redshifted or blueshifted
r_or_b = input("Is this red or blue shifted? ")

if(r_or_b == "b" or r_or_b == "B" or r_or_b == "blue" or r_or_b == "Blue"):
    newfile += "blue.fits"
elif(r_or_b == "r" or r_or_b == "R" or r_or_b == "red" or r_or_b == "Red"):
    newfile += "red.fits"
else:
    newfile += "error"

hdr = file[0].header


# Define useful functions
"""
Finds the velocity of a given slice using the header information
"""
def index_to_vel(x):
    return (hdr['CRVAL3'] + ((x+1)-hdr['CRPIX3']) * hdr['CDELT3'])

"""
Reverses index_to_vel function
"""
def vel_to_index(vel):
    return (((vel - hdr['CRVAL3'])/hdr['CDELT3']) + hdr['CRPIX3'] -1)
    


# Set data to variable names
data = file[0].data
slice = data[0]
ypos = slice[0]
xpos = ypos[0]



# Perform calculations to create new image array
lwr_index = math.ceil(vel_to_index(lwr_vel))
upr_index = math.floor(vel_to_index(upr_vel) + 0.1)
print(lwr_index)
print(upr_index)
delta_index = int(upr_index-lwr_index+1)

velocity_indexes = np.linspace(lwr_index, upr_index, delta_index)

new_image = np.zeros([int(hdr['NAXIS1']),int(hdr['NAXIS2'])])

for sl in velocity_indexes:
    ypos = slice[int(sl)]
    for j, y in enumerate(ypos):
        xpos = ypos[j]
        for i, x in enumerate(xpos):
            new_image[j,i] += ypos[j,i]
new_image *= (hdr['CDELT3']/1000)



# Make new fits file and write it out
new_file = fits.PrimaryHDU()
new_file.data = new_image
new_file.header = hdr.copy()
keys_to_remove = ['CDELT3', 'CRPIX3', 'CRVAL3', 'CTYPE3', 'CDELT4', 'CRPIX4', 'CRVAL4', 'CTYPE4']
for key in keys_to_remove:
    del new_file.header[key]

new_file.writeto(newfile, overwrite = True)
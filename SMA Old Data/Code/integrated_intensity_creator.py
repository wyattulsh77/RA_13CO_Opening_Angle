import os
import numpy as np
from astropy.io import fits
import math

# Set directory
os.chdir("C:\\users\\wyatt\\OneDrive\\Desktop\\Research Assistance\\Image Files\\13")



# Prompt user for file name and create new file name
file = input("What file would you like to read? (.13CO21.robust+/-1.fits added automatically) ")

# Optional line to change directory to a name specific one (Remove if unneeded)
os.chdir("C:\\users\\wyatt\\OneDrive\\Desktop\\Research Assistance\\Image Files\\13\\" + file)

robust = input("Is this a + or - robust image? ")

if(robust == "+"):
    filename = file + ".13CO21.robust1.fits" # Change this to whatever your file extensions after object namr are
else:
    filename = file + ".13CO21.robust-1.fits" # Change this to whatever your file extensions after object namr are
newfile = file + ".integrated_intensity."


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
import os
import numpy as np
from astropy.io import fits
import math
import turtle
import matplotlib.pyplot as plt
from astropy.io import fits
from astropy.wcs import WCS
from astropy.coordinates import SkyCoord
from astropy.stats import sigma_clipped_stats
from astropy.modeling import models, fitting


# VARIABLE TO EDIT

# How big of a radius around the object do you want to remove
cut_radius_arcsec = 15.0




# Sets directory to where files are held
os.chdir("C:\\users\\wyatt\\OneDrive\\Desktop\\Research Assistance\\Image Files\\13")

#Ask user for file name
filen = input("What file would you like to read? ")
name = filen


# Optional line to set directory to a name specific folder (delete if unneeded)
os.chdir("C:\\users\\wyatt\\OneDrive\\Desktop\\Research Assistance\\Image Files\\13\\" + filen)


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




# Give cordinates of objects
if(name == "Per1"):
    ra = "03h43m56.770s"
    dec = "32d00m49.865s"
elif(name == "Per2"):
    ra = "03h32m17.915s"
    dec = "30d49m48.033s"
elif(name == "Per3"):
    ra = "03h29m00.554s"
    dec = "31d11m59.859s"
elif(name == "Per5"):
    ra = "03h31m20.931s"
    dec = "30d45m30.334s"
elif(name == "Per6"):
    ra = "03h33m14.404s"
    dec = "31d07m10.715s"
elif(name == "Per7"):
    ra = "03h30m32.681s"
    dec = "+30d26m26.480s"
elif(name == "Per9"):
    ra = "03h29m51.876s"
    dec = "+31d39m05.516s"
elif(name == "Per10"):
    ra = "03h33m16.412s"
    dec = "+31d06m52.384s"
elif(name == "Per11"):
    ra = "03h43m57.055s"
    dec = "+32d03m04.669s"
elif(name == "Per13"):
    ra = "03h29m11.990s"
    dec = "+31d13m08.140s"
elif(name == "Per15"):
    ra = "03h29m04.190s"
    dec = "+31d14m48.430s"
elif(name == "Per16"):
    ra = "03h43m50.999s"
    dec = "+32d03m23.858s"
elif(name == "Per17"):
    ra = "03h27m39.120s"
    dec = "+30d13m02.526s"
elif(name == "Per19"):
    ra = "03h29m23.498s"
    dec = "+31d33m29.173s"
elif(name == "Per20"):
    ra = "03h27m43.119s"
    dec = "30d12m28.962s"
elif(name == "Per21"):
    ra = "03h29 m10.690s"
    dec = "+31d18m20.150s"
elif(name == "Per22"):
    ra = "03h25m22.353s"
    dec = "+30d45m13.213s"
elif(name == "Per23"):
    ra = "03h29m17.250s"
    dec = "+31d27m46.340s"
elif(name == "Per24"):
    ra = "03h28m45.297s"
    dec = "+31d05m41.693s"
elif(name == "Per25"):
    ra = "03h26m37.490s"
    dec = "+30d15m27.900s"
elif(name == "Per26"):
    ra = "03h25m38.870s"
    dec = "+30d44m05.300s"
elif(name == "Per27"):
    ra = "03h28m55.560s"
    dec = "+31d14m37.170s"
elif(name == "Per28"):
    ra = "03h43m50.987s"
    dec = "+32d03m07.967s"
elif(name == "Per29"):
    ra = "03h33m17.860s"
    dec = "+31d09m32.307s"
elif(name == "Per30"):
    ra = "03h33m27.330s"
    dec = "+31d07m10.290s"
elif(name == "Per31"):
    ra = "03h28m32.547s"
    dec = "+31d11m05.151s"
elif(name == "Per34"):
    ra = "03h30m15.190s"
    dec = "+30d23m49.110s"
elif(name == "Per36"):
    ra = "03h28m57.360s"
    dec = "+31d14m15.610s"
elif(name == "Per40"):
    ra = "03h33m16.650s"
    dec = "+31d07m54.810s"
elif(name == "Per41"):
    ra = "03h33m20.341s"
    dec = "+31d07m21.355s"
elif(name == "Per42"):
    ra = "03h25m39.135s"
    dec = "+30d43m57.909s"
elif(name == "Per44"):
    ra = "03h29m03.760s"
    dec = "+31d16m03.430s"
elif(name == "Per46"):
    ra = "03h28m00.420s"
    dec = "+30d08m01.010s"
elif(name == "Per50"):
    ra = "03h29m07.764s"
    dec = "+31d21m57.162s"
elif(name == "Per52"):
    ra = "03h28m39.699s"
    dec = "+31d17m31.882s"
elif(name == "Per53"):
    ra = "03h47m41.577s"
    dec = "+32d51m43.745s"
elif(name == "Per56"):
    ra = "03h47m05.422s"
    dec = "+32d43m08.330s"
elif(name == "Per57"):
    ra = "03h29m03.322s"
    dec = "+31d23m14.338s"
elif(name == "Per61"):
    ra = "03h44m21.301s"
    dec = "+31d59m32.526s"
elif(name == "Per62"):
    ra = "03h44m12.973s"
    dec = "+32d01m35.289s"
elif(name == "B1-bS"):
    ra = "03h33m21.340s"
    dec = "+31d07m26.440s"

# ---------------------------------------------- Per33
elif(name == "Per33"):
    ra = "03h25m36.330s"
    dec = "+30d45m14.810s"

elif(name == "Per-Bolo45"):
    ra = "03h29m06.770s"
    dec = "+31d17m29.960s"
elif(name == "Per-Bolo58"):
    ra = "03h29m25.417s"
    dec = "+31d28m15.000s"
elif(name == "SVS 13C"):
    ra = "03h29m02.030s"
    dec = "+31d15m37.750s"
else:
    ra = 0
    dec = 0



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
for j, z in enumerate(new_image):
    xpos = z
    for i, g in enumerate(xpos):
        x = (i - ra)
        y = (j - dec)
        
        if(g == 1 and math.sqrt((x**2) + (y**2))) >= cut_radius_pixel:
            new_image[j, i] = 0





#Overwrite file
new_file = fits.PrimaryHDU()
new_file.data = new_image
new_file.header = header
new_file.writeto(filename, overwrite = True)
print("File written successfully!")
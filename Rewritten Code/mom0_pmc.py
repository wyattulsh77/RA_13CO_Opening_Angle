unit = "m/s" # What are the units of your cube? (km/s, m/s) (will convert to km/s)

directory = "C:\\users\\wyatt\\OneDrive\\Desktop\\Research Assistance\\Class0\\HOPS169\\13CO" # What is the directory of your file?

molecule = "13CO" # What is the name of the molecule that you are working with as it appears in your filenames

fileprefix = "HOPS169_" # What are the prefixes before the molecule in your filenames

filesuffix = "_Tp12m7m_Combine_pbcor_masked" # What are the suffixes after the molcule in your filenames

filetype = ".fits" # What are you filetypes (most likely .fits, include .)

lwrvel = 4101.99 # What is the lower channel you would like to create moment 0 from? (in units of your cube, float)
#lwrvel = float(input("What is the lower channel you would like to integrate from? ")) # Uncomment this line if you'd like to be prompted when code runs

uprvel = 5264.38 # What is the upper channel you would like to create moment 0 to? (in units of your cube, float)
#uprvel = float(input("What is the upper channel you would like to integrate to? ")) # Uncomment this line if you'd like to be prompted when code runs

# If you do not have a good range for an rms map, set these to 0 and you can define a single value for rms when code runs
lwrrms = -20723.2  # What is a good lower chanel to start rms map at? (in units of your cube, float)

uprrms = -7853.98 # What is a good upper chanel to end rms map at? (in units of your cube, float)


# Code should not have to be edited beyond here ------------------------------------------------------------------------------------------------------------------


import astropy.units as u
from spectral_cube import SpectralCube
from spectral_cube import wcs_utils
import os
import numpy as np
from astropy.io import fits
import matplotlib.pyplot as plt
from astropy.convolution import Gaussian2DKernel

# Change directory
os.chdir(directory)

# Open fits file and cube and convert cube to km/s
file = fits.open(f'{fileprefix}{molecule}{filesuffix}{filetype}')
header = file[0].header
full_cube = SpectralCube.read(f'{fileprefix}{molecule}{filesuffix}{filetype}')
full_cube = full_cube.with_spectral_unit(u.km/u.s, velocity_convention='radio')

# Convert units if necessary
if unit == "m/s":
    lwrvel = (lwrvel/1000)
    uprvel = (lwrvel/1000)
    lwrrms = (lwrrms/1000)
    uprrms = (uprrms/1000)


# Create rms map if needed
singlerms = False
sat = False
if os.path.exists(f'{fileprefix}rmsmap.fits'):
    sat = input('Do you want to use existing rms map? (y/n) ')
    if sat == 'n':
        sat = False
    else:
        if sat != 'y': print('Invalid input, continuing with rms map. ')
        sat = True
        rmsfile = fits.open(f'{fileprefix}rmsmap.fits')
        rms_map = rmsfile[0].data

if lwrrms == 0:
    sat = True
    singlerms = True

while (not sat):
    rms_slab = full_cube.spectral_slab(lwrrms * u.km / u.s, uprrms * u.km / u.s)
    rms_map = np.sqrt(np.mean(np.square(rms_slab.unmasked_data[:]), axis=0))
    fig, ax = plt.subplots()
    plt.imshow(rms_map, origin="lower")
    plt.suptitle("RMS map")
    plt.show()
    sat = input('Does the rms map look good? (y/n) ')
    if(sat == ('y')):
        sat = True
        new_file = fits.PrimaryHDU()
        new_file.data = rms_map
        new_file.header = header.copy()
        keys_to_remove = ['CDELT3', 'CRPIX3', 'CRVAL3', 'CTYPE3', 'CUNIT3']
        for key in keys_to_remove:
            del new_file.header[key]
        new_file.header['LWRVEL'] = lwrrms
        new_file.header['UPRVEL'] = uprrms
        new_file.writeto(f'{fileprefix}rmsmap.fits', overwrite = True)
    else:
        sat = input('Adjust range (l/u +/- #) or define single value (s): ')
        if sat[0:1] == ('l'):
            if sat[1:2] == ('+'):
                lwrrms += float(sat[2:])*header['CDELT3']
            if sat[1:2] == ('-'):
                lwrrms -= float(sat[2:])*header['CDELT3']
            sat = False
        elif sat[0:1] == ('u'):
            if sat[1:2] == ('+'):
                uprrms += float(sat[2:])*header['CDELT3']
            if sat[1:2] == ('-'):
                uprrms -= float(sat[2:])*header['CDELT3']
            sat= False
        elif sat == 's':
            print('Single value will be entered after moment 0 map shown')
            sat = True
            singlerms = True
        else:
            print('Not a valid input.')
            sat = False





# Create moment 0 map
sat = False
while not sat:
    mom_slab = full_cube.spectral_slab(lwrvel * u.km / u.s, uprvel * u.km / u.s)
    mom0_map = mom_slab.moment(order=0, axis=0)
    fig, ax = plt.subplots()
    plt.imshow(mom0_map.value, origin="lower")
    plt.suptitle("Moment 0 map")
    plt.show()
    sat = input('Are you satisfied with the moment 0 map? (y/n) ')
    if sat == 'y':
        sat = True
    elif sat == 'n':
        sat = input(f"How would you like to adjust the range? (currently {lwrvel} to {uprvel} km/s) (l/u +/-/= #) ")
        if sat[0:1] == ('l'):
            if sat[1:2] == ('+'):
                lwrvel += float(sat[2:])*header['CDELT3']
            if sat[1:2] == ('-'):
                lwrvel -= float(sat[2:])*header['CDELT3']
            if sat[1:2] == ('='):
                lwrvel = float(sat[2:])
            sat = False
        elif sat[0:1] == ('u'):
            if sat[1:2] == ('+'):
                uprvel += float(sat[2:])*header['CDELT3']
            if sat[1:2] == ('-'):
                uprvel -= float(sat[2:])*header['CDELT3']
            if sat[1:2] == ('='):
                uprvel = float(sat[2:])
            sat= False





# Create boolean mask
snr_map = mom0_map/rms_map
mask = snr_map.value > 3
mom0_slab_masked = mom_slab.with_mask(mask)
mom0_map_masked = mom0_slab_masked.moment(order=0, axis=0)
fig, ax = plt.subplots(1, 3, figsize=(12, 4))
ax[1].imshow(mom0_map_masked.value, origin="lower")
ax[1].set_title("Moment 0 w/ mask")
ax[2].imshow(mask, origin="lower")
ax[2].set_title("Mask/pixel map")
ax[0].imshow(mom0_map.value, origin="lower")
ax[0].set_title("Moment 0")
plt.tight_layout()
plt.show()


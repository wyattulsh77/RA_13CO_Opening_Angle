import os
import numpy as np
from astropy.io import fits
import matplotlib.pyplot as plt

'''
Creates an interactive matplotlib window to remove unwanted pixels from a pixel map
'''


directory = "C:\\users\\wyatt\\OneDrive\\Desktop\\Research Assistance\\" 

cl = input("What is the class of the object? ")
if cl == "1" or cl == "I":
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
if r_or_b.lower().startswith("b"):
    filen += ".blue.pixel_map.fits"
    filename += ".blue.pixel_map.chopped.fits"
elif r_or_b.lower().startswith("r"):
    filen += ".red.pixel_map.fits"
    filename += ".red.pixel_map.chopped.fits"
else:
    raise ValueError("Unknown shift type: {}".format(r_or_b))

# Open file and extract data
with fits.open(filen) as hdu_list:
    new_image = hdu_list[0].data.astype(np.int8)
    header = hdu_list[0].header.copy()

# Mirror vertical axis so image matches ds9 style
new_image = new_image[::-1]
rows, cols = new_image.shape

# Parameters
erase_radius = 10  # radius affects (2*erase_radius+1)x(2*erase_radius+1) block

fig, ax = plt.subplots(figsize=(8, 8))
im = ax.imshow(new_image, cmap='gray_r', vmin=0, vmax=1, origin='upper')
ax.set_title('Interactive Pixel Map (click to erase)')
ax.set_xlabel('Column')
ax.set_ylabel('Row')


def update_image():
    im.set_data(new_image)
    im.axes.figure.canvas.draw_idle()


def erase_block(row_center, col_center):
    row_min = max(0, row_center - erase_radius)
    row_max = min(rows, row_center + erase_radius + 1)
    col_min = max(0, col_center - erase_radius)
    col_max = min(cols, col_center + erase_radius + 1)
    new_image[row_min:row_max, col_min:col_max] = 0


def on_click(event):
    if event.inaxes != ax or event.xdata is None or event.ydata is None:
        return
    col_center = int(np.floor(event.xdata))
    row_center = int(np.floor(event.ydata))
    if 0 <= row_center < rows and 0 <= col_center < cols:
        erase_block(row_center, col_center)
        update_image()


fig.canvas.mpl_connect('button_press_event', on_click)
plt.tight_layout()
plt.show()

# Mirror vertical axis back for saving
new_image = new_image[::-1]

new_hdu = fits.PrimaryHDU(data=new_image, header=header)
new_hdu.writeto(filen, overwrite=True) # change filen to filename if you want it to write a file with a .chopped extension
print('File written successfully:', filen)

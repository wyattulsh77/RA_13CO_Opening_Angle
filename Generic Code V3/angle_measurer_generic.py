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
How to use this file
THIS WILL NOT WORK WITH JUPYTER LAB (it does not allow for inspection of the graphs)
This will give you the final measurement and uncerainty of the outflow angle

1) Make sure you have your pixel maps generated for this source
- If you have both a red and a blue side, create a combined pixel map as well

2) Run this file and specify the object name and which pixel map you are using

3) It will bring up a histogram of the measured angles, and you need to define the central region you would like to cut (lower value first)
- Hover over the bars on the histogram to see what the value of the bar is (must be a multiple of 3 since angles are binned in 3 degrees)
- You can also define other ranges or individual values that you would like to remove (if you are entering a range, be sure to put + or - for the ±)

4) This will bring up a fitted Gaussian and an image with the measured angle overlayed
- The angle will be printed, as will the mean of the data
- The goal is to get this mean as close to 0 as possible
    - if the mean is ~ a positive integer, add that integer to the guess angle, and if it is ~ a negative integer, subtract that integer from the guess angle
- Be sure to save this image if you are happy with the results (there will be a save button on the opened window)

5) Specify how many bars you would like the fitting region to be shifted down and up to find the standard deviation
- This shift should be until the data no longer looks like the sides of a Gaussian



Things to edit:
1. Set directory (line 71)
2. Add directory to line 78 (or remove if unneeded)
3. Add in object cooridinates (starting at line 102)
'''



def overlay_RB(red, blue, title='Overlayed Red & Blue Image'):

    red_norm = (red - np.min(red)) / np.ptp(red)
    blue_norm = (blue - np.min(blue)) / np.ptp(blue)

    '''
    # Combine min and max across both images
    min_val = min(np.min(red), np.min(blue))
    max_val = max(np.max(red), np.max(blue))
    ptp_val = max_val - min_val

     # Normalize both using the same scale
    red_norm = (red - min_val) / ptp_val
    blue_norm = (blue - min_val) / ptp_val
    '''

     # Create RGB image
    overlay_rgb = np.zeros((*red.shape, 3))  # shape: (H, W, 3)
    overlay_rgb[..., 0] = red_norm   # Red channel
    overlay_rgb[..., 2] = blue_norm  # Blue channel

    return overlay_rgb


# Set directory  (C:\\...\\... for Windows Users, /Users/... for mac)
os.chdir("C:\\")


file = input("What is the name of the object? ")


# Optional line to set directory to a name specific folder (delete if unneeded)
os.chdir("C:\\" + file) # End the quotations with a \\ so that folder name is added propely


filename=file

# Ask user if file is redshifter or blushifted and name accordingly
r_or_b = input("Is this red shifted, blue shifted, or combined? ")

if(r_or_b == "b" or r_or_b == "B" or r_or_b == "blue" or r_or_b == "Blue"):
    filename += ".blue.pixel_map.fits"
elif(r_or_b == "r" or r_or_b == "R" or r_or_b == "red" or r_or_b == "Red"):
    filename += ".red.pixel_map.fits"
elif(r_or_b == "c" or r_or_b == "C" or r_or_b == "combined" or r_or_b == "Combined"):
    filename += ".combined.pixel_map.fits"



ra = ""
dec = ""



name = file

# Define cordinates and guess angles of objects ------------------------------------------------------------------------- Coordinates Here
if(name == "HOPS10"):
    ra = "05h35m09.050s"
    dec = "-05d58m26.8s"
elif(name == "HOPS185"):
    ra = "05h36m36.969s"
    dec = "-06d14m58.780s"
else:
    print("No coordinates given")
    ra = 0
    dec = 0


#Open file
file = fits.open(filename)

data = file[0].data
hdr = file[0].header


lwr_velo = hdr['LWRVELO']
upr_velo = hdr['UPRVELO']
cut_rad = hdr['CUTRAD']
threshold_value = hdr['TRSHVAL']


# Turn RA and dec into pixel where object is
wcs_3d = WCS(file[0].header)
wcs = wcs_3d.celestial  
# Convert to SkyCoord
sky_coord = SkyCoord(ra, dec, frame='icrs')
# Convert world (RA/Dec) to pixel (x/y)
ra, dec = wcs.world_to_pixel(sky_coord)
ra = int(ra)
dec = int(dec)

sat = False
run = 0

while(not sat):
    run+=1

    guess = int(input("What is your guess for the position angle? "))

    # Calculate the angle to each pixel and store in a list
    angle_list = []

    for j, z in enumerate(data):
        xpos = z
        for i, g in enumerate(xpos):
            x = (i - ra)
            y = (j - dec)
            
            if(data[j, i] == 1):
                
                angle = 0
                if(y == 0 and x < 0):
                    angle = 90
                elif(x == 0 and y < 0):
                    angle = 180
                elif(y == 0 and x > 0):
                    angle = 270    
                elif(y > 0 and x < 0):
                    angle = int(round(math.degrees(math.atan((-x)/y))))
                elif(y < 0 and x < 0):
                    angle = 90 + int(round(math.degrees(math.atan((-y)/(-x)))))
                elif(y < 0 and x > 0):
                    angle = 180 + int(round(math.degrees(math.atan((x)/(-y)))))
                elif(y > 0 and x > 0):
                    angle = 270 + int(round(math.degrees(math.atan((y)/(x)))))





                '''
                elif(y > 0 and x < 0):
                    angle = 180 - int(round(math.degrees(math.atan((-x)/y))))
                elif(y < 0 and x < 0):
                    angle = 90 - int(round(math.degrees(math.atan((-y)/(-x)))))
                elif(y < 0 and x > 0):
                    angle = 360 - int(round(math.degrees(math.atan((x)/(-y)))))
                elif(y > 0 and x > 0):
                    angle = 270 - int(round(math.degrees(math.atan((y)/(x)))))
                '''


                if(angle >= 180):
                    angle -= 180
                if(guess < 90 and angle > guess + 90):
                    angle -= 180
                if(guess > 90 and angle < guess - 90):
                    angle += 180

                angle = angle - guess


                angle_list.append(angle)
                #print(angle)
                #if(angle < 45):
                    #print(i,j,x,y,angle)

    # Create graph of angles
    angle_list.sort()
    angles_possible = []
    weights = []
    ind = -90
    while(ind < 91):
        weights.append(1)
        angles_possible.append(ind)
        ind += 3

    angle_freq = np.zeros(len(angles_possible))
    for i, angle in enumerate(angles_possible):
        for ang in angle_list:
            if (ang >= angle and ang < angle + 3):
                angle_freq[i] += 1

    plt.bar(angles_possible, angle_freq)
    plt.show()


    # Select values to remove
    lwr_remove = 1
    upr_remove = 1

    while(lwr_remove % 3 != 0):
        lwr_remove = int(input("What is the lower value that you would like to remove from the curve? "))
    while(upr_remove % 3 != 0):
        upr_remove = int(input("What is the upper value that you would like to remove from the curve? "))


    angle_freq_old = angle_freq.copy()
    weights_old = weights.copy()



    # Remove angles between selected values
    angles_to_remove = []
    angles_to_remove_perm = []
    ind = lwr_remove
    while(ind <= upr_remove):
        angles_to_remove.append(ind)
        ind += 3

    remove_range = ""
    xtra_ranges = []
    while(remove_range != "n"):
        remove_range = input("Any range of values to remove? (input as '±xx ±xx', lower first: n to stop entering ranges) ")
        if(remove_range != "n"):
            xtra_ranges.append(remove_range)
        if(remove_range!= "n" and int(remove_range[0:3]) % 3 == 0):
            lower = int(remove_range[0:3])
            upper = int(remove_range[4:7])
            while(lower <= upper):
                angles_to_remove.append(lower)
                angles_to_remove_perm.append(lower)
                lower += 3

    remove_individual = ""
    while(remove_individual != "n"):
        remove_individual = input("Any indiviual values to remove? (n to stop entering values) ")
        if(remove_individual != "n"):
            xtra_ranges.append(remove_individual)
            angles_to_remove.append(int(remove_individual))
            angles_to_remove_perm.append(int(remove_individual))
            
    for angle in angles_possible:
        if angle in angles_to_remove:
            index = angles_possible.index(angle)
            angle_freq[index] = 0
            weights[index] = 0


    # Fit Gaussian to data
    g_init = models.Gaussian1D(amplitude=200., mean=0, stddev=25.0)
    fit_g = fitting.TRFLSQFitter()
    g = fit_g(g_init, angles_possible, angle_freq, weights=weights)


    opening_angle = 2*math.sqrt((-math.log(0.25))*2*(g.stddev**2))
    fnl_angle = opening_angle
    # Show results
    print("Opening Angle = " + str(int(opening_angle)))
    print("Gaussian mean offset from zero = " + str(g.mean.value) + " (Add to position angle guess)")


    # Graph initial gaussian
    if(run <= 1):
        if(r_or_b == "b" or r_or_b == "B" or r_or_b == "blue" or r_or_b == "Blue" or r_or_b == "r" or r_or_b == "R" or r_or_b == "red" or r_or_b == "Red"):
            name += ".integrated_intensity"

            if(r_or_b == "b" or r_or_b == "B" or r_or_b == "blue" or r_or_b == "Blue"):
                name += ".blue.fits"
            elif(r_or_b == "r" or r_or_b == "R" or r_or_b == "red" or r_or_b == "Red"):
                name += ".red.fits"


            file = fits.open(name)
            img = file[0].data

        else:
            file = fits.open(name + ".integrated_intensity.red.fits")
            red_data = file[0].data
            file = fits.open(name + ".integrated_intensity.blue.fits")
            blue_data = file[0].data
            img = overlay_RB(red_data, blue_data)



    # Create image with angles next to Gaussian
    fig, axes = plt.subplots(nrows=1, ncols=2, figsize=(12, 4))
    axes[0].bar(angles_possible, angle_freq_old, color='khaki')
    axes[0].bar(angles_possible, angle_freq, color='forestgreen')
    axes[0].plot(angles_possible, g(angles_possible), label='Gaussian', color='orange')
    axes[0].set_ylim(0, 1.2*np.max(angle_freq))
    axes[1].imshow(img, cmap='magma', origin='lower')
    axes[1].axhline(dec, color='white', linewidth=1, linestyle='--')  # x-axis
    axes[1].axvline(ra, color='white', linewidth=1, linestyle='--')  # y-axis

    # Figure out x and y values of guess line
    guess_xes = []
    guess_ys = []

    guess_xes.append(0)
    guess_ys.append(dec - (math.tan(math.radians(guess-90))*ra))
    guess_xes.append(len(data[0])-1)
    guess_ys.append(dec + (math.tan(math.radians(guess-90))*(len(data[0]-1)-(ra+1))))

    axes[1].plot(guess_xes, guess_ys, linestyle="dotted")

    # Figure out x and y values of negative angle lines
    neg_xes = []
    neg_ys = []

    neg_xes.append(0)
    neg_ys.append(dec - (math.tan(math.radians((guess-(opening_angle/2))-90))*ra))
    neg_xes.append(len(data[0])-1)
    neg_ys.append(dec + (math.tan(math.radians(guess-(opening_angle/2)-90))*(len(data[0]-1)-(ra+1))))

    axes[1].plot(neg_xes, neg_ys, linestyle="-.", color='lightgreen')


    # Figure out x and y values of negative positive lines
    pos_xes = []
    pos_ys = []

    pos_xes.append(0)
    pos_ys.append(dec - (math.tan(math.radians((guess+(opening_angle/2))-90))*ra))
    pos_xes.append(len(data[0])-1)
    pos_ys.append(dec + (math.tan(math.radians(guess+(opening_angle/2)-90))*(len(data[0]-1)-(ra+1))))

    axes[1].plot(pos_xes, pos_ys, linestyle="-.", color='lightgreen')

    axes[1].set_ylim(-.5, len(data)-.5)
    axes[1].set_xlim(-.5, len(data)-.5)

    fig.tight_layout()
    fig.show()

    satq = input("Are you happy with these results? (y/n) ")
    if(satq.lower() == "y" or satq.lower() == "yes"):
        sat = True




# Ask user how far down and up they would like to push the fitting region for the uncertainty
lwr_amt = int(input("How many values would you like to shift the lower value down? "))
upr_amt = int(input("How many values would you like to upper the lower value up? "))


# Shift lower and upper removes to find standard deviation
measured_angles = []


# Shift lower down
lwr_remove_old = lwr_remove
upr_remove_old = upr_remove
lwr_remove += 3


for i in range(lwr_amt + 1):

    lwr_remove -= 3
    upr_remove = upr_remove_old

    for j in range(upr_amt + 1):
        k_or_d = "k" # make k and comment out line to keep all
        angle_freq = angle_freq_old.copy()
        weights = weights_old.copy()
        
        # Remove angles between selected values
        angles_to_remove = []
        ind = lwr_remove
        while(ind <= upr_remove):
            angles_to_remove.append(ind)
            ind += 3

        for angle in angles_to_remove_perm:
            angles_to_remove.append(angle)

        for angle in angles_possible:
            if angle in angles_to_remove:
                index = angles_possible.index(angle)
                angle_freq[index] = 0
                weights[index] = 0



        g_init = models.Gaussian1D(amplitude=200., mean=0, stddev=25.0)
        fit_g = fitting.TRFLSQFitter()
        g = fit_g(g_init, angles_possible, angle_freq, weights=weights)

        # Uncomment to check graphs
        plt.bar(angles_possible, angle_freq_old)
        plt.plot(angles_possible, g(angles_possible), label='Gaussian', color='orange')

        opening_angle = 2*math.sqrt((-math.log(0.25))*2*(g.stddev**2))

        

        print("This has an angle of " + str(int(opening_angle)) + " and ignores from " + str(lwr_remove) + " to " + str(upr_remove) + ".")
        #plt.show()
        #k_or_d = input("Would you like to keep or drop it? ")

        if(k_or_d == "k" or k_or_d == "keep" or k_or_d == "K" or k_or_d == "Keep"):
            measured_angles.append(opening_angle)
        upr_remove += 3


# Display standard deviation of angles
uncertainty = int(np.std(measured_angles))
print(uncertainty)


print("Final Results:\nLower Velocity of Integration = " + str(lwr_velo) + " m/s\nUpper Velocity of Integration = " + str(upr_velo) + " m/s")
print("Threshold Value of Detection Pixel = " + str(threshold_value) + "\nCentral Cut Radius = " + str(cut_rad) + " Arcsec")

print("Position Angle = " + str(guess) + " Degrees")
print("Opening Angle = " + str(round(fnl_angle)) + " +/- " + str(uncertainty) + " Degrees")
print("Central Range = " + str(lwr_remove_old) + " to " + str(upr_remove_old) + "\nExtra Values and Ranges Removed = " + str(xtra_ranges))
print("Lower Shift for Uncertainty = " + str(lwr_amt) + "\nUpper Shift for Uncertainty = " + str(upr_amt))

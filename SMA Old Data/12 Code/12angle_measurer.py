import os
import numpy as np
import matplotlib.pyplot as plt
from astropy.io import fits
import math
from astropy.wcs import WCS
from astropy.coordinates import SkyCoord
from astropy.stats import sigma_clipped_stats
from astropy.modeling import models, fitting


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



# Set directory
os.chdir("C:\\users\\wyatt\\OneDrive\\Desktop\\Research Assistance\\Image Files\\12")

# Ask user for file name
filename = input("What file would you like to read? ")
name = filename

# Optional line to set directory to a name specific folder
os.chdir("C:\\users\\wyatt\\OneDrive\\Desktop\\Research Assistance\\Image Files\\12\\" + name)


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

# Define cordinates and guess angles of objects
if(name == "Per1"):
    ra = "03h43m56.770s"
    dec = "32d00m49.865s"
    guess = 114
elif(name == "Per2"):
    ra = "03h32m17.915s"
    dec = "30d49m48.033s"
    guess = 131
elif(name == "Per3"):
    ra = "03h29m00.554s"
    dec = "31d11m59.859s"
    guess = 96
elif(name == "Per5"):
    ra = "03h31m20.931s"
    dec = "30d45m30.334s"
    guess = 118
elif(name == "Per6"):
    ra = "03h33m14.404s"
    dec = "31d07m10.715s"
    guess = 58
elif(name == "Per7"):
    ra = "03h30m32.681s"
    dec = "+30d26m26.480s"
    guess = 171
elif(name == "Per9"):
    ra = "03h29m51.876s"
    dec = "+31d39m05.516s"
    guess = 62
elif(name == "Per10"):
    ra = "03h33m16.412s"
    dec = "+31d06m52.384s"
    guess = 49
elif(name == "Per11"):
    ra = "03h43m57.055s"
    dec = "+32d03m04.669s"
    guess = 162
elif(name == "Per13"):
    ra = "03h29m11.990s"
    dec = "+31d13m08.140s"
    guess = 172
elif(name == "Per15"):
    ra = "03h29m04.190s"
    dec = "+31d14m48.430s"
    guess = 150
elif(name == "Per16"):
    ra = "03h43m50.999s"
    dec = "+32d03m23.858s"
    guess = 177
elif(name == "Per17"):
    ra = "03h27m39.120s"
    dec = "+30d13m02.526s"
    guess = 64
elif(name == "Per19"):
    ra = "03h29m23.498s"
    dec = "+31d33m29.173s"
    guess = 141 
elif(name == "Per20"):
    ra = "03h27m43.119s"
    dec = "30d12m28.962s"
    guess = 136
elif(name == "Per21"):
    ra = "03h29 m10.690s"
    dec = "+31d18m20.150s"
    guess = 57
elif(name == "Per22"):
    ra = "03h25m22.353s"
    dec = "+30d45m13.213s"
    guess = 131
elif(name == "Per23"):
    ra = "03h29m17.250s"
    dec = "+31d27m46.340s"
    guess = 61
elif(name == "Per24"):
    ra = "03h28m45.297s"
    dec = "+31d05m41.693s"
    guess = 92
elif(name == "Per25"):
    ra = "03h26m37.490s"
    dec = "+30d15m27.900s"
    guess = 107
elif(name == "Per26"):
    ra = "03h25m38.870s"
    dec = "+30d44m05.300s"
    guess = 159
elif(name == "Per27"):
    ra = "03h28m55.560s"
    dec = "+31d14m37.170s"
    guess = 44
elif(name == "Per28"):
    ra = "03h43m50.987s"
    dec = "+32d03m07.967s"
    guess = 121
elif(name == "Per29"):
    ra = "03h33m17.860s"
    dec = "+31d09m32.307s"
    guess = 90
elif(name == "Per30"):
    ra = "03h33m27.330s"
    dec = "+31d07m10.290s"
    guess = 98
elif(name == "Per31"):
    ra = "03h28m32.547s"
    dec = "+31d11m05.151s"
    guess = 149
elif(name == "Per34"):
    ra = "03h30m15.190s"
    dec = "+30d23m49.110s"
    guess = 45
elif(name == "Per36"):
    ra = "03h28m57.360s"
    dec = "+31d14m15.610s"
    guess = 13
elif(name == "Per40"):
    ra = "03h33m16.650s"
    dec = "+31d07m54.810s"
    guess = 109
elif(name == "Per41"):
    ra = "03h33m20.341s"
    dec = "+31d07m21.355s"
    guess = 25
elif(name == "Per42"):
    ra = "03h25m39.135s"
    dec = "+30d43m57.909s"
    guess = 50
elif(name == "Per44"):
    ra = "03h29m03.760s"
    dec = "+31d16m03.430s"
    guess = 140
elif(name == "Per46"):
    ra = "03h28m00.420s"
    dec = "+30d08m01.010s"
    guess = 127
elif(name == "Per50"):
    ra = "03h29m07.764s"
    dec = "+31d21m57.162s"
    guess = 95
elif(name == "Per52"):
    ra = "03h28m39.699s"
    dec = "+31d17m31.882s"
    guess = 12
elif(name == "Per53"):
    ra = "03h47m41.577s"
    dec = "+32d51m43.745s"
    guess = 54
elif(name == "Per56"):
    ra = "03h47m05.422s"
    dec = "+32d43m08.330s"
    guess = 145
elif(name == "Per57"):
    ra = "03h29m03.322s"
    dec = "+31d23m14.338s"
    guess = 148
elif(name == "Per61"):
    ra = "03h44m21.301s"
    dec = "+31d59m32.526s"
    guess = 10
elif(name == "Per62"):
    ra = "03h44m12.973s"
    dec = "+32d01m35.289s"
    guess = 18
elif(name == "B1-bS"):
    ra = "03h33m21.340s"
    dec = "+31d07m26.440s"
    guess = 110
elif(name == "L1448N-NW"):
    ra = "03h25m35.673s"
    dec = "+30d45m34.357s"
    guess = 130
elif(name == "L1448N-B"):
    ra = "03h25m35.330s"
    dec = "+30d45m14.81s"
    guess = 129
elif(name == "Per-Bolo45"):
    ra = "03h29m06.770s"
    dec = "+31d17m29.960s"
    guess = 142
elif(name == "Per-Bolo58"):
    ra = "03h29m25.417s"
    dec = "+31d28m15.000s"
    guess = 87
elif(name == "SVS 13C"):
    ra = "03h29m02.030s"
    dec = "+31d15m37.750s"
    guess = 7



#Open file
file = fits.open(filename)

data = file[0].data
hdr = file[0].header



if(ra == ""):
    ra = (input("What is the hours of the RA of the object? "))
    ra += "h"
    ra += (input("What is the minutes of the RA of the object? "))
    ra += "m"
    ra += input("What is the seconds of the RA of the object? ")
    ra += "s"

    dec = (input("What is the hours of the dec of the object? "))
    dec += "d"
    dec += (input("What is the minutes of the dec of the object? "))
    dec += "m"
    dec += (input("What is the seconds of the dec of the object? "))
    dec += "s"

    guess = int(input("What is your guess for the angle? (East of North) "))


# Turn RA and dec into pixel where object is
wcs_3d = WCS(file[0].header)
wcs = wcs_3d.celestial  
# Convert to SkyCoord
sky_coord = SkyCoord(ra, dec, frame='icrs')
# Convert world (RA/Dec) to pixel (x/y)
ra, dec = wcs.world_to_pixel(sky_coord)
ra = int(ra)
dec = int(dec)

print(ra, dec)


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
while(remove_range != "n"):
    remove_range = input("Any range of values to remove? (input as '±xx ±xx', lower first: n to stop entering ranges) ")
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
        angles_to_remove.append(int(remove_individual))
        angles_to_remove_perm.append(int(remove_individual))
        
for angle in angles_possible:
    if angle in angles_to_remove:
        index = angles_possible.index(angle)
        angle_freq[index] = 0
        weights[index] = 0



'''
Not Useful - For Testing Purposes Only
# Mirror list code
temp = 0
ind = 0
while(ind > -1):
    angle_freq[temp] = angle_freq[ind]
    temp += 1
    if(temp < 91):
        ind +=1
    else:
        ind-=1
'''



# Fit Gaussian to data
g_init = models.Gaussian1D(amplitude=200., mean=0, stddev=25.0)
fit_g = fitting.TRFLSQFitter()
g = fit_g(g_init, angles_possible, angle_freq, weights=weights)


opening_angle = 2*math.sqrt((-math.log(0.25))*2*(g.stddev**2))


# Show results
print("Angle = " + str(int(opening_angle)))
print(g.mean)



# Graph initial gaussian
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
axes[0].bar(angles_possible, angle_freq_old)
axes[0].plot(angles_possible, g(angles_possible), label='Gaussian', color='orange')
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
print(int(np.std(measured_angles)))

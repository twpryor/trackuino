import datetime
import time
import numpy as np
import matplotlib.pyplot as plt
from stdatm import temp, pres

plot = True

onTime = 1495170180.0 # Time at which payload turned on (3:03 PM) - Seconds since some random epoch years ago
launchTime = 1495170948.0 # Time at which first packet received (about 12 min later)
launchDelay = launchTime-onTime # Difference between the 2, used to reconcile SD card saved data with telemetry data

# Reduce and plot temperature and pressure data
data = []
# Extract data from csv file download from APRS.fi
f = open("PTdata.csv","r")
for line in f:
    linefields = line.split(",")

    # Determine time in seconds
    d = datetime.datetime.strptime(linefields[0], "%Y-%m-%d %H:%M:%S")
    secs = time.mktime(d.timetuple()) - launchTime

    # Get speed
    speed = float(linefields[5])

    # Get altitude
    alt = float(linefields[6])

    # Get stuff in comment field
    tp = linefields[7].split('"')[1].split("/")
    # print(tp)
    ti = (float(tp[0].strip("Ti="))-32)*(5/9)+273.15
    te = (float(tp[1].strip("Te="))-32)*(5/9)+273.15
    p = float(tp[2].strip("P= "))
    v = float(tp[3].strip("V="))

    data.append([secs/3600, alt, ti, te, p, v, speed])

f.close()

dataArray = np.array(data)
# np.savetxt("values.csv", dataArray, delimiter=",")

# Determine "predicted" temperature and pressure vs altitude
# Using 1976 standard atmosphere where To = 288.15 K = 15 C, Po = 101325 Pa
alt = np.arange(0,35000,10)
N = len(alt)
T = np.zeros(N)
P = np.zeros(N)
for j in range(N):
    # print(j)
    z = alt[j]
    T[j] = temp(288.15, z)
    P[j] = pres(101325, 288.15, z)

if plot:
    # Plot temperature vs altitude
    plt.figure(0)
    plt.plot(dataArray[0:688,1], dataArray[0:688,3] - 273.15, linewidth=3, label="Measured Temperature (ascent)")
    plt.plot(dataArray[689:,1], dataArray[689:,3] - 273.15, linewidth=3, label="Measured Temperature (descent)")
    plt.plot(alt, T-273.15, linewidth=3, label="Predicted Temperature")
    plt.xlabel("Altitude (meters)", fontsize=30)
    plt.ylabel("Temperature ($^\circ$C)", fontsize=30)
    plt.tick_params(axis='both', which='major', labelsize=20)
    plt.legend(prop={'size':16})
    plt.grid()
    plt.show()

    # Plot pressure vs altitude
    plt.figure(1)
    plt.plot(dataArray[0:688,1], dataArray[0:688, 4]/1000, linewidth=3, label="Measured Pressure (ascent)")
    plt.plot(dataArray[689:,1], dataArray[689:, 4]/1000, linewidth=3, label="Measured Pressure (descent)")
    plt.plot(alt, P/1000, linewidth=3, label="Predicted Pressure")
    plt.xlabel("Altitude (meters)", fontsize=30)
    plt.ylabel("Pressure (kPa)", fontsize=30)
    plt.tick_params(axis='both', which='major', labelsize=20)
    plt.legend(prop={'size':16})
    plt.grid()
    plt.show()

# Get arrays of UV, ozone, and associated time.
uvo = np.genfromtxt('output.csv', delimiter=',') # Load from CSV
currentUV = uvo[:,1] # All data in UV column
currentOzone = 1000/uvo[:,2] # All data in Ozone column - but since lower voltage readout is positive ozone, take the inverse and multiply by 1000 to get values close to 1
# currentOzone = uvo[:,2] # Plots raw data if uncommented
currentTime = (-launchDelay + uvo[:,0]/1000)/3600 # Current time in hours at each data point - launchDelay accounts for the time between 3:03 PM and first packet received

# For each point, determine/interpolate altitude from packet data
currentAlt = np.interp(currentTime,dataArray[:,0],dataArray[:,1])

# Crop off data after landing and before launch
start = 775
crop = -3200
currentTime = currentTime[start:crop]
currentAlt = currentAlt[start:crop]
currentUV = currentUV[start:crop]
currentOzone = currentOzone[start:crop]
uvoN = len(currentTime) # Number of data points on SD card

# For each set time interval, find peak UV
intervalWidth = 120 # 2 minutes
Nintervals = int(np.ceil(uvoN/intervalWidth))
UV = np.zeros([Nintervals,2])
for j in range(Nintervals):
    intervS = intervalWidth*j
    if j != Nintervals-1:
        intervE = intervalWidth*(j+1)
    else:
        intervE = uvoN-1
    # Find peak UV in this range
    intervM = np.round((intervE+intervS)/2)
    UVval = np.max(currentUV[intervS:intervE])
    UVintensity = 82.87*UVval*5/1024 - 82.04 # Calibration equation to go from voltage readout to W/m^2
    UV[j,:] = [intervM, UVintensity]

# Plot UV
plt.figure(2)
UVx = currentAlt[UV[:,0].astype(int)]
UVy = UV[:,1]
pop = 87
UVx1 = UVx[:pop]
UVx2 = UVx[pop:]
UVy1 = UVy[:pop]
UVy2 = UVy[pop:]
plt.plot(UVx1, UVy1, linewidth=3, label="Measured UV (ascent)")
plt.plot(UVx2, UVy2, linewidth=3, label="Measured UV (descent)")
plt.xlabel("Altitude (meters)", fontsize=30)
plt.ylabel("UV Intensity (W/m$^2$)", fontsize=30)
plt.tick_params(axis='both', which='major', labelsize=20)
plt.legend(prop={'size':24}, loc="Upper Left")
plt.grid()
plt.show()

# Plot Ozone
plt.figure(3)
popO = 10400
Ozonex1 = currentAlt[:popO]
Ozonex2 = currentAlt[popO:]
Ozoney1 = currentOzone[:popO]
Ozoney2 = currentOzone[popO:]
plt.plot(Ozonex1, Ozoney1, linewidth=3, label="Measured ozone (ascent)")
plt.plot(Ozonex2, Ozoney2, linewidth=3, label="Measured ozone (descent)")
plt.xlabel("Altitude (meters)", fontsize=30)
plt.ylabel("Ozone Intensity", fontsize=30)
plt.tick_params(axis='both', which='major', labelsize=20)
plt.legend(prop={'size':24}, loc="Upper Left")
plt.grid()
plt.show()
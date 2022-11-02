"""This script creates a 2D colormap plot from a set of two-column datasets.
Created for plotting of X-ray powder diffraction data, the script can easily 
be modified to accommodate any task with a similar structure of data. 
"""

from matplotlib import cm
from matplotlib import colors
import matplotlib.pyplot as plt
import numpy as np
import matplotlib.ticker as ticker

# creating function for secondary X axis; this step is optional
def thetatoq(x):
    return 4/0.7093*np.pi*np.sin(np.deg2rad(x/2))

def qtotheta(x):
    return 2*np.rad2deg(np.arcsin(x*0.7093/4/np.pi))

j = 0 # file counter
N = 778 # number of points on X axis
N2 = 19 # number of flies, i.e. number of points on Y axis
x = np.linspace(2.4000000000000004E+000, 4.1250000000000000E+001, N) # Xmin, Xmax, number of points
y = np.linspace(20, 210, N2) # Ymin, Ymax, number of points
z = []
A = np.zeros([N2, N])

# filling each point of the N × N2 mesh with a value
for i in range(20, 210, 10):
    Z = []
    file_no = (str(j))
    data = np.genfromtxt('DF598_kapton05_30-200dC_%s_0001.sfrm.txt'%file_no)
    for line in data:
        Z.append(line[1])
    A[j, :] = Z
    j = j+1

# setting up the plot
X, Y = np.meshgrid(x,y)
fig, ax = plt.subplots()
secax = ax.secondary_xaxis('top', functions=(thetatoq, qtotheta))
secax.set_xlabel(r'Q, Å$^{\rm -1}$')
ax.xaxis.set_minor_locator(ticker.MultipleLocator(1))
secax.xaxis.set_major_locator(ticker.MultipleLocator(1))
secax.xaxis.set_minor_locator(ticker.MultipleLocator(0.2))
cs = ax.pcolormesh(X, Y, A, norm=colors.PowerNorm(gamma=0.55),cmap=cm.jet, shading='gouraud')
cbar = fig.colorbar(cs, pad=0.035)
cbar.set_label('Intensity')
cbar.set_ticks([])
plt.xlim(2.4, 20)
plt.ylim(20,210)
plt.xlabel('2θ,°')
plt.ylabel('Temperature, °C')

# saving and showing the result
plt.savefig('plot.png', dpi=600)
plt.show()

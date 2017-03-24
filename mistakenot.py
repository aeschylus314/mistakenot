#   Name    : mistakenot 
#   Function: Provides multi-species particle balance by grid zone. Includes total particles,
#		total neutral particles, and total recycling sources for each species.	
#   Contains   :        class FluxRibbon
#   Functions  : 	explainname()
#			importribbon(start, finish, tag, length = 200)
#			
#  
#   Author: Ian Waters --iwaters@wisc.edu
#   GitHub Page: https://github.com/aeschylus314/mistakenot



def explainname():
	print ("""'Mistake Not' is the name of a Culture warship in the novel The Hydrogen Sonata. I was originally going to title the module 'analysisian.py' and then import it as 'ai'. 'AI' like artifical intelligence, like a self aware ship mind. So import mistakenot as ai. Too clever by half I know.""")

from mpl_toolkits.mplot3d import Axes3D
import matplotlib.pyplot as plt
import matplotlib
from matplotlib import cm
from matplotlib.ticker import LinearLocator, FormatStrFormatter
import numpy as np

# Flux Ribbon class allows for easier plotting. Contains a default plot and all of the arrays
# to easily plot multiple ribbons in a way that is transparent.

class FluxRibbon:
	
# Initialization of a Flux Ribbon
	def __init__(self, density=0, temp=0, plaspres=0, flow=0, source =0, length=0, radius=0, start=[0,0,0], finish=[0,0,0]):

		self.density=density
		self.temp=temp
		self.plaspres=plaspres
		self.flow=flow
		self.source=source
		self.length=length
		self.radius=radius
		self.start=start
		self.finish=finish

# Default plot of a ribbon displays density, ion temperature, plasma pressure, and Mach flow.
# Each subplot has its own colorbar.
# TODO: Need to make the min/maxes easier to change.
	def plt(self, density=0,temp=0, plaspres=0, flow=0, title=None):

		# Set up overall figure
		fig, axes = plt.subplots(figsize=(26, 6), ncols=4, nrows=1)
		fig.suptitle(title, fontsize='xx-large')
		ax1, ax2, ax3, ax4 = axes.flatten()
		for ax in axes.flatten():
			ax.set_ylim(-400, 400)
			ax.set_xlim(19.6, 20.4)
		# Plot Density
		density = ax1.pcolormesh(self.radius, self.length,self.density, vmin=1E12, vmax=1E14, cmap='viridis', shading='flat')
		cb = fig.colorbar(density,shrink=0.75, aspect=8, ax=ax1)
		cb.set_label('Density[cm^-3])')
		ax1.set_title('Density')
		# Plot temperature
		temp = ax2.pcolormesh(self.radius, self.length,self.temp,vmin=10,vmax=50, cmap='inferno', shading='flat')
		cb = fig.colorbar(temp,shrink=0.75, aspect=8, ax=ax2)
		cb.set_label('Temp[eV])')
		ax2.set_title('Temperature')
		# Plot Static Plasma Pressure
		plaspres = ax3.pcolormesh(self.radius, self.length, self.plaspres, vmin=5E14, vmax=5E15, cmap='plasma', shading='flat')
		cb = fig.colorbar(plaspres,shrink=0.75, aspect=8, ax=ax3)
		cb.set_label('Pressure [eV/cm^3]')
		ax3.set_title('Static Pressure')
		# Plot Mach flow. Don't change vmin/vmax
		flow = ax4.pcolormesh(self.radius, self.length,self.flow,cmap=cm.coolwarm, vmin=-1,vmax=1, shading='flat')
		cb = fig.colorbar(flow,shrink=0.75, aspect=8, ax=ax4)
		cb.set_label('M')
		ax4.set_title('MachFlow')
		# Routine will display plot. May want to add print vs. save
		plt.show()
		
		return


# importribbon is a function that imports a set of emc3_eirene post processing outputs
# and turns them into a usable fluxribbon object. Then they can be plotted and manipulated
# in a more straightforward and transparent way than by doing it manually.
# The start and finish parameters should be radial positions in mm. The tag is then the
# string or number that is being used to differentiate the post processing files.
# Should lool like: test_fl_plasma_mmmtag.txt
def importribbon(start, finish, tag, length = 200):

	# Initialize arrays
	width = finish-start + 1
	n = 0
	L=np.ones([length,width])      # Length along field line
	R=np.ones([length,width])      # Original Radial start point
	N=np.ones([length,width+1])    # Density
	Ti=np.ones([length,width+1])   # Ion Temp
	Te=np.ones([length,width+1])   # Electron Temp
	FL=np.ones([length,width+1])   # Mach Flow
	S=np.ones([length,width+1])    # Plasma Source

	# Loop through data files to populate arrays with plasma data
	while n < width:
		targetname=str(start+n)
		target = 'test_fl_plasma_'+targetname+tag+'.txt'
		targetdata = np.loadtxt(target)
		L[:,n]=targetdata[:,0]
		R[:,n]=(start+n)/10
		FL[:,n]=targetdata[:,3]
		S[:,n]=targetdata[:,4]
		Ti[:,n]=targetdata[:,2]
		Te[:,n]=targetdata[:,9]
		N[:,n]=targetdata[:,1]
		n=n+1
	
	# Set the last column in the data files to be the length variable
	N[:,width] = targetdata[:,0]
	S[:,width] = targetdata[:,0]
	Ti[:,width] = targetdata[:,0]
	Te[:,width] = targetdata[:,0]
	FL[:,width] = targetdata[:,0]

	# Use that length value to sort the data from the beginning of the ribbon to the end.
	# The EMC3 routine starts at zero, goes one way, then comes back to zero and goes the 
	# other way. This gets it to plot correctly in the colormap.
	N=N[np.argsort(N[:,width])]
	S=S[np.argsort(S[:,width])]
	Ti=Ti[np.argsort(Ti[:,width])]
	Te=Te[np.argsort(Te[:,width])]
	FL=FL[np.argsort(FL[:,width])]
	L=L[np.argsort(L[:,0])]
	
	# Strip the length column back out so you're left with only the right data.
	Ti=Ti[:,0:width]
	Te=Te[:,0:width]
	N=N[:,0:width]
	S=S[:,0:width]
	FL=FL[:,0:width]

	# Calculate plasma pressure	
	P = np.multiply(N,Te+Ti)
	
	# Create a new flux ribbon objext using the data in the arrays.
	ribbon = FluxRibbon(density=N, temp = Ti, source=S, flow = FL, plaspres = P, length = L, radius =R)
		
	return ribbon




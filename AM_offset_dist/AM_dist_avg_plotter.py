#!/usr/bin/python
import os
import matplotlib.pyplot as plt
from matplotlib import rc
from itertools import cycle

#Plots the histograms for average jobs at distance t from AM for both actors and actresses.

#Functions.

def get_data(loc):
	
	f = open(loc, 'r')
	
	data_vals = []
	
	for line in f:
		if len(line) > 0:
			dum_line = line.split('\t')
			x_val = float(dum_line[0])
			y_val = float(dum_line[1][0:-1])		#Ignore trailing \n.
	
			data_vals.append([x_val,y_val])
	
	return data_vals


def plot_pair(dat_1,dat_2,out_loc):
	
	x_1 = [x[0] for x in dat_1]
	y_1 = [x[1] for x in dat_1]
	
	x_2 = [x[0] for x in dat_2]
	y_2 = [x[1] for x in dat_2]
	
	rc('font', **{'family':'serif','serif':['Palatino']})
	rc('text', usetex=True)
	
	colours = cycle(["aqua", "black", "blue", "fuchsia", "gray", "green", "lime", "maroon", "navy", "olive", "purple", "red", "silver", "teal", "yellow"])
	
	fig = plt.figure()
	ax = fig.add_subplot(111)
	
	ax.plot(x_1,y_1, color = next(colours), label = 'actors')
	ax.plot(x_2,y_2, color = next(colours), label = 'actresses')
			
	ax.set_xlabel(r"offset", fontsize=18)
	ax.set_ylabel(r"Average", fontsize=18)
	
	#ax.set_xscale("log", nonposx='clip')
	ax.set_yscale("log", nonposy='clip')
	
	ax.legend(loc="best")
	
	#title = "Infected Fraction VS Time for various p\n y = "+str(y)+" q = "+str(q)+" l = " +str(l)
	#plt.title(title)
	
	ax.margins(0.1)
	#fig.tight_layout()
	
	fig_name = 'AM_dist_avg_comp_shuffle.eps'
	
	save_name = os.path.join(out_loc, fig_name)
	
	plt.savefig(save_name, format='eps', dpi=1000)
	
	plt.close("all")
	







#Main.

#Location of data files for AM distributions.

#Current data is shuffled ``null model" version, can be changed to non-shuffled data.
d_loc_1 = "actors_AM_dist_avg_shuffle.txt"
d_loc_2 = "actresses_AM_dist_avg_shuffle.txt"

#Location of desired output for AM distribution histograms.
out_loc = "AM_dist_avg_data"

vals_1 = get_data(d_loc_1)
vals_2 = get_data(d_loc_2)

plot_pair(vals_1,vals_2,out_loc)
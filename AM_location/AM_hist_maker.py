#!/usr/bin/python
from __future__ import division
import os
import matplotlib.pyplot as plt
from matplotlib import rc
from itertools import cycle
import numpy as np

#Program plots two histograms against each other.

#Functions.

def get_data(loc):
	
	f = open(loc, 'r')
	
	data_vals = []
	
	for line in f:
		if len(line) > 0:
			dat_point = float(line[0:-1])
			
			data_vals.append(dat_point)
				
	return data_vals


def get_centers(bins):
	
	c_vals = []
	
	#shift = 0.0
	
	for i in xrange(len(bins) - 1):
		shift = bins[i]
		mid = (bins[i+1] - bins[i])/2
		c_vals.append(mid+shift)
	return c_vals	


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
			
	ax.set_xlabel(r"period bin", fontsize=18)
	ax.set_ylabel(r"Probability", fontsize=18)
	
	#ax.set_xscale("log", nonposx='clip')
	#ax.set_yscale("log", nonposy='clip')
	
	ax.legend(loc="best")
	
	#plt.title(title)
	
	ax.margins(0.1)
	#fig.tight_layout()
	
	fig_name = 'AM_hist_last_bins_'+str(bin_no)+'.eps'
	
	save_name = os.path.join(out_loc, fig_name)
	
	plt.savefig(save_name, format='eps', dpi=1000)
	
	plt.close("all")


#Main.

bin_no = 5

#Path to actors (or actresses) AM location data file.
d_loc_1 = "actors_AM_locs_last.txt"
d_loc_2 = "actresses_AM_locs_last.txt"

#Desired output location for AM location histograms.
out_loc = "/AM_loc_data"

vals_1 = get_data(d_loc_1)
vals_2 = get_data(d_loc_2)

#Got the values now get the two histograms.
vals_1,bins_1 = np.histogram(vals_1,bin_no)
v_sum_1 = sum(vals_1)
n_vals_1 = [x/v_sum_1 for x in vals_1]
c_bins_1 = get_centers(bins_1)

vals_2,bins_2 = np.histogram(vals_2,bin_no)
v_sum_2 = sum(vals_2)
n_vals_2 = [x/v_sum_2 for x in vals_2]
c_bins_2 = get_centers(bins_2)

hist_dat_1 = zip(c_bins_1,n_vals_1)
hist_dat_2 = zip(c_bins_2,n_vals_2)

plot_pair(hist_dat_1,hist_dat_2,out_loc)
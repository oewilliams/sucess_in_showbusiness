#!/usr/bin/python
from __future__ import division
from collections import Counter
import numpy as np
import os
import matplotlib.pyplot as plt
from matplotlib import rc
from itertools import cycle


#Program gets pdf of number of years with jobs for either actors or actresses.

#Get data from date series with names striped.
def get_data(loc,cutoff=0):
	
	f = open(loc,'r')
	
	ranges = []
	
	for line in f:
		if len(line) > 1:
			if '\t' in line:
				dum_dat = line.split('\t')[0:-1]		#Ignore ending \n caracter.
				dat_line = [int(x) for x in dum_dat]
				dat_line_strip = [int(x) for x in dum_dat if int(x) != 0]
				r_val = float(len(dat_line_strip)+1)/float(len(dat_line)+1)
			else:
				dat_line_strip = [1]
				r_val = 1
			
			if len(dat_line_strip) < cutoff:			
				ranges.append(r_val)
				
	return ranges

def get_bins(bin_count):
	
	step = 1/bin_count
	
	bins = [0.0]
	
	for i in xrange(bin_count):
		bins.append(bins[i] + step)
		
	return bins
	

#Get the histogram values and bin centers.
def get_hist(data,bin_set):
	
	vals,bins = np.histogram(data,bins=bin_set)
	
	sum_val = sum(vals)
	norm_vals = [x/sum_val for x in vals]
	
	
	return bins,norm_vals


def get_comp_dist(D_range, bin_set):
	
	fracs = [1]

	for d in D_range:
		for n in range(2,d+1):
			fracs.append(n/d)
		
		
	vals,bins = np.histogram(fracs,bins=bin_set)
	
	sum_val = sum(vals)
	norm_vals = [x/sum_val for x in vals]
		
	return bins, norm_vals

def get_mids(bins):
	
	bin_mids = []
		
	for i in xrange(len(bins)-1):
		mid = (bins[i+1]-bins[i])/2
		bin_mids.append(mid+bins[i])
	
	return bin_mids


def scale_values(mids_1, vals_1, mods_c, vals_c):
	
	scaled_vals = []
	
	for i in xrange(len(vals_1)):
		if vals_c[i] != 0:
			scaled_vals.append(vals_1[i]/vals_c[i])
		else:
			scaled_vals.append(-1)
	
	return scaled_vals
			

def write_to_file(bins,vals,loc,identifier):
	
	f_name = identifier + "_s_L_frac_"+str(bin_count)+"_bins.txt"
	
	f = os.path.join(loc, f_name)
	
	out = open(f,'w')
	
	for i in xrange(len(bins)):
		out.write(str(bins[i]) +'\t'+ str(vals[i]) + '\n')
	
	out.close()


def plot_set(dat_1,dat_2,dat_3,out_loc):
	
	x_1 = [x for x in dat_1[0]]
	y_1 = [x for x in dat_1[1]]
	
	print len(x_1),len(y_1)

	
	x_2 = [x for x in dat_2[0]]
	y_2 = [x for x in dat_2[1]]
	
	x_3 = [x for x in dat_3[0]]
	y_3 = [x for x in dat_3[1]]
	
	#print len(x_1),len(y_1)
	
	rc('font', **{'family':'serif','serif':['Palatino']})
	rc('text', usetex=True)
	
	colours = cycle(["aqua", "black", "blue", "fuchsia", "gray", "green", "lime", "maroon", "navy", "olive", "purple", "red", "silver", "teal", "yellow"])
	
	fig = plt.figure()
	ax = fig.add_subplot(111)
	
	ax.plot(x_1,y_1, color = next(colours), label = 'actors')
	ax.plot(x_2,y_2, color = next(colours), label = 'actresses')
	ax.plot(x_1,y_3, color = next(colours), label = 'uniform')
			
	ax.set_xlabel(r"$s/L$", fontsize=18)
	ax.set_ylabel(r"$P(s/L)$", fontsize=18)
	
	#ax.set_xscale("log", nonposx='clip')
	ax.set_yscale("log", nonposy='clip')
	
	ax.legend(loc="best")
	
	#title = "Infected Fraction VS Time for various p\n y = "+str(y)+" q = "+str(q)+" l = " +str(l)
	#plt.title(title)
	
	ax.margins(0.1)
	#fig.tight_layout()
	
	if CLIP_1:
		fig_name = "work_frac_pdf_base_comp_clip_b_"+str(bin_count)+".eps"
	else:
		fig_name = "work_frac_pdf_base_comp_b_"+str(bin_count)+".eps"
		
	
	save_name = os.path.join(out_loc, fig_name)
	
	plt.savefig(save_name, format='eps', dpi=1000)
	
	plt.close("all")


#Main.
global CLIP_1
CLIP_1 = False

global bin_count
bin_count = 500

#Path to actors and actresses working count data.
data_loc_1 = "Actresses_count_series_name_strip.txt"
data_loc_2 = "Actors_count_series_name_strip.txt"

#Location of desired folder for output of activity density function data.
out_loc = "/activity_pdf_data"


cutoff = 100				#Maximum career lenght to consider.

data_1 = get_data(data_loc_1,cutoff)
data_2 = get_data(data_loc_2,cutoff)

bins_1 = get_bins(bin_count)

bins_1,vals_1 = get_hist(data_1, bins_1)
bins_2,vals_2 = get_hist(data_2, bins_1)

x_base,y_base = get_comp_dist(xrange(cutoff),bins_1)

mids_1 = get_mids(bins_1)
mids_2 = get_mids(bins_2)
mids_3 = get_mids(x_base)

plot_set([mids_1,vals_1],[mids_2,vals_2],[mids_3,y_base],out_loc)

#print mids_3
#print y_base

write_to_file(mids_1,vals_1,out_loc,"Actors")
write_to_file(mids_2,vals_2,out_loc,"Actresses")
write_to_file(mids_3,y_base,out_loc,"comparison")

scale_v_1 = scale_values(mids_1,vals_1,mids_3,y_base)
scale_v_2 = scale_values(mids_2,vals_2,mids_3,y_base)

write_to_file(mids_1,scale_v_1,out_loc,"Actors_scaled")
write_to_file(mids_2,scale_v_2,out_loc,"Actresses_scaled")
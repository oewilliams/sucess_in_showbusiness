#!/usr/bin/python
from __future__ import division
from collections import Counter
import numpy as np

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


#Get the histogram values and bin centers.
def get_hist(data):
	
	vals,bins = np.histogram(data,bins=bin_count)
	
	sum_val = sum(vals)
	norm_vals = [x/sum_val for x in vals]
	
	bin_mids = []
	
	for i in xrange(len(bins)-1):
		mid = (bins[i+1]-bins[i])/2
		bin_mids.append(mid+bins[i])
	
	return bin_mids,norm_vals
			

def write_to_file(bins,vals,loc):
	
	out = open(loc,'w')
	
	for i in xrange(len(bins)):
		out.write(str(bins[i]) +'\t'+ str(vals[i]) + '\n')
	
	out.close()

#Main.

global bin_count
bin_count = 250

#Path to actors (or actresses) working count data.
data_loc = "Actresses_count_series_name_strip.txt"

#Location of desired output file for bined working fraction density function.
out_loc = "actresses_work_frac_pdf_b_"+str(bin_count)+".txt"


cutoff = 100				#Maximum career lenght to consider.

data = get_data(data_loc,cutoff)

bins,vals = get_hist(data)

write_to_file(bins,vals,out_loc)
#!/usr/bin/python
from __future__ import division
from collections import Counter

#Program gets pdf of number of years with jobs for either actors or actresses.

#Get data from date series with names striped.
def get_data(loc):
	
	f = open(loc,'r')
	
	ranges = []
	
	for line in f:
		if len(line) > 1:
			if '\t' in line:
				dum_dat = line.split('\t')[0:-1]		#Ignore ending \n caracter.
				dat_line = [int(x) for x in dum_dat if int(x) != 0]
				r_val = len(dat_line) + 1
				if r_val == 1:
					print repr(line), dum_dat
			else:
				r_val = 1
			
			if r_val == 0:
				print line
			ranges.append(r_val)

	
	return ranges


#Get the histogram values and bin centers.
def get_hist(data,cutoff):
	#DUM VERSION FIRST TO SEE IF IT WORKS!!!
	count_dict = Counter(data)
	
	bins = []
	vals = []
	
	for x in sorted(count_dict.keys()):
		if x <= cutoff:
			bins.append(x)
			vals.append(count_dict[x])
			#print bins[-1],vals[-1]
	sum_val = sum(vals)
	norm_vals = [x/sum_val for x in vals]
	
	return bins,norm_vals
			

def write_to_file(bins,vals,loc):
	
	out = open(loc,'w')
	
	for i in xrange(len(bins)):
		out.write(str(bins[i]) +'\t'+ str(vals[i]) + '\n')
	
	out.close()

#Main.

#Path to actresses (or actors) working count series.
data_loc = "Actresses_count_series_name_strip.txt"
out_loc = "actresses_working_years_pdf.txt"

data = get_data(data_loc)

cutoff = 100				#Maximum career lenght to consider.

bins,vals = get_hist(data,cutoff)

write_to_file(bins,vals,out_loc)
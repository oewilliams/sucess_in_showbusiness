#!/usr/bin/python
from __future__ import division
from collections import Counter

#Program gets pdf of number of years over carreer for either actors or actresses.

#Get data from date series with names striped.
def get_data(loc):
	
	f = open(loc,'r')
	
	ranges = []
	
	for line in f:
		if len(line) > 0:
			if '\t' in line:
				dum_dat = line.split('\t')[0:-1]		#Ignore ending \n caracter.
				dat_line = [int(x) for x in dum_dat]
				r_val = len(dat_line)+1
			else:
				r_val = 1
			
			if r_val == 0:
				print line
			ranges.append(r_val)

	
	return ranges


#Get the histogram values and bin centers.
def get_hist(data,cutoff):
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

#Path to actors (or actresses) working count series data. 
data_loc = "Actresses_count_series_name_strip.txt"

#Location of desired output for total working years data.
out_loc = "actresses_total_years_pdf.txt"

data = get_data(data_loc)

cutoff = 800				#Maximum career lenght to consider.

bins,vals = get_hist(data,cutoff)

print vals

#write_to_file(bins,vals,out_loc)
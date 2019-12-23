#!/usr/bin/python
from __future__ import division
from collections import Counter
import os
import matplotlib.pyplot as plt
from matplotlib import rc
from itertools import cycle
#Program finds positions of the first and last AM in each actor or actresses career.

#Get data from date series with names striped.

#Get the AM for a sequence.
def get_AM(X,rev_check=True):
	max_val = max(X)
	if rev_check:
		rev = X[::-1]		#Reverse list.
		AM_rev = rev.index(max_val)			#Get the location of the last AM (first in reversed sequence).
		
		AM_val = len(X) - AM_rev - 1			#Index of last AM in foward sequence.
	else:
		AM_val = X.index(max_val)
	
	return AM_val
	
#Get the location of the first and last AM, along with career length.
def get_data(loc, len_cutoff, AM_cutoff):
	
	f = open(loc,'r')
	
	locs = []
	
	for line in f:
		if len(line) > 0:
			dum_dat = line.split('\t')		
			dum_dat[-1] = dum_dat[-1][0:-1]	#Remove \n.

			dat_line = [int(x) for x in dum_dat]
			
			AM_f = get_AM(dat_line,False)
			AM_l = get_AM(dat_line,True)
			
			if (dat_line[AM_f] >= AM_cutoff) and (len(dat_line) >= len_cutoff):
			
				locs.append([AM_f,AM_l,len(dat_line)])
	
	return locs


#Main.

#Path to actors (or actresses working count series.
data_loc = "Actors_count_series_name_strip.txt"

#Path to desired output file for actors (or actresses) AM location.
out_loc_f = "actors_AM_locs_first.txt"
out_loc_l = "actors_AM_locs_last.txt"


AM_cutoff = 5
len_cutoff = 20

data = get_data(data_loc, len_cutoff, AM_cutoff)

#Get the fraction through the career the first and last AM is at and write to file.

out_f = open(out_loc_f,'w')
out_l = open(out_loc_l,'w')

fracs_f = []
fracs_l = []
for x in data:
	frac_f = x[0]/x[2]
	frac_l = x[1]/x[2]
	
	fracs_f.append(frac_f)
	fracs_l.append(frac_l)
	
	out_f.write(str(frac_f) + '\n')
	out_l.write(str(frac_l) + '\n')

out_f.close()
out_l.close()


#Write to file.






#!/usr/bin/python
from __future__ import division
from random import shuffle
#Program gets distributions of average number of jobs before and after AM up.

#SHUFFLE VERSION: shuffle interior of each career.

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


def shuffle_line(data):
	
	first = data[0]
	last = data[-1]
	
	mid = data[1:-1]
	shuffle(mid)
	
	new_data = [first] + mid + [last]
	
	return new_data
	
	
#Get the location of the first and last AM, along with career length.
def get_shuffled_data(loc, len_cutoff, AM_cutoff):
	
	f = open(loc,'r')
	
	seqs = []
	
	for line in f:
		if len(line) > 0:
			dum_dat = line.split('\t')		
			dum_dat[-1] = dum_dat[-1][0:-1]	#Remove \n.

			dat_line = [int(x) for x in dum_dat]
			
			dat_line = shuffle_line(dat_line)
			
			AM_f = get_AM(dat_line,False)
			AM_l = get_AM(dat_line,True)
			
			if (dat_line[AM_f] >= AM_cutoff) and (len(dat_line) >= len_cutoff):
			
				seqs.append([AM_f,AM_l,dat_line])
	
	return seqs


#Get the avg counts about first and last AM.
def get_samp_dicts(X,t_range):
	
	AM = X[1]
	seq = X[2]
	
	s_d = {}
	c_d = {}
	
	for i in range(-t_range, t_range+1):
		try:
			s_d[i] = seq[AM - i]
			c_d[i] = 1
		except:
			s_d[i] = 0
			c_d[i] = 0
	
	return s_d,c_d


#Add the contents of two dictionaries together.
def dict_add(x,y):
	out_dict = {}
	for key in x.keys():
		out_dict[key] = x[key] + y[key]
	
	return out_dict



#Main.

#Path to actors (or actresses) working count series data.
data_loc = "Actresses_count_series_name_strip.txt"

#Location of desired output for shuffled AM distribution data.
out_loc = "/actresses_AM_dist_avg_shuffle.txt"


AM_cutoff = 5
len_cutoff = 20

t_range = 10			#Distance away from AM to look at.

#Initialise dict for counting jobs.
samp_size = {}				#Dict for counting number of actors with valid counts in each bin.
count_dict = {}
for i in range(-t_range,t_range+1):
	count_dict[i] = 0
	samp_size[i] = 0

data = get_shuffled_data(data_loc, len_cutoff, AM_cutoff)
points = len(data)

dum_dict = {}
dum_samp = {}
for x in data:
	dum_dict, dum_samp = get_samp_dicts(x,t_range)
	count_dict = dict_add(count_dict, dum_dict)
	samp_size = dict_add(samp_size, dum_samp)

out = open(out_loc,'w')

for x in sorted(count_dict.keys()):
	count_dict[x] = count_dict[x]/samp_size[x]
	
	out.write(str(x) + '\t' + str(count_dict[x]) + '\n')

out.close()
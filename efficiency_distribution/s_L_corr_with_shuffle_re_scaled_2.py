#!/usr/bin/python
from __future__ import division
import numpy as np
import matplotlib.pyplot as plt
from matplotlib import rc
import os
import random


#Program finds the correlation between s and L for either actors or actresses.
#Also finds a shuffled comparison.

#VERSION PLOTS RE-SCALED SCATTER
#ALSO CLEANING OFFLOADED TO OTHER FUNCTION.


#Get data from date series with names striped.
def get_data(loc):
	
	f = open(loc,'r')
	
	ranges = []
	
	for line in f:
		if len(line) > 1:
			if '\t' in line:
				dum_dat = line.split('\t')[0:-1]		#Ignore ending \n caracter.
				dat_line = [int(x) for x in dum_dat]
				dat_line_strip = [int(x) for x in dum_dat if int(x) != 0]
				r_val = (len(dat_line_strip)+1,len(dat_line)+1)
			else:
				dat_line_strip = [1]
				r_val = (1,1)
			
			ranges.append(r_val)
	
	return ranges

def clean_data(data, cuttoff = 0, clip=False):
	
	clean_list = []
	
	for x in data:
		if x==(1,1):
			if clip == False:
				clean_list.append(x)
		elif x[1] < cutoff:
			clean_list.append(x)
	return clean_list

def re_scale(data):
	new_data = []
	
	for x in data:
		dum_pair = (x[0]/x[1], x[1])
		new_data.append(dum_pair)
	
	return new_data	
	
"""
def re_scale(data):
	
	new_data = []
	shift_vals = [x[1]-x[0] for x in data]
	
	s_mean = np.average(shift_vals)
	re_scaled_s_vals = [x-s_mean for x in shift_vals]
	
	for i in xrange(len(data)):
		new_data.append((re_scaled_s_vals[i],data[i][1]))
	
	return new_data
"""

def get_corr(data):
	X = [x[0] for x in data]
	Y = [x[1] for x in data]
	
	m_x = np.mean(X)
	m_y = np.mean(Y)
	s_x = np.std(X)
	s_y = np.std(Y)
	
	count = 0
	sum_term = 0.0
	for i in xrange(min(len(X),len(Y))):
		sum_term += (X[i] - m_x)*(Y[i]-m_y)
		count += 1
	
	corr = sum_term/(count * s_x * s_y)
	
	return corr

"""
def shuffle_set(data):
	L_list = [x[0] for x in data]
	s_list = [x[1] for x in data]
	
	random.shuffle(s_list)
	
	return zip(L_list, s_list)
"""

def shuffle_set(data):
	
	l = len(data)
		
	L_list = [x[1] for x in data]
	s_list = [x[0] for x in data]
	
	for i in xrange(shuffle_times):
		
		accept_s = False
		while not accept_s:
			r_1 = random.randint(0,l-1)
			r_2 = random.randint(0,l-1)
			
			if r_1 != r_2:
				s_1 = s_list[r_1]
				s_2 = s_list[r_2]
				L_1 = L_list[r_1]
				L_2 = L_list[r_2]
								
				if s_1 <= L_2 and s_2 <= L_1:
					dum = s_2
					s_list[r_2] = s_1
					s_list[r_1] = dum
					accept_s = True
	
	new_data = zip(s_list,L_list)
	
	check = 0
	for x in xrange(l):
		if data[x] == new_data[x]:
			check +=1
	print l, check
	
	return new_data
	

def write_to_file(data,sex,out_loc):
	
	out_file = sex + "_L_and_s_data_clip_no_cut.txt"
	out_name = os.path.join(out_loc,out_file)
	out = open(out_name,'w')
	
	for x in data:
		out.write(str(x[1]) + '\t' + str(x[0]) + '\n') 	
	
	
def scatter_plot(data,corr,sex,out_loc):
	
	data = list(set(data))
	
	X = [x[1] for x in data]
	Y = [x[0] for x in data]
	
	rc('font', **{'family':'serif','serif':['Palatino']})
	rc('text', usetex=True)
	
	fig = plt.figure()
	ax = fig.add_subplot(111)
	
	ax.scatter(X,Y)
	
	ax.set_xlabel(r"$L$", fontsize=18)
	ax.set_ylabel(r"$s/L$", fontsize=18)
	
	title = r"$s/L$ vs $L$ scatter plot for " + str(sex) + "\n correlation coefficient: " + str(corr)
	plt.title(title)
	
	#fig_name = str(sex) + " s_v_L_scatter.eps"
	fig_name = str(sex) + " s_v_L_scatter_re_scaled_clip.png"
	
	save_name = os.path.join(out_loc, fig_name)
	
	#plt.savefig(save_name, format='eps', dpi=1000)
	plt.savefig(save_name, format='png')
	
	plt.close("all")



#Main.

CLIP_1 = True			#Flag for clipping cases where s=L=1.
RESACALE = False
WRITE_TO_FILE = True
RESCALE_WRITE = True
SHUFFLE_WRITE = True

#Path to actors and actresses working count data.
data_loc_1 = "Actresses_count_series_name_strip.txt"
data_loc_2 = "Actors_count_series_name_strip.txt"

#Location of desired folder for correlation data outputs/plots.
out_loc = "corr_data"


global shuffle_times
shuffle_times = 10000000
cutoff = 100				#Maximum career lenght to consider.

data_1 = get_data(data_loc_1)
data_2 = get_data(data_loc_2)

data_1 = clean_data(data_1, cutoff, CLIP_1)
data_2 = clean_data(data_2, cutoff, CLIP_1)

if WRITE_TO_FILE:
	write_to_file(data_1,"Actresses",out_loc)
	write_to_file(data_2,"Actors",out_loc)

if RESACALE:
	re_scaled_data_1 = re_scale(data_1)
	re_scaled_data_2 = re_scale(data_2)
	
	if RESCALE_WRITE:
		write_to_file(re_scaled_data_1, "Actresses_re_scaled", out_loc)
		write_to_file(re_scaled_data_2, "Actors_re_scaled", out_loc)
	
else:
	re_scaled_data_1 = data_1
	re_scaled_data_2 = data_2
	
corr_1 = get_corr(re_scaled_data_1)
corr_2 = get_corr(re_scaled_data_2)

s_data_1 = shuffle_set(re_scaled_data_1)
s_data_2 = shuffle_set(re_scaled_data_2)

if SHUFFLE_WRITE:
	write_to_file(s_data_1, "nullActresses", out_loc)
	write_to_file(s_data_2, "nullActors", out_loc)

corr_1_s = get_corr(s_data_1)
corr_2_s = get_corr(s_data_2)

print corr_1, corr_2, corr_1_s, corr_2_s

#print corr_1, corr_2
scatter_plot(re_scaled_data_1, corr_1, "Actresses", out_loc)
scatter_plot(re_scaled_data_2, corr_2, "Actors", out_loc)

scatter_plot(s_data_1, corr_1_s, "nullActresses", out_loc)
scatter_plot(s_data_2, corr_2_s, "nullActors", out_loc)

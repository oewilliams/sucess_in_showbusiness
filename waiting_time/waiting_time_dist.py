#!/usr/bin/python
from __future__ import division
from collections import Counter
import os
import matplotlib.pyplot as plt
from matplotlib import rc
from itertools import cycle
import random

#Program finds the waiting time distribution for either actors or actresses.
#These distributions are complaired to shuffled versions of the same data.

#Functions.

#sequences of activities with length and value cutoff.
def get_data(loc, len_cutoff, val_cutoff):
	
	f = open(loc,'r')
	
	sequences = []
	
	for line in f:
		if len(line) > 0:
			dum_dat = line.split('\t')		
			dum_dat[-1] = dum_dat[-1][0:-1]	#Remove \n.

			dat_line = [int(x) for x in dum_dat if int(x) >= val_cutoff]
			
			if len(dat_line) >= len_cutoff:
			
				sequences.append(dat_line)
	
	return sequences

#Get the set of (non-unique) waiting times.
def get_waiting_times(X):
	
	count = 1
	
	times = []
	
	for x in X:
		if x != 0:
			times.append(count)
			count = 1
		else:
			count += 1
	
	return times

#Shuffle the activity sequence, keeping the first and last values.
def shuffle_seq(X):
	c_X = X[1:-1]
	
	random.shuffle(c_X)
	
	new_seq = [X[0]]+c_X+[X[-1]]
	
	return new_seq
	

def plot_pair(dat_1,dat_2,out_loc, truncate):
	
	dat_1_t = dat_1[0:truncate]
	dat_2_t = dat_2[0:truncate]
	
	x_1 = [x[0] for x in dat_1_t]
	y_1 = [x[1] for x in dat_1_t]
	
	x_2 = [x[0] for x in dat_2_t]
	y_2 = [x[1] for x in dat_2_t]
	
	rc('font', **{'family':'serif','serif':['Palatino']})
	rc('text', usetex=True)
	
	colours = cycle(["aqua", "black", "blue", "fuchsia", "gray", "green", "lime", "maroon", "navy", "olive", "purple", "red", "silver", "teal", "yellow"])
	
	fig = plt.figure()
	ax = fig.add_subplot(111)
	
	ax.plot(x_1,y_1, color = next(colours), label = 'actors')
	ax.plot(x_2,y_2, color = next(colours), label = 'null model')
			
	ax.set_xlabel(r"$\tau$", fontsize=18)
	ax.set_ylabel(r"$P(\tau)$", fontsize=18)
	
	#ax.set_xscale("log", nonposx='clip')
	#ax.set_yscale("log", nonposy='clip')
	
	ax.legend(loc="best")
	
	#title = "Infected Fraction VS Time for various p\n y = "+str(y)+" q = "+str(q)+" l = " +str(l)
	#plt.title(title)
	
	ax.margins(0.1)
	#fig.tight_layout()
	
	fig_name = 'actresses_waiting_dist.eps'
	
	save_name = os.path.join(out_loc, fig_name)
	
	plt.savefig(save_name, format='eps', dpi=1000)
	
	plt.close("all")


def write_to_file(out_loc, f_name, data):
	
	out_f = os.path.join(out_loc,f_name)
	
	out = open(out_f,'w')
	
	for x in data:
		out.write(str(x[0]) + '\t' + str(x[1]) + '\n')
	
	out.close()
	

#Main.

#Path to actresses (or actors) working count series data.
data_loc = "Actresses_count_series_name_strip.txt"

#Location of desired output folder for between-job waiting time data.
out_loc = "/waiting_time_data"

len_cutoff = 10
val_cutoff = 0

truncate = 10				#Max value to plot prob for.

data = get_data(data_loc, len_cutoff, val_cutoff)

waiting_times = []
shuffled_times = []

for x in data:
	waiting_times += get_waiting_times(x)
	shuffled_times += get_waiting_times(shuffle_seq(x))

waiting_count = Counter(waiting_times)
shuffle_count = Counter(shuffled_times)

waiting_probs = []
shuffle_probs = []

total_wait = sum(waiting_count.values())
total_shuffle = sum(shuffle_count.values())

for x in sorted(waiting_count.keys()):
	waiting_probs.append([x,waiting_count[x]/total_wait])

for x in sorted(shuffle_count.keys()):
	shuffle_probs.append([x,shuffle_count[x]/total_shuffle])

write_to_file(out_loc,'actresses_waiting_probs',waiting_probs)
write_to_file(out_loc,'actresses_shuffle_probs',shuffle_probs)

plot_pair(waiting_probs, shuffle_probs, out_loc, truncate)


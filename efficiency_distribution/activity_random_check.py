#!/usr/bin/python
from __future__ import division
from collections import Counter
import numpy as np
import os
import matplotlib.pyplot as plt
from matplotlib import rc
from itertools import cycle
import random


#Program generates sample values for L and s and compares the ratios.
#This is effectively a null model for activity.

def get_corr(X,Y):
	
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


def get_comp_dist(D_range):
	
	fracs = [1]

	for d in D_range:
		for n in range(2,d+1):
			fracs.append(n/d)
		
	counts = Counter(fracs)

	frac_num = len(counts.keys())

	c_sum = sum(counts.values())

	#print frac_num

	norm_counts = []
	x_vals = []
	y_vals = []

	for x in sorted(counts.keys()):
		norm_counts.append([x,counts[x]/c_sum])
		
		x_vals.append(x)
		y_vals.append(counts[x]/c_sum)
	
	return x_vals,y_vals


def get_samp_dist(cutoff,sample):
	
	fracs = []
	s_list = []
	L_list = []
	
	for i in xrange(sample):
		L = random.randint(1,cutoff)
		
		if L == 1:
			s = 1
		else:
			s = random.randint(2,L)
		fracs.append(s/L)
		s_list.append(s)
		L_list.append(L)
	
	
	corr = get_corr(s_list,L_list)
	
	counts = Counter(fracs)

	frac_num = len(counts.keys())

	c_sum = sum(counts.values())

	#print frac_num

	norm_counts = []
	x_vals = []
	y_vals = []

	for x in sorted(counts.keys()):
		norm_counts.append([x,counts[x]/c_sum])
		
		x_vals.append(x)
		y_vals.append(counts[x]/c_sum)
	
	return x_vals,y_vals, corr



def print_pair(dat_1,dat_2,out_loc):
	
	x_1 = [x for x in dat_1[0]]
	y_1 = [x for x in dat_1[1]]
	
	x_2 = [x for x in dat_2[0]]
	y_2 = [x for x in dat_2[1]]

	
	rc('font', **{'family':'serif','serif':['Palatino']})
	rc('text', usetex=True)
	
	colours = cycle(["aqua", "black", "blue", "fuchsia", "gray", "green", "lime", "maroon", "navy", "olive", "purple", "red", "silver", "teal", "yellow"])
	
	fig = plt.figure()
	ax = fig.add_subplot(111)
	
	ax.plot(x_1,y_1, color = next(colours), label = 'comparison')
	ax.plot(x_2,y_2, color = next(colours), label = 'random')
			
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
		fig_name = "random_comp_clip.eps"
	else:
		fig_name = "random_comp.eps"
		
	
	save_name = os.path.join(out_loc, fig_name)
	
	plt.savefig(save_name, format='eps', dpi=1000)
	
	plt.close("all")


#Main.
global CLIP_1
CLIP_1 = False

#Location for desired output folder for random activity data. 
out_loc = "/activity_pdf_data"


cutoff = 100
sample = 100000

D_range = xrange(cutoff)

x_comp, y_comp = get_comp_dist(D_range)

x_samp, y_samp, corr = get_samp_dist(cutoff,sample)

print corr

print_pair([x_comp,y_comp],[x_samp,y_samp], out_loc)



#!/usr/bin/python
from __future__ import division
from collections import Counter
import math

#Program checks for gender bias in activity series. 

#VERSION TWO - mixing of data now done with two sets of x axis, not one.

#Get data from date series with names striped.
def get_data(loc):
	
	f = open(loc,'r')
	
	ranges = []
	
	for line in f:
		if len(line) > 0:
			dum_dat = line.split('\t')[0:-1]		#Ignore ending \n caracter.
			dat_line = [int(x) for x in dum_dat]
			try:
				r_val = dat_line[-1] - dat_line[0]
			except:
				r_val = dat_line[0]
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

def fit_exp(x,y):
	
	l_y = [math.log(z) for z in y]
	
	x_bar = sum(x)/len(x)
	l_y_bar = sum(l_y)/len(l_y)
	
	denom = 0
	numer = 0
	
	for i in xrange(len(x)):
		denom += (x[i] - x_bar)*(l_y[i] - l_y_bar)
		numer += (x[i] - x_bar)*(x[i] - x_bar)
	
	m = denom/numer
	b = l_y_bar - (m*x_bar)
	
	return math.exp(b),m

#Get the AIC value.
def get_AIC(c,a, bins, vals):
	k = 2						#value left for later flexibility.
	
	points = len(bins)
	
	MSE = 0.0
	
	for i in xrange(points):
		l_term = math.log(vals[i]) - math.log(c) - (a*bins[i])
		MSE += l_term * l_term
	
	MSE = MSE/points
	
	AIC = (2*k) + (2 * points * math.log(MSE))
	
	return AIC

def get_bi_AIC(c_1,a_1,c_2,a_2, bins_1, bins_2, vals_1, vals_2):
	
	k = 4
	
	MSE = 0.0
	
	p_1 = len(bins_1)
	p_2 = len(bins_2)
	
	N = p_1 + p_2
	
	sum_1 = 0.0
	for i in xrange(p_1):
		l_term = math.log(vals_1[i]) - math.log(c_1) - (a_1*bins_1[i])
		sum_1 += l_term * l_term
	
	sum_2 = 0.0
	for i in xrange(p_2):
		l_term = math.log(vals_2[i]) - math.log(c_2) - (a_2*bins_2[i])
		sum_2 += l_term * l_term
	
	MSE = (sum_1 + sum_2)/N
		
	AIC = (2*k) + (2 * N * math.log(MSE))
	
	return AIC	

#Main.

#Location of actors and actresses working date series data.
data_loc_m = "Actors_date_series_name_strip.txt"
data_loc_f = "Actresses_date_series_name_strip.txt"

#Potential output location for activity density function if required.
#out_loc = "/actresses_activity_pdf.txt"

data_m = get_data(data_loc_m)
data_f = get_data(data_loc_f)

cutoff = 100				#Maximum career lenght to consider.

bins_m,vals_m = get_hist(data_m[1:],cutoff)
bins_f,vals_f = get_hist(data_f[1:],cutoff)

c_m,a_m = fit_exp(bins_m,vals_m)
c_f,a_f = fit_exp(bins_f,vals_f)

bins_mix = bins_m + bins_f
vals_mix = vals_m + vals_f

c_h,a_h = fit_exp(bins_mix,vals_mix)

print "Exp fit vals"
print "male: c_m " +str(c_m) + '\ta_m ' + str(a_m)
print "female: c_f " +str(c_f) + '\ta_f ' + str(a_f)
print "mixed: c_h " +str(c_h) + '\ta_h ' + str(a_h)

"""
#Introduce lucas's values for testing.
c_h = 0.02306
a_h = -0.07673
c_f = 0.02232
a_f = -0.07768
c_m = 0.02382
a_m = -0.07578
"""

g_1_AIC = get_AIC(c_h, a_h, bins_mix, vals_mix)

g_2_AIC = get_bi_AIC(c_m, a_m, c_f, a_f, bins_m, bins_f, vals_m, vals_f)

print "AIC values:"
print g_1_AIC, g_2_AIC


#write_to_file(bins,vals,out_loc)
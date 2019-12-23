#!/usr/bin/python
from __future__ import division
import random
import math
from operator import mul

# "dumb" clasifier for monotonicity.
#	Finds the acceptible deviation from monotonicity for classification.


#Functions.

#Get data from file containing one time series per line, seperated by tabs.
def get_data(loc, cutoff, min_peak = 1):
	
	f = open(loc,'r')
	series = []
	dum_series = []
	
	for line in f:
		if len(line) > 1:
			dum_series = line[0:-1].split('\t')		#Ignore \n character.
			strip_series = [int(x) for x in dum_series[0:-1] if x != '0']		#Convert to integers and strip zeros.
			if (len(dum_series) > cutoff) and (max(strip_series) > min_peak):
				dum_series = [int(x) for x in dum_series]
				series.append(dum_series)
	
	return series


def write_to_file(data):
	out = open("Actresses_failed_samples_full_fail.txt" ,'w')
	for series in data:
		for x in series[0]:
			out.write(str(x) + ',')
		if FULL_FAIL:
			out.write('\t')
			for x in series[3]:
				out.write(str(x) + ',')
		out.write('\t' + str(series[1]) + '\t' + str(series[2]) + '\n')
	return


#Get the AM for a sequence.
def get_AM(X):
	
	#AM_val = X.index(max(X))
	
	rev = X[::-1]		#Reverse list.
	AM_rev = rev.index(max(X))			#Get the location of the last AM (first in reversed sequence).
	AM_val = len(X) - AM_rev - 1			#Index of last AM in foward sequence.
		
	return AM_val


#Get list of n samples from series X with class lables.
def get_samples(X, n):
	
	AM_val = get_AM(X)
	
	samples = []
	for i in xrange(n):
		loc = random.randint(1,len(X))			#Pick a random location to sample to.
		samp_seq = X[0:loc]
		lable = 1 if loc <= AM_val else 0		#Get class lable - 1 for pre AM, 0 for post AM.
		rem_seq = X[loc:]
		samples.append([samp_seq,lable,len(X),rem_seq])
	
	return samples


def get_class(X, theta):
	
	d = 0
	#print X
	for i in xrange(len(X)-1):
		#print i, X[i+1] - X[i]
		d -= min([0,X[i+1] - X[i]])
	
	if d > theta:
		return 0
	else:
		return 1
	

def train_process(samples):
	
	print "Training process..."
	
	t_min = 0
	t_max = 100
	
	runs = 500
	
	c_samps = samples
	
	while(math.floor(t_max) != math.floor(t_min)):
	#for i in xrange(runs):
		
		random.shuffle(c_samps)
		
		t_step = float(t_max - t_min)/4
		
		t_1 = t_min + t_step
		t_2 = t_max - t_step
		
		score_1 = 0
		score_2 = 0
		
		for x in c_samps:
			
			path = x[0]
			class_val = x[1]
			
			t_1_c = get_class(path,t_1)
			t_2_c = get_class(path,t_2)
			
			score_1 += 1 if t_1_c == class_val else 0
			score_2 += 1 if t_2_c == class_val else 0
		
		if score_1 > score_2:
			t_mid = t_1
			#print t_1, score_1
		else:
			t_mid = t_2
			#print t_2, score_2
		
		t_max = t_mid + t_step
		t_min = t_mid - t_step
	
	return t_mid
		

#Test the trained process on the remaining data.
def test_process(series, theta, print_conf_mat=False):
	
	score = 0
	
	c1_o_c1 = 0
	c1_o_c2 = 0
	c2_o_c1 = 0
	c2_o_c2 = 0
	
	failed_samples = []
	
	for x in series:
		class_val = x[1]
		
		class_est = get_class(x[0],theta) 
		
		if class_est == class_val:
			score += 1
			
			if class_val == 1:
				c1_o_c1 += 1
			else:
				c2_o_c2 += 1
		else:
			failed_samples.append(x)
			if class_val == 1:
				c2_o_c1 += 1
			else:
				c1_o_c2 +=1
	if print_conf_mat:
		print "Confusion matrix : "
		print "C1 observed, is C1: " + str(c1_o_c1)
		print "C1 observed, is C2: " + str(c1_o_c2)
		print "C2 observed, is C1: " + str(c2_o_c1)
		print "C2 observed, is C2: " + str(c2_o_c2)
		
		precision = c1_o_c1/(c1_o_c1+c1_o_c2)
		recall = c1_o_c1/(c1_o_c1+c2_o_c1)
		
		t_c1 = c1_o_c1 + c2_o_c1
		t_c2 = c2_o_c2 + c1_o_c2
		
		print "Precision: " + str(precision)
		print "Recall: " + str(recall)
		print "F1 score: " + str(2*precision*recall/(precision+recall))
		print "Total C1: " + str(t_c1)
		print "Total C2: " + str(t_c2)
	
	score = score/len(series)
	
	if WRITE_FAILS:
		write_to_file(failed_samples)
	
	return score



#Null classifier.
def null_class(X):
	
	last_ind = len(X)-1
	
	AM = get_AM(X)
	
	if AM == last_ind:
		return 1
	else:
		return 0


#Test the null model on the same data.
def null_test(series):
	
	score = 0
	
	for x in series:
		class_val = x[1]
		class_est = null_class(x[0])
		
		if class_est == class_val:
			score += 1
	
	score = score/len(series)
	
	return score



#Main.

global WRITE_FAILS
WRITE_FAILS = True
global FULL_FAIL
FULL_FAIL = True

#Path to actresses or actors working count series data.
data_loc = "Actresses_count_series_name_strip.txt"
#data_loc = "Actors_count_series_name_strip.txt"

n = 5				#Number of samples to take from each time series.
T = 1000			#Number of times series to use in training.
cutoff = 10			#Minimum number of ative years (excluding zeros).
min_peak = 5

series = get_data(data_loc, cutoff, min_peak)

print len(series)

sub_series = series[0:T]
test_series = series[T:]

samples = []
for x in sub_series:
	samples += get_samples(x,n)			#Get new samples with class lables.
	
theta = train_process(samples)		#Get values for threshold and variance given initial estimates.

print "Training complete, testing remaining data..."

test_samples = []
for x in test_series:
	test_samples += get_samples(x, n)

score = test_process(test_samples, theta, True)

"""
#Dum testing section.
print "Individual value testing..."
test_vector = []
for t in xrange(50):
	test_vector.append([t,test_process(test_samples, t, False)])
	#print t,test_process(test_samples, t)

profile_dump = "dum_est_s_fn_d.txt"
out = open(profile_dump,'w')
for x in test_vector:
	out.write(str(x[0]) + '\t' + str(x[1]) + '\n')
"""

null_score = null_test(test_samples)

print score, theta
print "null score: "+str(null_score)

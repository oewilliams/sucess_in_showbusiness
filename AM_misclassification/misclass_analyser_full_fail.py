#!/usr/bin/python
from __future__ import division
import os
#Program takes misclassified data and parses.

def parse_data(data_file):
	
	f = open(data_file,'r')
	
	AM_false_pre_list = []
	AM_false_post_list = []
	
	for line in f:
		split_line = line.split('\t')
		dum_pre_series = split_line[0]
		dum_post_series = split_line[1]
		AM_class = int(split_line[2])
		orig_len = int(split_line[3])
		
		pre_series = [int(x) for x in dum_pre_series[0:-1].split(',')]
		try:
			post_series = [int(x) for x in dum_post_series[0:-1].split(',')]
			if AM_class == 0:
				AM_false_pre_list.append([pre_series,post_series,AM_class,orig_len])
			else:
				AM_false_post_list.append([pre_series,post_series,AM_class,orig_len])
		except:
			#print dum_post_series
			pass
						
		#print AM_false_pre_list[-1]	
	return AM_false_pre_list, AM_false_post_list


def get_AM(X):
	
	#AM_val = X.index(max(X))
	
	rev = X[::-1]		#Reverse list.
	AM_rev = rev.index(max(X))			#Get the location of the last AM (first in reversed sequence).
	AM_val = len(X) - AM_rev - 1			#Index of last AM in foward sequence.
		
	return AM_val


def analyse_data(data):
	
	dist_list = []
	
	for x in data:
		pre_series = x[0]
		post_series = x[1]
		
		false_AM_index = get_AM(pre_series)
		true_AM_index = get_AM(pre_series+post_series)
		
		dist_list.append(true_AM_index-false_AM_index)
		
	return dist_list

def write_to_file(data, name, out_loc):
	
	file_name = "Actresses_AM_false_"+name+"_dist_to_true.txt"
	out_name = os.path.join(out_loc,file_name)
	out = open(out_name,'w')
	
	for x in data:
		out.write(str(x) + '\n')
	
	return


def main():
	
	#Path to actresses (or actors) failed classification sample data.
	data_file = "Actresses_failed_samples_full_fail.txt"
	
	#Location of desired output folder for misclassification data.
	out_loc = "/misclasified_data"
	
	AM_false_pre_list, AM_false_post_list = parse_data(data_file)
	
	#false_pre_data = analyse_data(AM_false_pre_list)
	false_post_dists = analyse_data(AM_false_post_list)
	
	false_post_dists.sort()
		
	write_to_file(false_post_dists,"post",out_loc)


if __name__ == "__main__":
	main()
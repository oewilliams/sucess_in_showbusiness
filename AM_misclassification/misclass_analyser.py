#!/usr/bin/python
from __future__ import division
import os
#Program takes misclassified data and parses.

def parse_data(data_file):
	
	f = open(data_file,'r')
	
	AM_false_pre_list = []
	AM_false_post_list = []
	
	for line in f:
		split_line = line.split(',')
		AM_class = int(split_line[-1][1])
		orig_len = int(split_line[-1][3:-1])
		series = [int(x) for x in split_line[0:-1]]
		
		if AM_class == 0:
			AM_false_pre_list.append([series,AM_class,orig_len])
		else:
			AM_false_post_list.append([series,AM_class,orig_len])
		
		#print [series,AM_class,orig_len]
	
	return AM_false_pre_list, AM_false_post_list


def analyse_data(data):
	
	out_list = []
	
	for x in data:
		sample_length = len(x[0])
		len_frac = sample_length/x[2]
		out_list.append([sample_length,len_frac])
	return out_list

def write_to_file(data, name, out_loc):
	
	file_name = "Actresses_AM_false_"+name+"_length_frac.txt"
	out_name = os.path.join(out_loc,file_name)
	out = open(out_name,'w')
	
	for x in data:
		out.write(str(x[0]) + '\t' + str(x[1]) + '\n')
	
	return


def main():
	
	#Path to actresses (or actors) misclassification samples.
	data_file = "/Users/oliverwilliams/Documents/qmul/data/imdb/Lucas_project/misclasified_data/Actresses_failed_samples.txt"
	
	#Location of desired output folder for misclassification data.
	out_loc = "/Users/oliverwilliams/Documents/qmul/data/imdb/Lucas_project/misclasified_data"
	
	AM_false_pre_list, AM_false_post_list = parse_data(data_file)
	
	false_pre_data = analyse_data(AM_false_pre_list)
	false_post_data = analyse_data(AM_false_post_list)
	
	write_to_file(false_pre_data,"pre",out_loc)
	write_to_file(false_post_data,'post',out_loc)


if __name__ == "__main__":
	main()
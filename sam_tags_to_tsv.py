#!/usr/bin/python 
import sys, os 
import pandas 
import pysam 


samhandle = sys.argv[1]
# outhandle = sys.argv[2]

print 'reading sam file: {}'.format(samhandle)
# print 'writing to tsv file: {}'.format(outhandle) 

# def make_df(record): return pd.DataFrame(record.tags, columns=['c', record.query_name]).set_index('c').T

sam = pysam.AlignmentFile(samhandle, 'rb')

for record in sam: 
	tagdict = dict(record.tags)
	cell_barcode = None
	if 'CB' in tagdict.keys(): 
		cell_barcode = tagdict['CB'].split("-")[0]
	elif 'CR' in tagdict.keys(): 
		cell_barcode = tagdict['CR']

	umi = None 
	if 'UB' in tagdict.keys(): 
		umi = tagdict['UB']
	elif 'UR' in tagdict.keys(): 
		umi = tagdict['UR']
	
	if cell_barcode and umi: 
		print "{}\t{}\t{}".format(record.query_name, umi, cell_barcode)



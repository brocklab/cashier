#!/usr/bin/python 
import sys, os 
from itertools import islice

fastqhandle = sys.argv[1]

if fastqhandle == "-": 
	sys.stderr.write('parsing fastq from stdin\n') 
	infile = sys.stdin 
else: 
	sys.stderr.write('parsing fastq from file: {}\n'.format(fastqhandle))
	infile = open(fastqhandle, 'r')


def process_record(record): 
	# sys.stderr.write('working on record: \n')
	# sys.stderr.write(str(record))
	# sys.stderr.write('\n')
	# print record
	read_name, umi, cell_barcode = record[0].rstrip('\n').split('_')
	lineage_barcode = record[1].rstrip('\n')
	print "{}\t{}\t{}\t{}".format(read_name, umi, cell_barcode, lineage_barcode)


lines = []
for line in infile:
    lines.append(line)
    if len(lines) == 4:
        # print 'working on ' + str(lines)
        process_record(lines)
        lines = []

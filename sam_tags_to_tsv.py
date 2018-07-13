#!/usr/bin/python 
import sys, os 
import pandas 
import pysam 
import tempfile

samhandle = sys.argv[1]
# outhandle = sys.argv[2]

sys.stderr.write('finding header on sam file: {}\n'.format(samhandle))
# print 'writing to tsv file: {}'.format(outhandle) 

# def make_df(record): return pd.DataFrame(record.tags, columns=['c', record.query_name]).set_index('c').T

fake_header='''@HD\tVN:1.6\tSO:coordinate
@SQ\tSN:1\tLN:1000
@SQ\tSN:2\tLN:1000
@SQ\tSN:3\tLN:1000
@SQ\tSN:4\tLN:1000
@SQ\tSN:5\tLN:1000
@SQ\tSN:6\tLN:1000
@SQ\tSN:7\tLN:1000
@SQ\tSN:8\tLN:1000
@SQ\tSN:9\tLN:1000
@SQ\tSN:10\tLN:1000
@SQ\tSN:11\tLN:1000
@SQ\tSN:12\tLN:1000
@SQ\tSN:13\tLN:1000
@SQ\tSN:14\tLN:1000
@SQ\tSN:15\tLN:1000
@SQ\tSN:16\tLN:1000
@SQ\tSN:17\tLN:1000
@SQ\tSN:18\tLN:1000
@SQ\tSN:19\tLN:1000
@SQ\tSN:20\tLN:1000
@SQ\tSN:21\tLN:1000
@SQ\tSN:22\tLN:1000
@SQ\tSN:23\tLN:1000
@SQ\tSN:X\tLN:1000
@SQ\tSN:Y\tLN:1000
@SQ\tSN:MT\tLN:1000
'''

delete_sam = False 

if open(samhandle, 'r').next()[0:3]!='@HD':
	#samhandle.close()
	sys.stderr.write('sam does not have header!\n')
	sys.stderr.write('fixing by copying fake mammalian header\n')
	sys.stderr.write('cwd: {}\n'.format(os.getcwd()))	
	f = tempfile.NamedTemporaryFile(delete=False, dir=os.getcwd())
	sys.stderr.write('copying new sam to {}\n'.format(f.name))
	f.write(fake_header)
	with open(samhandle, 'r') as samfile: 
		for line in samfile: 
			f.write(line)
	f.close() 
	samhandle = f.name
	delete_sam = True 
 
	

sys.stderr.write('reading sam file: {}\n'.format(samhandle))

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


if delete_sam == True:
	sys.stderr.write('cleaning up temporary sam file\n')  
	os.unlink(samhandle) 

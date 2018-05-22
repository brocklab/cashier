# crispr_barcoding_code

collection of code to process crispr-compatible barcoding libraries 

now supports UMI and barcode extraction 


### runtime options: 

-V show version 

-v verbose mode     (shows all bash executions) 

-i | --input  <input fastq file> 

-u | --upstream_sequence <DNA sequence upstream or 5' of barcode on sequencing read> 

-d | --downstream_sequence <DNA sequence downstream or 3' of barcode on sequencing read> 

-bl | --barcode_length <integer length of expected barcode (20)> 

-q | --min_quality  <minimum PHRED quality required of all barcode bases> 
  
-umi | --umi  perform UMI extraction as well for UMIs 5' of upstream sequence 

-ul | --umi_length  <integer length of expected UMI (16)> 

-t | --trim  <integer # bases to trim on 5' end of read until UMI sequence (0)> 
  
  
  
#### defaults to the following properties: 

upstream (5') adapter sequence: CTTGTGGAAAGGACGAAACACCG

downstream (3') adapter sequence: GTTTTAGAGCTAGAA

barcode length: 20bp 

umi length: 16bp 



#### example 

to extract barcodes from file: 

extract_barcodes.sh -i 1K.raw.fastq

to extract barcodes and UMIs from file: 

extract_barcodes.sh --umi -i 1K.raw.fastq 



#### two dependencies: 
requires cutadapt to perform adapter recoginition and masking 
requires fastq_quality_filter to perform quality filtering 




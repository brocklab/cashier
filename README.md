# Expressed CRISPR-compatible barcoding tools 

A collection of bash scripts to process crispr-compatible barcoding amplicon and scRNAseq libraries. 

Now supports simultaneous UMI and barcode extraction and clustering. 

Vizualization tools in development. 

## Getting Started 

To extract barcode sequences from amplicon data: 
```
extract_barcodes.sh -i 1K.raw.fastq 
```
To extract barcode and UMI sequences from amplicon data: 
``` 
extract_barcodes.sh -i 1K.raw.fastq --umi 
``` 
To cluster UMI and barcode sequences: 
``` 
cluster_umi_barcode_file.sh -i 1K.umi.barcode.tsv --distance 2 
``` 

### Dependencies 

* cutadapt - to identify and mask adapter sequences 
* fastq_quality_filter - to filter minimum base quality 
* starcode - to cluster UMIs and barcodes on minimum levenshtein distance


### Runtime Options: 

``` 
extract_barcodes.sh -i <input_file> 

-V show version 

-v verbose mode  (shows all bash executions) 

-i | --input  <input fastq file> 

-u | --upstream_sequence <DNA sequence upstream or 5' of barcode on sequencing read> 

-d | --downstream_sequence <DNA sequence downstream or 3' of barcode on sequencing read> 

-bl | --barcode_length <integer length of expected barcode (20)> 

-q | --min_quality  <minimum PHRED quality required of all barcode bases> 
  
-umi | --umi  perform UMI extraction as well for UMIs 5' of upstream sequence 

-ul | --umi_length  <integer length of expected UMI (16)> 

-t | --trim  <integer # bases to trim on 5' end of read until UMI sequence (0)> 
  
  
  
defaults to the following properties: 

upstream (5') adapter sequence: CTTGTGGAAAGGACGAAACACCG

downstream (3') adapter sequence: GTTTTAGAGCTAGAA

barcode length: 20bp 

umi length: 16bp 


```




``` 
cluster_umi_barcode_file.sh -i <input readname-umi-barcode.tsv file> 


-i | --input <input file in form readname \t umi \t barcode> 

-V | --version   show version and exit 

-v | --verbose   verbose mode - all bash executions will be printed

-d | --distance  <int minimum levenshtein distance for clustering> 

-bd | --barcode-distance  <int minimum distance for barcode clustering> 

-ud | --umi-distance   <int minimum distance for umi clustering> 

-s | --sep   <string separator for file (" " or "\t", generally) 
```






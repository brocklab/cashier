##  Cash in on Expressed Barcode Tags (EBTs) from NGS Sequencing Data 

Bash and python scripts at your fingertips. 

Processes barcode sequencing data from both amplicon and scRNAseq sources, and enables working with 5' UMI adapters.

We employ starcode, a radically fast minimum levenshtein clustering tool, to compensate for sequencing error in the extracted barcodes (and UMIs). 

This arsenal defaults to our particular brand of crispr/cpf1 library, but it's easily relatable to your line of work. 



## Getting Started 

To extract barcode sequences from amplicon data (our crispr gRNA barcode adapters as default): 
```
extract_barcodes.sh -i 1K.raw.fastq 
```
Adapted for your adapters: 
```
extract_barcodes.sh -i 1K.raw.fastq -u <upstream adapter sequence> -d <downstream adapter sequence> 
```
To extract barcode and UMI sequences from amplicon data: 
``` 
extract_barcodes.sh -i 1K.raw.fastq --umi 
``` 
To cluster UMI and barcode sequences for a particular sample: 
``` 
cluster_umi_barcode_file.sh -i sample_1.umi.barcode.tsv --distance 1 
``` 

Right now we build quite a few intermediate files, so please bear with us. You can also pipe things straight through as below. 

<sample_name.umi.barcode.tsv> has your groceries. 



### Beautiful Dependencies 

* cutadapt - to identify and mask adapter sequences 
* fastq_quality_filter - to filter minimum base quality 
* starcode - to cluster UMIs and barcodes using a levenshtein distance network and message passing clustering (min centroid-point clustering threshold at default 5 to 1) 



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
  
  
  
DEFAULTS to the following properties the ingest the mind-blowingly-useful "COLBERT", a transduced expressed gRNA barcode library developed by Aziz in the Brock Lab to trace cell lineages: 

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



### Extract lineage barcodes straight from trustably tagged 10X cellranger BAM output: 

```
We tag read names from the possorted.bam file with their 10X-corrected whitelisted cell and umi barcodes, then check reads for our expressed barcode tags, outputing the fastq of adapter-detected trimmed reads to fastq, whence we translate to a tsv: 

first use samtools to convert possorted.bam > possorted.sam 

python sam_to_name_labeled_fastq.py 10x_possorted.sam | cutadapt -g CTTGTGGAAAGGACGAAACACCG -a  GTTTTAGAGCTAGAA  -  | python fastq_tagged_to_tsv.py - > readname_umi_cellbarcode_lineagebarcode.tsv 

```





##  Cash in on Expressed Barcode Tags (EBTs) from NGS Sequencing Data 

Cashier is a tool to simplify extraction and error-correction of expressed barcode tags from sequencing reads. 

It is basically a wrapper for cutadapt an impressive program that identifies and removes flanking adapter sequences to extract the barcodes, and starcode, a radically fast minimum levenshtein clustering tool, to compensate for sequencing error in the extracted barcodes (and UMIs).  

We use it to process our barcode sequencing data from both amplicon and scRNAseq sources, and it can even work with 5' UMI adapters.

This software defaults to our particular brand of crispr/cpf1 library, but it's easily relatable to your line of work. 



###  Dependencies Needed In Path 

* cutadapt - to identify and mask adapter sequences 
* fastq_quality_filter - to filter minimum base quality 
* starcode - to cluster UMIs and barcodes using a levenshtein distance network and message passing clustering (min centroid-point clustering threshold at default 5 to 1) 



## Getting Started With Amplicon Data 

To extract barcode sequences from amplicon data (our crispr gRNA barcode adapters as default): 
```
cashier_extract -i 1K.raw.fastq 
```
Adapted for your adapters: 
```
cashier_extract -i 1K.raw.fastq -u <upstream adapter sequence> -d <downstream adapter sequence> 
```
To extract barcode and UMI sequences from amplicon data: 
``` 
cashier_extract -i 1K.raw.fastq --umi 
``` 


## Error Correction of UMI and Barcode Sequences 

To cluster UMI and barcode sequences for a particular sample: 
``` 
cluster_umi_barcode_file.sh -i sample_1.umi.barcode.tsv --distance 1 
``` 

Right now we build quite a few intermediate files, so please bear with us. You can also pipe things straight through as below. 

<sample_name.umi.barcode.tsv> has your groceries. 




### casher_extract uses cutadapt to identify and trim flanking adapters: 

``` 
cashier_extract -i <input_file> 

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

### cluster_columns.sh uses starcode to run levenshtein-distance clustering on a file, then join those cluster centroids with the original data 

``` 
cluster_columns.sh -i <input readname-umi-barcode.tsv file> 

-i | --input <tab-separated input input file> 

-c | --columns  the columns you want to cluster (can be comma-saparated list) 

-V | --version   show version and exit 

-v | --verbose   verbose mode - all bash executions will be printed

-d | --distance  <int minimum levenshtein distance for clustering> 

-bd | --barcode-distance  <int minimum distance for barcode clustering> 

-ud | --umi-distance   <int minimum distance for umi clustering> 


```



### Extract lineage barcodes straight from reliably-tagged 10X cellranger output: 

The 10X Cellranger program uses a set of known 'whitelisted' bead barcodes for confidently mark reads with their proper bead barcode. 

We keep those by annotating the read names from the cellranger output alignment file with their 10X-corrected whitelisted cell and umi barcodes (marked as tags in the sam file), then check those reads for our expressed barcode tags - outputing a final fastq of only our adapter-flanked trimmed reads that we translate to a tsv: 

```
# Translate your cellranger bam file into a sam - generally only interested in the unmapped reads 
samtools view possorted.bam > possorted.sam

# Pipe the bead- and umi-tagged reads through cutadapt to identify and trim barcodes, then translate into a tsv 

python $cashier/scripts/sam_to_name_labeled_fastq.py 10x_possorted.sam | cutadapt -g CTTGTGGAAAGGACGAAACACCG -a GTTTTAGAGCTAGAA -n 2  -  | python $cashier/scripts/fastq_tagged_to_tsv.py - > readname_umi_cellbarcode_lineagebarcode.tsv 
```





#!/usr/bin/env bash
version="0.1"
# get arguments 

while [[ "$1" =~ ^- && ! "$1" == "--" ]]; do case $1 in
  -V | --version )
    echo $version
    exit
    ;;
  -v | --verbose ) 
		echo "verbose mode - all commands will be printed"
		set -x 
		;; 
  -i | --input )
    shift; input_file=$1
    ;;
  -u | --upstream_sequence )
    shift; upstream_sequence=$1
    ;;
  -d | --downstream_sequence )
    shift; downstream_sequence=$1
    ;;
  -bl | --barcode_length )
    shift; barcode_length=$1
    ;;
  -ul | --umi_length )
    shift; umi_length=$1
    ;;
  -umi | --umi )
    extract_umi="1"
    ;;
  -t | --trim )
    shift; trim=$1
    ;;
  -q | --min_quality )
    shift; min_quality=$1
    ;;
esac; shift; done
if [[ "$1" == '--' ]]; then shift; fi


echo "input file: " $input_file
echo "required barcode length: " $barcode_length
echo "upstream sequence: " $upstream_sequence
echo "downstream_sequence: " $downstream_sequence



### barcode extraction 

echo "running barcode extraction"
barcode_fastq_file=${input_file%.fastq}.barcode.fastq
echo "barcode fastq file: " $barcode_fastq_file

cutadapt -e 0.1 --minimum-length=$barcode_length --maximum-length=$barcode_length --max-n=0 -g $upstream_sequence -a $downstream_sequence -n 2 -o $barcode_fastq_file $input_file

if [ -n "$min_quality" ]; then 
	echo "filtering barcodes for all bases minimum quality " $min_quality
	filtered_barcode_fastq_file=${barcode_fastq_file%.fastq}.filtered.fastq 
	fastq_quality_filter -q $min_quality -p 100 -i $barcode_fastq_file -o $filtered_barcode_fastq_file -Q 33
	barcode_fastq_file=$filtered_barcode_fastq_file
fi 

echo "transforming fastq to tsv" 
barcode_tsv_file=${input_file%.fastq}.barcodes.tsv 
awk 'BEGIN{RS="@";OFS="\t"}NR>1{print $1,$3}'  $barcode_fastq_file > $barcode_tsv_file



### umi extraction 

if [ -n "$extract_umi" ]; then 
	echo "running UMI extraction"
	echo "required UMI length: " $umi_length
	umi_fastq_file=${input_file%.fastq}.umi.fastq 
	echo "umi fastq file: " $umi_fastq_file
	if  [ -n "$trim" ]; then 
		trim=$trim 
	else
		trim=0
	fi 
	cutadapt -e 0.1 --minimum-length=$umi_length --maximum-length=$umi_length --max-n=0 -a $upstream_sequence -u $trim -o $umi_fastq_file $input_file

	if [ -n "$min_quality" ]; then 
		echo "filtering UMIs for all bases minimum quality " $min_quality
		filtered_umi_fastq_file=${umi_fastq_file%.fastq}.filtered.fastq 
		fastq_quality_filter -q $min_quality -p 100 -i $umi_fastq_file -o $filtered_umi_fastq_file -Q 33
		umi_fastq_file=$filtered_umi_fastq_file
	fi 

	echo "transforming umi fastq to tsv" 
	umi_tsv_file=${input_file%.fastq}.umi.tsv 
	awk 'BEGIN{RS="@";OFS="\t"}NR>1{print $1,$3}'  $umi_fastq_file > $umi_tsv_file

	# joining barcode and umi on read name 

	echo "joining barcode and umi on read name "
	sort -k1 $barcode_tsv_file > ${barcode_tsv_file%.tsv}.sorted.tsv
	sort -k1 $umi_tsv_file > ${umi_tsv_file%.tsv}.sorted.tsv 
	join ${umi_tsv_file%.tsv}.sorted.tsv ${barcode_tsv_file%.tsv}.sorted.tsv > ${input_file%.fastq}.umi.barcode.tsv 

fi 













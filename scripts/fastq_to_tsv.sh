#bash script to translate a fastq file into a tsv 

input_fastq_file=$1 
output_tsv_file=${input_fastq_file%.fastq}.tsv 

echo "transforming fastq: " $input_fastq_file
echo "into tsv file: " $output_tsv_file

awk 'BEGIN{RS="@";OFS="\t"}NR>1{print $1,$3}'  $input_fastq_file > $output_tsv_file



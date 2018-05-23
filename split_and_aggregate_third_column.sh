#/usr/bin/bash 

awk '{split($0,arr,"\t"); split(arr[3],sequences,",");  for (i in sequences) print arr[1], arr[2], sequences[i] }' < $1


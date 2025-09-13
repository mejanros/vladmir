#!/bin/bash


KMER=$1
PATH_FASTQ='/home/jan/Vladmir/data/fastq/new_samples'
PATH_TO_SAVE='/home/jan/Vladmir/data/raw/new_samples'


echo $PATH_FASTQ
echo '================================================'

for FILE in *.fastq;do
	
	FILE_BASE=$(echo $FILE|cut -d'.' -f1)
	
	echo "O nome base do arquivo é: $FILE_BASE"
	echo '======================================'
	echo
	echo "processando o arquivo $FILE e salvando em $PATH_TO_SAVE/$FILE_BASE.jf"
	echo "===================================================================="

	jellyfish count\
	       	-m $KMER -s 1G -t 2 -o "$PATH_TO_SAVE/$FILE_BASE.jf" $FILE
	
	jellyfish dump\
		-c -o "$PATH_TO_SAVE/$FILE_BASE.$KMER.txt" "$PATH_TO_SAVE/$FILE_BASE.jf"
     
done
#rm -f *.jf


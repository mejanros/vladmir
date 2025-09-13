#!/bin/bash

PATH_ID_LIST='/home/jan/Vladmir/data/fastq/new_samples/SRR_Acc_List.txt'
PATH_TO_FASTQ_DIR='/home/jan/Vladmir/data/fastq/new_samples'
PATH_TEMP_DIR='/home/jan/Vladmir/data/fastq/tempdir'

for id in $(cat $PATH_ID_LIST);do
	echo "Baixando o arquivo $ID"
	fasterq-dump\
	       	$id -p -t $PATH_TEMP_DIR -O $PATH_TO_FASTQ_DIR
	echo "==============================================="
	echo
done


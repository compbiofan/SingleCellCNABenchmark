#!/usr/bin/env bash
if [ $# -lt 2 ]; then
    echo "Given the prefix of paired end fq reads, the reference and the number of processors, use bwa mem to align and generate the bam. \nUsage: $0 <prefix> <ref> <processor> <qual>\n";
    exit
fi

# prefix of the fq files
str=$1
# reference
ref=$2
# processors
processor=$3
# filter out reads with mapping quality smaller than qual
qual=$4

bwa mem -t $processor $ref ${str}_1.fq ${str}_2.fq > ${str}.sam
samtools view -q $qual -hbS ${str}.sam > ${str}.bam
samtools sort -o ${str}.sorted.beforedup.bam ${str}.bam
samtools rmdup ${str}.sorted.beforedup.bam ${str}.sorted.bam
samtools index ${str}.sorted.bam
rm ${str}.sam
rm ${str}.bam
rm ${str}.sorted.beforedup.bam

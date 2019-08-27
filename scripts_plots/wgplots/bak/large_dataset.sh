N=9992
gt=/storage/hpc/work/nakhleh/xf2/benchmark/large_dataset/rep_1/misc/gt_sep/gt${N}.gs.bed
bam=/storage/hpc/work/nakhleh/xf2/benchmark/large_dataset/rep_1/bams/leaf${N}.sorted.bam
hc=/storage/hpc/work/nakhleh/xf2/benchmark/large_dataset/rep_1/hmmcopy/output/strength10m_nu2p1_ep999999/leaf${N}.segs.csv
perl bam_gt_est_forplot.pl /projects/nakhleh/xf2/reference/hg19.fa.fai 200000 $gt $bam $hc > large_dataset_N${N}.forplot

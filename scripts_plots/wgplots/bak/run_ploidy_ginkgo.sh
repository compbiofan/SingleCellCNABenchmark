p=4
N=103
gt=/storage/hpc/work/nakhleh/xf2/benchmark/sim_ploidy/p${p}/rep_1/misc/gt_sep/gt${N}.bed
bam=/storage/hpc/work/nakhleh/xf2/benchmark/sim_ploidy/p${p}/rep_1/bams/leaf${N}.sorted.bam
hc=/storage/hpc/work/nakhleh/xf2/benchmark/sim_ploidy/p${p}/rep_1/hmmcopy/output/strength10m_nu2p1_ep999999/hc${N}.bed
perl bam_gt_est_forplot.pl /projects/nakhleh/xf2/reference/hg19.fa.fai 200000 $gt $bam $hc > ploidy_p${p}_N${N}.forplot

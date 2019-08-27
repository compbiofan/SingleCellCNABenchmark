#p=1
#N=175
#gt=/storage/hpc/work/nakhleh/xf2/benchmark/sim_ploidy/p${p}/rep_1/misc/gt_sep/gt${N}.bed
#bam=/storage/hpc/work/nakhleh/xf2/benchmark/sim_ploidy/p${p}/rep_1/bams/leaf${N}.sorted.bam
#hc=/storage/hpc/work/nakhleh/xf2/benchmark/sim_ploidy/p${p}/rep_1/hmmcopy/output/strength10m_nu2p1_ep999999/hc${N}.bed
#perl bam_gt_est_forplot.pl /projects/nakhleh/xf2/reference/hg19.fa.fai 200000 $gt $bam $hc > ploidy_p${p}_N${N}.forplot 
#
#p=2
#N=100
#gt=/storage/hpc/work/nakhleh/xf2/benchmark/sim_ploidy/p${p}/rep_1/misc/gt_sep/gt${N}.bed
#bam=/storage/hpc/work/nakhleh/xf2/benchmark/sim_ploidy/p${p}/rep_1/bams/leaf${N}.sorted.bam
#hc=/storage/hpc/work/nakhleh/xf2/benchmark/sim_ploidy/p${p}/rep_1/hmmcopy/output/strength10m_nu2p1_ep999999/hc${N}.bed
#perl bam_gt_est_forplot.pl /projects/nakhleh/xf2/reference/hg19.fa.fai 200000 $gt $bam $hc > ploidy_p${p}_N${N}.forplot 
#
#p=3
#N=101
#gt=/storage/hpc/work/nakhleh/xf2/benchmark/sim_ploidy/p${p}/rep_1/misc/gt_sep/gt${N}.bed
#bam=/storage/hpc/work/nakhleh/xf2/benchmark/sim_ploidy/p${p}/rep_1/bams/leaf${N}.sorted.bam
#hc=/storage/hpc/work/nakhleh/xf2/benchmark/sim_ploidy/p${p}/rep_1/hmmcopy/output/strength10m_nu2p1_ep999999/hc${N}.bed
#perl bam_gt_est_forplot.pl /projects/nakhleh/xf2/reference/hg19.fa.fai 200000 $gt $bam $hc > ploidy_p${p}_N${N}.forplot 

p=4
N=99
gt=/scratch/xf2/benchmark/sim_ploidy/rerun/data/p${p}/rep_1/gt_sep/gt${N}.bed
bam=/scratch/xf2/benchmark/sim_ploidy/rerun/data/p${p}/rep_1/leaf${N}.sorted.bam
hc=NA
echo "perl bam_gt_est_forplot.pl /projects/nakhleh/xf2/reference/hg19.fa.fai 200000 $gt $bam $hc > ploidy_new_p${p}_N${N}.forplot" 

p=5
N=198
gt=/scratch/xf2/benchmark/sim_ploidy/rerun/data/p${p}/rep_1/gt_sep/gt_${N}.bed
bam=NA
hc=NA
echo "perl bam_gt_est_forplot.pl /projects/nakhleh/xf2/reference/hg19.fa.fai 200000 $gt $bam $hc > ploidy_new_p${p}_N${N}.forplot"


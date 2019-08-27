p=1
j=0
N=13
gt=/scratch/xf2/benchmark/sim_fluc/data/gt_sep/gt${N}.bed
bam=/scratch/xf2/benchmark/sim_fluc/data/p${p}/rep_1/leaf${N}.sorted.bam
hc=/scratch/xf2/benchmark/sim_fluc/data/p${p}/rep_1/strength10m_nu2p1_ep999999/hc${N}.csv
perl bam_gt_est_forplot.pl /projects/nakhleh/xf2/reference/hg19.fa.fai 200000 $gt $bam $hc > fluc_p${p}_N${N}.forplot

p=2
j=0
N=13
gt=/scratch/xf2/benchmark/sim_fluc/data/gt_sep/gt${N}.bed
bam=/scratch/xf2/benchmark/sim_fluc/data/p${p}/rep_1/leaf${N}.sorted.bam
hc=/scratch/xf2/benchmark/sim_fluc/data/p${p}/rep_1/strength10m_nu2p1_ep999999/hc${N}.csv
perl bam_gt_est_forplot.pl /projects/nakhleh/xf2/reference/hg19.fa.fai 200000 $gt $bam $hc > fluc_p${p}_N${N}.forplot

p=3
j=0
N=13
gt=/scratch/xf2/benchmark/sim_fluc/data/gt_sep/gt${N}.bed
bam=/scratch/xf2/benchmark/sim_fluc/data/p${p}/rep_1/leaf${N}.sorted.bam
hc=/scratch/xf2/benchmark/sim_fluc/data/p${p}/rep_1/strength10m_nu2p1_ep999999/hc${N}.csv
perl bam_gt_est_forplot.pl /projects/nakhleh/xf2/reference/hg19.fa.fai 200000 $gt $bam $hc > fluc_p${p}_N${N}.forplot

p=4
j=0
N=13
gt=/scratch/xf2/benchmark/sim_fluc/data/gt_sep/gt${N}.bed
bam=/scratch/xf2/benchmark/sim_fluc/data/p${p}/rep_1/leaf${N}.sorted.bam
hc=/scratch/xf2/benchmark/sim_fluc/data/p${p}/rep_1/strength10m_nu2p1_ep999999/hc${N}.csv
perl bam_gt_est_forplot.pl /projects/nakhleh/xf2/reference/hg19.fa.fai 200000 $gt $bam $hc > fluc_p${p}_N${N}.forplot



p=2
j=3
N=44
gt=/scratch/xf2/benchmark/sim_fluc/data/p${p}/rep_1/gt_sep/gt${N}.bed
bam=/scratch/xf2/benchmark/sim_fluc/data/p${p}/rep_1/job${j}/leaf${N}.sorted.bam
#hc=/scratch/xf2/benchmark/sim_coverage/p${p}/rep_1/hmmcopy/output/strength10m_nu2p1_ep999999/hc${N}.bed
hc=NA
perl bam_gt_est_forplot.pl /projects/nakhleh/xf2/reference/hg19.fa.fai 200000 $gt $bam $hc > fluc_p${p}_N${N}.forplot

p=3
j=0
N=35
gt=/scratch/xf2/benchmark/sim_fluc/data/p${p}/rep_1/gt_sep/gt${N}.bed
bam=/scratch/xf2/benchmark/sim_fluc/data/p${p}/rep_1/job${j}/leaf${N}.sorted.bam
#hc=/scratch/xf2/benchmark/sim_coverage/p${p}/rep_1/hmmcopy/output/strength10m_nu2p1_ep999999/hc${N}.bed
hc=NA
perl bam_gt_est_forplot.pl /projects/nakhleh/xf2/reference/hg19.fa.fai 200000 $gt $bam $hc > fluc_p${p}_N${N}.forplot

p=4
j=90
N=190
gt=/scratch/xf2/benchmark/sim_fluc/data/p${p}/rep_1/gt_sep/gt${N}.bed
bam=/scratch/xf2/benchmark/sim_fluc/data/p${p}/rep_1/job${j}/leaf${N}.sorted.bam
#hc=/scratch/xf2/benchmark/sim_coverage/p${p}/rep_1/hmmcopy/output/strength10m_nu2p1_ep999999/hc${N}.bed
hc=NA
perl bam_gt_est_forplot.pl /projects/nakhleh/xf2/reference/hg19.fa.fai 200000 $gt $bam $hc > fluc_p${p}_N${N}.forplot

# for two ploidies of hmmcopy, one is wrong (giving all uniform profile), one is correct (giving correct breakpoint and absolute copy number).
perl bam_gt_twohmmcopy_forplot.pl /projects/nakhleh/xf2/reference/hg19.fa.fai 200000 /scratch/xf2/benchmark/sim_fluc/data/p3/rep_1/leaf523.sorted.bam /scratch/xf2/benchmark/sim_fluc/data/p3/rep_1/strength10m_nu2p1_ep999999/leaf523/2/segs.csv /scratch/xf2/benchmark/sim_fluc/data/p3/rep_1/strength10m_nu2p1_ep999999/leaf523/0/segs.csv > fluc_p3_N523.twoploidies_hmm.forplot

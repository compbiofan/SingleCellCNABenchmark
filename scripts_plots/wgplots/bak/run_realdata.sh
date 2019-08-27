p=1
N=97
gt=/storage/hpc/work/nakhleh/xf2/benchmark/sim_coverage/p${p}/rep_1/misc/gt_sep/gt${N}.bed
bam=/storage/hpc/work/nakhleh/xf2/benchmark/sim_coverage/p${p}/rep_1/bams/leaf${N}.sorted.bam
hc=/storage/hpc/work/nakhleh/xf2/benchmark/sim_coverage/p${p}/rep_1/hmmcopy/output/strength10m_nu2p1_ep999999/hc${N}.bed
perl bam_gt_est_forplot.pl /projects/nakhleh/xf2/reference/hg19.fa.fai 200000 $gt $bam $hc > coverage_p${p}_N${N}.forplot

p=2
N=99
gt=/storage/hpc/work/nakhleh/xf2/benchmark/sim_coverage/p${p}/rep_1/misc/gt_sep/gt${N}.bed
bam=/storage/hpc/work/nakhleh/xf2/benchmark/sim_coverage/p${p}/rep_1/bams/leaf${N}.sorted.bam
hc=/storage/hpc/work/nakhleh/xf2/benchmark/sim_coverage/p${p}/rep_1/hmmcopy/output/strength10m_nu2p1_ep999999/hc${N}.bed
perl bam_gt_est_forplot.pl /projects/nakhleh/xf2/reference/hg19.fa.fai 200000 $gt $bam $hc > coverage_p${p}_N${N}.forplot 

p=3
N=99
gt=/storage/hpc/work/nakhleh/xf2/benchmark/sim_coverage/p${p}/rep_1/misc/gt_sep/gt${N}.bed
bam=/storage/hpc/work/nakhleh/xf2/benchmark/sim_coverage/p${p}/rep_1/bams/leaf${N}.sorted.bam
hc=/storage/hpc/work/nakhleh/xf2/benchmark/sim_coverage/p${p}/rep_1/hmmcopy/output/strength10m_nu2p1_ep999999/hc${N}.bed
perl bam_gt_est_forplot.pl /projects/nakhleh/xf2/reference/hg19.fa.fai 200000 $gt $bam $hc > coverage_p${p}_N${N}.forplot 

p=4
N=96
gt=/storage/hpc/work/nakhleh/xf2/benchmark/sim_coverage/p${p}/rep_1/misc/gt_sep/gt${N}.bed
bam=/storage/hpc/work/nakhleh/xf2/benchmark/sim_coverage/p${p}/rep_1/bams/leaf${N}.sorted.bam
hc=/storage/hpc/work/nakhleh/xf2/benchmark/sim_coverage/p${p}/rep_1/hmmcopy/output/strength10m_nu2p1_ep999999/hc${N}.bed
perl bam_gt_est_forplot.pl /projects/nakhleh/xf2/reference/hg19.fa.fai 200000 $gt $bam $hc > coverage_p${p}_N${N}.forplot 

p=5
N=98
gt=/storage/hpc/work/nakhleh/xf2/benchmark/sim_coverage/p${p}/rep_1/misc/gt_sep/gt${N}.bed
bam=/storage/hpc/work/nakhleh/xf2/benchmark/sim_coverage/p${p}/rep_1/bams/leaf${N}.sorted.bam
hc=/storage/hpc/work/nakhleh/xf2/benchmark/sim_coverage/p${p}/rep_1/hmmcopy/output/strength10m_nu2p1_ep999999/hc${N}.bed
perl bam_gt_est_forplot.pl /projects/nakhleh/xf2/reference/hg19.fa.fai 200000 $gt $bam $hc > coverage_p${p}_N${N}.forplot 


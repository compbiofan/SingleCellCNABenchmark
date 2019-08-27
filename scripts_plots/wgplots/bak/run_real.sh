N=5969789
bam=/scratch/xf2/benchmark/real/kim_ruli_2018cell/SRR${N}.sorted.bam
hc=/storage/hpc/work/nakhleh/xf2/benchmark/real/hmmcopy/SRR${N}.segs.csv
perl bam_gt_est_forplot.pl /projects/nakhleh/xf2/reference/hg19.fa.fai 200000 NA $bam $hc > real_p54M_N${N}.forplot

N=5969781
bam=/scratch/xf2/benchmark/real/kim_ruli_2018cell/SRR${N}.sorted.bam
hc=/storage/hpc/work/nakhleh/xf2/benchmark/real/hmmcopy/SRR${N}.segs.csv
perl bam_gt_est_forplot.pl /projects/nakhleh/xf2/reference/hg19.fa.fai 200000 NA $bam $hc > real_p191M_N${N}.forplot

N=5964389
bam=/scratch/xf2/benchmark/real/kim_ruli_2018cell/SRR${N}.sorted.bam
hc=/storage/hpc/work/nakhleh/xf2/benchmark/real/hmmcopy/SRR${N}.segs.csv
perl bam_gt_est_forplot.pl /projects/nakhleh/xf2/reference/hg19.fa.fai 200000 NA $bam $hc > real_p519M_N${N}.forplot

N=5964159
bam=/scratch/xf2/benchmark/real/kim_ruli_2018cell/SRR${N}.sorted.bam
hc=/storage/hpc/work/nakhleh/xf2/benchmark/real/hmmcopy/SRR${N}.segs.csv
perl bam_gt_est_forplot.pl /projects/nakhleh/xf2/reference/hg19.fa.fai 200000 NA $bam $hc > real_p1100M_N${N}.forplot

N=5964255
bam=/scratch/xf2/benchmark/real/kim_ruli_2018cell/SRR${N}.sorted.bam
hc=/storage/hpc/work/nakhleh/xf2/benchmark/real/hmmcopy/SRR${N}.segs.csv
perl bam_gt_est_forplot.pl /projects/nakhleh/xf2/reference/hg19.fa.fai 200000 NA $bam $hc > real_p1500M_N${N}.forplot



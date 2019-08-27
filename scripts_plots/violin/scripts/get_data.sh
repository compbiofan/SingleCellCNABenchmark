# ploidy rep_1

# get hmmcopy
exp=ploidy
rep=1
met=HMMcopy
for i in `seq 1 5`; do dir="../data/${exp}/rep_${rep}/${met}/p$i"; mkdir -p $dir; scp -r xf2@nots.rice.edu:/storage/hpc/work/nakhleh/xf2/benchmark/sim_${exp}/p$i/rep_${rep}/hmmcopy/output/strength10m_nu2p1_ep999999/hc* $dir/; done

# get groundtruth
exp=ploidy
rep=1
met=gt
#for i in `seq 1 5`; do dir="../data/${exp}/rep_${rep}/${met}/p$i"; mkdir -p $dir; scp -r xf2@nots.rice.edu:/storage/hpc/work/nakhleh/xf2/benchmark/sim_${exp}/p$i/rep_${rep}/misc/gt_sep/gt* $dir/; done
for i in `seq 1 5`; do dir="../data/${exp}/rep_${rep}/${met}/p$i"; mkdir -p $dir; scp -r xf2@nots.rice.edu:/storage/hpc/work/nakhleh/xf2/benchmark/sim_${exp}/p$i/rep_${rep}/misc/gt.all.csv $dir/; done

# get ginkgo
exp=ploidy
rep=1
met=Ginkgo
for i in `seq 1 5`; do dir="../data/${exp}/rep_${rep}/${met}/p$i"; mkdir -p $dir; scp -r xf2@nots.rice.edu:/storage/hpc/work/nakhleh/xf2/benchmark/sim_${exp}/p$i/rep_${rep}/bams/SegCopy $dir/; done

# get copynumber
exp=ploidy
rep=1
met=CopyNumber
for i in `seq 1 5`; do dir="../data/${exp}/rep_${rep}/${met}/p$i"; mkdir -p $dir; scp -r xf2@nots.rice.edu:/storage/hpc/work/nakhleh/xf2/benchmark/sim_${exp}/p$i/rep_${rep}/copynumber/copynumber.output.csv $dir/; done

# fluctuation rep_1
exp=fluc
rep=1
met=Ginkgo
for i in `seq 1 4`; do dir="../data/${exp}/rep_${rep}/${met}/p$i"; mkdir -p $dir; scp -r xf2@nots.rice.edu:/storage/hpc/work/nakhleh/xf2/benchmark/sim_${exp}/p$i/rep_${rep}/bams/SegCopy $dir/; done

exp=fluc
rep=1
met=HMMcopy
for i in `seq 1 4`; do dir="../data/${exp}/rep_${rep}/${met}/p$i"; mkdir -p $dir; scp -r xf2@nots.rice.edu:/storage/hpc/work/nakhleh/xf2/benchmark/sim_${exp}/p$i/rep_${rep}/hmmcopy/output/strength10m_nu2p1_ep999999/hc* $dir/; done

exp=fluc
rep=1
met=gt
for i in `seq 1 4`; do dir="../data/${exp}/rep_${rep}/${met}/p$i"; mkdir -p $dir; scp -r xf2@nots.rice.edu:/storage/hpc/work/nakhleh/xf2/benchmark/sim_${exp}/gt_sep_rep${rep}/gt* $dir/; done
for i in `seq 1 4`; do dir="../data/${exp}/rep_${rep}/${met}/p$i"; pushd $dir; cat gt*.bed > gt.all.csv; perl -ane 'print join("\t", @F[0 .. 2]) . "\n"' | sort | uniq -c | perl -ane 'print join("\t", @F[1 .. 3]) . "\n" if($F[0] > 5)' > gt.all.forCN.csv; popd; done
#scp -r xf2@nots.rice.edu:/storage/hpc/work/nakhleh/xf2/benchmark/sim_${exp}/gt.all.csv $dir/;

# get copynumber
exp=fluc
rep=1
met=CopyNumber
for i in `seq 1 4`; do dir="../data/${exp}/rep_${rep}/${met}/p$i"; mkdir -p $dir; scp -r xf2@nots.rice.edu:/storage/hpc/work/nakhleh/xf2/benchmark/sim_${exp}/p$i/rep_${rep}/copynumber/copynumber.output.csv $dir/; done



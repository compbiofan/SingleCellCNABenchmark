p=$1
# get the line number of this genomic position
python tree_edge.py -s $p -f ../../hfreqCNA/test.segcopy.wheader -n
# get the read count from segcopy in the surrounding region
python tree_edge.py -s $p -f ../../hfreqCNA/test.segcopy.wheader -l -a ../../hfreqCNA/test.segcopy
# get the probability from posterior decoding in the surrounding region
python tree_edge.py -s $p -f ../../hfreqCNA/test.segcopy.wheader -F 6 -a ../../hfreqCNA/test.segcopy.outfreq | perl -ane 'print $_ if($F[6] > 0.99)' | wc -l 

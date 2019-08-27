use warnings;
use strict;
require comparison;

if(@ARGV == 0){
    die "This takes a copynumber output, a merged ground truth, and calculate the recall and precision regardless of rising/falling/absolute copy number. \nUsage: $0 <cn_file> <gt_file> <t> \n";
}

my ($cn_f, $gt_f, $t) = @ARGV;

my ($recall, $precision) = comparison::get_cn_recall_precision($cn_f, $gt_f, $t);
print join("\t", $recall, $precision) . "\n";

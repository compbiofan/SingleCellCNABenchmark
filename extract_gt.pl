use warnings;
use strict;

if(@ARGV == 0){
    die "This takes a gt.all.csv, and a file with the list of cells, output lines in gt.all.csv that has the last column in the list of cells.\nUsage: $0 <gt_all_csv> <list_cells>\n";
}
my ($gt_f, $l_f) = @ARGV;

my $h;
open fh_, "<$l_f" or die $!;
while(<fh_>){
    chomp;
    $h->{$_} = 1;
}
close fh_;

open fh_, "<$gt_f" or die $!;
while(<fh_>){
    chomp;
    my @a = split(/\t/, $_);
    if(defined $h->{$a[$#a]}){
        print $_ . "\n";
    }
}
close fh_;

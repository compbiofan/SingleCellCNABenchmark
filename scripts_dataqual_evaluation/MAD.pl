use warnings;
use strict;
require math;

if(@ARGV == 0){
    die "This takes a wig file, and output the Median Absolute Deviation (MAD) of this cell.\nUsage: $0 <wig>\n";
}

my ($wig_f) = @ARGV;
my @a;
open fh_,"<$wig_f" or die $!;
while(<fh_>){
    next if($_ =~ /^fixedStep/);
    chomp;
    push @a, $_;
}
close fh_;
my $mad = math::MAD(\@a);
my $median = math::median(\@a);
my $mad_ = sprintf("%.2f", $mad/$median);
print $mad_ . "\n";

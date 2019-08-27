use warnings;
use strict;

if(@ARGV == 0){
    die "This takes a forplot file, and a SegCopy file, add an additional column to the forplot file so that they are on the same coordinates. \nUsage: $0 <forplot file> <SegCopy>\n";
}

my ($forplot_f, $SegCopy_f) = @ARGV;

my $h;
open fh_, "<$forplot_f" or die $!;
while(<fh_>){
    chomp;
    my @a = split(/\t/, $_);
    $a[1] = $a[1] / 200000;
    $h->{$a[0]}->{$a[1]}->{gt} = $a[2];
    $h->{$a[0]}->{$a[1]}->{rc} = $a[3];
    $h->{$a[0]}->{$a[1]}->{hmm} = $a[4];
}
close fh_;

open fh_, "<$SegCopy_f" or die $!;
while(<fh_>){
    next if($_ =~ /START/);
    chomp;
    my @a = split(/\t/, $_);
    my $bin_s = &round($a[1]/200000);
    my $bin_e = &round($a[2]/200000);
    foreach my $s ($bin_s .. $bin_e){
        next if(!defined $h->{$a[0]}->{$s});
        $h->{$a[0]}->{$s}->{ginkgo} = $a[$#a];
    }
}
close fh_;

my @chrs = (1 .. 22, "X", "Y");
foreach my $chr (@chrs){
    $chr = "chr" . $chr;
    foreach my $s (sort {$a <=> $b} keys %{$h->{$chr}}){
        my $s1 = $s * 200000;
        if(!defined $h->{$chr}->{$s}->{ginkgo}){
            $h->{$chr}->{$s}->{ginkgo} = 2;
        }
        print join("\t", $chr, $s1, $h->{$chr}->{$s}->{gt}, $h->{$chr}->{$s}->{rc}, $h->{$chr}->{$s}->{hmm}, $h->{$chr}->{$s}->{ginkgo}) . "\n";
    }
}
1;
sub round{
    my ($a) = @_;
    return int($a + 0.5);
}

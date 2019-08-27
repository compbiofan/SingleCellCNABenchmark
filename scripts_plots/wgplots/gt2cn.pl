use warnings;
use strict;

if(@ARGV == 0){
    die "This takes a file with the ground truth bed, generate the absolute cpy number for each bin, taking up a row for each bin.\nUsage: $0 <fai> <window_size> <gt_file>\n";
}

my ($fai, $w, $gt_f) = @ARGV;

my $gt_h = &init($fai, $w);
$gt_h = &read_gt($gt_h, $gt_f, $w);
&print_gt($gt_h, $w);

1;

sub init{
    my ($fai, $w) = @_;
    my $gt_h;
    #my $num = 0;
    open fh_, "<$fai" or die $!;
    while(<fh_>){
        my @a = split(/\s+/, $_); 
        my $bin_num = int($a[1]/$w);
        foreach my $i (0 .. $bin_num){
            #$num ++;
            $gt_h->{$a[0]}->{$i} = 2;
        }
    }
    close fh_;
    #print $num . "\n";
    return $gt_h;
}
        

sub print_gt{
    my ($gt_h, $w) = @_;
    my @chrs = (1 .. 22);
    push @chrs, "X";
    push @chrs, "Y";
    foreach my $chr (@chrs){
        my $c;
        $c = "chr" . $chr;
        foreach my $s (sort {$a <=> $b} keys %{$gt_h->{$c}}){
            my $pos = $w * $s;
            print join("\t", ($c, $pos, $gt_h->{$c}->{$s})) . "\n";
        }
    }
}

sub read_gt{
    my ($gt_h, $gt_f, $w) = @_;
    open fh_, "<$gt_f" or die $!;
    while(<fh_>){
        chomp;
        my @a = split(/\t/, $_);
        my $bin_s = int($a[1]/$w); 
        my $bin_e = int($a[2]/$w);
        foreach my $i ($bin_s .. $bin_e){
            $gt_h->{$a[0]}->{$i} = $a[3];
        }
    }
    close fh_;
    return $gt_h;
}

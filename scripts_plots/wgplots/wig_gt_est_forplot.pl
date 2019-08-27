use warnings;
use strict;

if(@ARGV == 0){
    die "This takes a file with the ground truth bed, generate the absolute cpy number for each bin, taking up a row for each bin. It then takes a wig file, with the same bin size, count the number of reads falling to that bin, and on the additional column, output this number. It then reads hmmcopy's segs.csv file, take the third column which is the absolute copy number, and put it on the extra column of the output of this script.\nUsage: $0 <fai> <window_size> <gt_file> <wig> <hmmcopy_segs_csv>\n";
}

my ($fai, $w, $gt_f, $wig, $hmmcopy_segs) = @ARGV;
# TODO: add the absolute copy number from a method (segs.csv) etc. 

my $gt_h;
$gt_h = &init($gt_h, $fai, $w, 2, "gt");
if($gt_f ne "NA"){
    $gt_h = &read_gt($gt_h, $gt_f, $w, "gt");
}
$gt_h = &init($gt_h, $fai, $w, 0, "rc");
if($wig ne "NA"){
    $gt_h = &read_wig($gt_h, $wig, $w, "rc"); 
}
$gt_h = &init($gt_h, $fai, $w, 2, "hc");
if($hmmcopy_segs ne "NA"){
    $gt_h = &read_hc($gt_h, $hmmcopy_segs, $w, "hc");
}
my @keys = ("gt", "rc", "hc");
&print_gt($gt_h, $w, \@keys);

1;

sub read_hc{
    my ($gt_h, $hc_f, $w, $key) = @_;
    if(!-e $hc_f){
        print "$hc_f does not exist. \n";
    }
    open fh_, "<$hc_f" or die $!;
    while(<fh_>){
        next if($_ =~ /start/);
        my @a = split(/\,/, $_);
        my ($chr, $start, $end, $ab_cn) = @a[0 .. 3];
        $start = int($start/$w);
        $end = int($end/$w);
        foreach my $s ($start .. $end){
            $gt_h->{$chr}->{$s}->{$key} = $ab_cn;
        }
    }
    close fh_;
    return $gt_h;
}

sub read_wig{
    my ($gt_h, $wig, $w, $key) = @_;
    my $chr;
    my $p;
    open fh_, "<$wig" or die $!;
    while(<fh_>){
        chomp;
        if($_ =~ /chrom/){
            ($chr) = ($_ =~ /chrom=(\S+)/);
            $p = 0;
            next;
        }
        $gt_h->{$chr}->{$p}->{$key} = $_;
        $p ++;
    }
    close fh_;
    return $gt_h;
}
    
sub init{
    my ($gt_h, $fai, $w, $value, $key) = @_;
    #my $num = 0;
    open fh_, "<$fai" or die $!;
    while(<fh_>){
        my @a = split(/\s+/, $_); 
        my $bin_num = int($a[1]/$w);
        foreach my $i (0 .. $bin_num){
            #$num ++;
            $gt_h->{$a[0]}->{$i}->{$key} = $value;
        }
    }
    close fh_;
    #print $num . "\n";
    return $gt_h;
}
        

sub print_gt{
    my ($gt_h, $w, $keys) = @_;
    my @chrs = (1 .. 22);
    push @chrs, "X";
    push @chrs, "Y";
    foreach my $chr (@chrs){
        my $c;
        $c = "chr" . $chr;
        foreach my $s (sort {$a <=> $b} keys %{$gt_h->{$c}}){
            next if(!defined $gt_h->{$c}->{$s}->{gt});
            my $pos = $w * $s;
            print join("\t", $c, $pos);
            foreach my $key (@$keys){
                if(!defined $gt_h->{$c}->{$s}->{$key}){
                    print "\t" . 0;
                }
                else{
                    print "\t" . $gt_h->{$c}->{$s}->{$key};
                }
            }
            print "\n";
        }
    }
}

sub read_gt{
    my ($gt_h, $gt_f, $w, $key) = @_;
    open fh_, "<$gt_f" or die $!;
    while(<fh_>){
        chomp;
        my @a = split(/\t/, $_);
        my $bin_s = int($a[1]/$w); 
        my $bin_e = int($a[2]/$w);
        foreach my $i ($bin_s .. $bin_e){
            $gt_h->{$a[0]}->{$i}->{$key} = $a[3];
        }
    }
    close fh_;
    return $gt_h;
}

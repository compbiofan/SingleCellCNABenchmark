use warnings;
use strict;

if(@ARGV == 0){
    die "This takes a bam file, with the same bin size, count the number of reads falling to that bin, and on the additional column, output this number. It then reads hmmcopy's segs.csv file for the correct and wrong selection of ploidy and adds them as the extra two columns.\nUsage: $0 <fai> <window_size> <bam> <hmmcopy_segs_csv_correct_ploidy> <hmmcopy_segs_csv_wrong_ploidy>\n";
}

my ($fai, $w, $bam, $hmmcopy_segs_correct, $hmmcopy_segs_wrong) = @ARGV;
# TODO: add the absolute copy number from a method (segs.csv) etc. 

my $gt_h;
$gt_h = &init($gt_h, $fai, $w, 0, "rc");
if($bam ne "NA"){
    $gt_h = &read_bam($gt_h, $bam, $w, "rc"); 
}
my $key = "hc_correct";
$gt_h = &init($gt_h, $fai, $w, 2, $key);
if($hmmcopy_segs_correct ne "NA"){
    $gt_h = &read_hc($gt_h, $hmmcopy_segs_correct, $w, $key);
}
$key = "hc_wrong";
$gt_h = &init($gt_h, $fai, $w, 2, $key);
if($hmmcopy_segs_correct ne "NA"){
    $gt_h = &read_hc($gt_h, $hmmcopy_segs_wrong, $w, $key);
}
my @keys = ("rc", "hc_correct", "hc_wrong");
&print_gt($gt_h, $w, \@keys);

1;

sub read_hc{
    my ($gt_h, $hc_f, $w, $key) = @_;
    if(!-e $hc_f){
        print "$hc_f does not exist. \n";
    }
    open fh_, "<$hc_f" or die $!;
    while(<fh_>){
        next if($_ =~ /start/i);
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

sub read_bam{
    my ($gt_h, $bam, $w, $key) = @_;
    open IN, "samtools view $bam | " or die $!;
    while(<IN>){
        my @a = split(/\t/, $_);
        my ($chr, $pos) = @a[2 .. 3];
        $b = int($pos/$w);
        next if(! defined $gt_h->{$chr}->{$b}->{$key});
        #if(! defined $gt_h->{$chr}->{$b}->{$key}){
        #    $gt_h->{$chr}->{$b}->{$key} = 1;
        #}
        #else{
        $gt_h->{$chr}->{$b}->{$key} ++;
        #}
    }
    close IN;
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
            #next if(!defined $gt_h->{$c}->{$s}->{gt});
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

use warnings;
use strict;
require math;

if(@ARGV == 0){
    die "This takes a fai file, a ground truth file, read count file, generate the SNR.\nUsage: $0 <fai> <w> <gt_f> <bam>\n";
}

my ($fai, $w, $gt_f, $bam) = @ARGV;

my $gt_h;
$gt_h = &init($gt_h, $fai, $w, 2, "gt");
$gt_h = &read_gt($gt_h, $gt_f, $w, "gt");
$gt_h = &init($gt_h, $fai, $w, 0, "rc");
$gt_h = &read_bam($gt_h, $bam, $w, "rc"); 

my $SNR = &calculate_SNR($gt_h);
print $SNR . "\n";
#&print_gt($gt_h, $w, \@keys);

1;

sub calculate_SNR{
    my ($gt_h) = @_;
    # every two neighboring regions has an SNR
    my @SNRs;
    my $prev_prev_cn = -1;
    my $prev_cn = -1;
    my @prev_prev_rcs = ();
    my @prev_rcs = ();
    my $tag = 0;
    foreach my $chr (sort keys %$gt_h){
        foreach my $pos (sort {$a <=> $b} keys %{$gt_h->{$chr}}){
            my $cn = $gt_h->{$chr}->{$pos}->{gt};
            my $rc = $gt_h->{$chr}->{$pos}->{rc};
            if($cn != $prev_cn && $prev_prev_cn != -1){
                if(scalar(@prev_rcs) == 1){
                    print join("\t", $chr, $pos, $prev_cn) . "\n";
                }
                my $this_SNR = &summarize($prev_prev_cn, $prev_cn, \@prev_prev_rcs, \@prev_rcs);
                push @SNRs, $this_SNR if($this_SNR ne "NA");
                @prev_prev_rcs = ();
                foreach my $i (@prev_rcs){
                    push @prev_prev_rcs, $i;
                }
                @prev_rcs = ();
                push @prev_rcs, $rc;
                $prev_prev_cn = $prev_cn;
                $prev_cn = $cn;
            }
            elsif($cn != $prev_cn && $prev_cn == -1){
                $prev_cn = $cn;
                push @prev_rcs, $rc;
            }
            elsif($cn != $prev_cn && $prev_cn != -1 && $prev_prev_cn == -1){
                foreach my $i (@prev_rcs){
                    push @prev_prev_rcs, $i;
                }
                @prev_rcs = ();
                push @prev_rcs, $rc;
                $prev_prev_cn = $prev_cn;
                $prev_cn = $cn;
            }
            else{
                push @prev_rcs, $rc;
            }
        }
    }
    my $this_SNR = &summarize($prev_prev_cn, $prev_cn, \@prev_prev_rcs, \@prev_rcs);
    push @SNRs, $this_SNR;
    #print join("\t", @SNRs) . "\n";
    return math::avg(\@SNRs);
}

sub summarize{
    my ($ppcn, $pcn, $pprc, $prc) = @_;
    # calculate the difference of the average rcs per copy number, which is the signal, and the maximum noise of each rcs in their region, which is the noise.
    my $a_pprc = math::avg($pprc);
    my $a_prc = math::avg($prc);
    my $signal = abs($a_pprc - $a_prc)/abs($ppcn - $pcn);

    my $noise1 = math::MAD($pprc);
    my $noise2 = math::MAD($prc);
    my $t = $noise1;
    if($t < $noise2){
        $t = $noise2;
    }
    # get the maximum difference between two read counts that are neighbors and in the same cn region
#    my $ppt = 0;
#    for(my $i = 0; $i < scalar(@$pprc) - 1; $i ++){
#        my $diff = abs($pprc->[$i] - $pprc->[$i + 1]);
#        if($diff > $ppt){
#            $ppt = $diff;
#        }
#    }
#    my $pt = 0;
#    for(my $i = 0; $i < scalar(@$prc) - 1; $i ++){
#        my $diff = abs($prc->[$i] - $prc->[$i + 1]);
#        if($diff > $pt){
#            $pt = $diff;
#        }
#    }
#    my $t = $ppt;
#    if($t < $pt){
#        $t = $pt;
#    }
    if($t == 0){
        return "NA";
    }
    my $SNR = $signal/$t;
    return $SNR;
}

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

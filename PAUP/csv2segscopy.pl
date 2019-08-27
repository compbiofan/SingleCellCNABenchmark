use warnings;
use strict;

if(@ARGV == 0){
    die "This takes a string in which there are segs.csv file from HMMcopy, it generates a segs.copy file in which the first line is the header, the first, second and third columns are chr, start, and end of each window, and starting from the fourth column are the read counts for the bin for each cell, whose name were identified in the header.\nUsage: $0 <str> <bin_size>\n";
}

my ($folder, $seg) = @ARGV;
my @fs = split(/\n/, `ls $folder`);
&print_header(\@fs);
my $h = &get_all(\@fs, $seg);
&print_h($h, \@fs);

1;

sub print_header{
    my ($files) = @_;
    print join("\t", "CHR", "START", "END");
    foreach my $f (@$files){
        my @a = split(/\//, $f);
        print "\t" . $a[$#a];
    }
    print "\n";
}

sub print_h{
    my ($h, $files) = @_;
    my @chrs = (1 .. 22);
    push @chrs, "X";
    push @chrs, "Y";
    for(my $i = 0; $i < scalar(@chrs); $i ++){
        $chrs[$i] = "chr" . $chrs[$i];
    }
    foreach my $chr (@chrs){
        next if(!defined $h->{$chr});
        foreach my $pos (sort {$a <=> $b} keys %{$h->{$chr}}){
            my ($s, $e) = split(/\./, $pos);
            print join("\t", $chr, $s, $e);
            foreach my $file (@$files){
                if(!defined $h->{$chr}->{$pos}->{$file}){
                    print "\t" . 2;
                }
                else{
                    print "\t" . $h->{$chr}->{$pos}->{$file};
                }
            }
            print "\n";
        }
    }
}
        

sub get_all{
    my ($fs, $seg) = @_;
    my $chr;
    my $step;
    my $s;
    my $e;
    my $n;
    my $h;
    foreach my $f (@$fs){
        open fh_, "<$f" or die $!;
        while(<fh_>){
            chomp;
            next if($_ =~ /^chr\,start/);
            my ($chr, $start, $end, $cn,) = split(/\,/, $_);
            my $line_num = ($end - $start + 1)/$seg;
            foreach my $l (1 .. $line_num){
                $s = $start + ($l - 1)*$seg;
                $e = $s + $seg - 1;
                $n = join(".", $s, $e);
                $h->{$chr}->{$n}->{$f} = $cn;
            }
        }
        close fh_;
    }
    return $h;
}


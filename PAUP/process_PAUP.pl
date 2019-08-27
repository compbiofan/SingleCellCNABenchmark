use warnings;
use strict;

if(@ARGV == 0){
    die "This reads the PAUP output which contains two pieces of information of the tree: tree structure in the first table and the character asignment on the nodes on the second tree. This outputs a file that has the first column the node IDs (either on the leaf or the internal nodes), the second column the parents of these nodes, and the character assignment for each bin starting from the third bin. \nUsage: $0 <input_file> <output_prefix>\n";
}

my ($f, $prefix) = @ARGV;

# read the first piece of information: tree structure
my $tree;
$tree = &read_tree_structure($f, $tree);

# read the second piece of information: the character assignment
$tree = &read_tree_assignment($f, $tree);

# print out the id (keys), the leaf_node str, the parent and the characters, each taking a column
&print_tree($tree, $prefix);

1;

sub print_tree{
    my ($h, $prefix) = @_;
    foreach my $tree (keys %$h){
        open fh_, ">$prefix.tree$tree.csv" or die $!;
        foreach my $id (keys %{$h->{$tree}}){
#            foreach my $x ("leaf_node", "par", "char"){
#                if(!defined $h->{$tree}->{$id}->{$x}){
#                    print "not defined " . join(" ", $tree, $id, $x) . "\n";
#                }
#            }
            print fh_ join("\t", $id, $h->{$tree}->{$id}->{leaf_node}, $h->{$tree}->{$id}->{par}, split("", $h->{$tree}->{$id}->{char})) . "\n";
        }
        close fh_;
    }
}

sub read_tree_structure{
    my ($f, $h, $tree_num) = @_;
# return this hash, for each node, save the root in par (parent) and leaf_node (leaf node string, if none, then "NA") key. 
# test whether it hits the first line
    my $tag = -1;
    my $tree_id = 0;
    open fh_, "<$f" or die $!;
    while(<fh_>){
        if($tag == -1 && $_ !~ /^Tree \d+:$/){
# not open yet
            next;
        }
        elsif($tag == -1 && $_ =~ /^Tree \d+:$/){
            ($tree_id) = ($_ =~ /^Tree (\d+):/);
# this will open the door for tree structure
            $tag = 0;
        }
        elsif($tag == 0 && $_ !~ /-------/){
# skip the first few lines between Tree 1: and the tree
# when all tree are over, it will stay at this state
            next;
        }
        elsif($tag == 0 && $_ =~ /------/){
# now begin
            $tag = 1;
        }
        elsif($tag == 1 && $_ !~ /------/){
# hit it the first time
            ($_) = ($_ =~ /^\s*(.+)$/);
            my @a = split(/\s+/, $_);
            if($a[1] =~ /\(\d+\)/){
                my ($id) = ($a[1] =~ /\((\d+)\)/);
                $h->{$tree_id}->{$a[0]}->{par} = $a[2];
                $h->{$tree_id}->{$a[0]}->{leaf_node} = $id;
            }
            else{
                $h->{$tree_id}->{$a[0]}->{par} = $a[1];
                $h->{$tree_id}->{$a[0]}->{leaf_node} = "NA";
            }
        } 
        elsif($tag == 1 && $_ =~ /------/){
# hit it the second time, go back to the original state
            $tag = -1;
        }
    }
    close fh_;
    return $h;
}


sub read_tree_assignment{
    my ($f, $h) = @_;
    my $tag = -1;
    my $tree_id;
    open fh_, "<$f" or die $!;
    while(<fh_>){
        if($tag == -1 && $_ !~ /^Tree \d+:$/){
# not open yet
            next;
        }
        elsif($tag == -1 && $_ =~ /^Tree \d+:$/){
            ($tree_id) = ($_ =~ /^Tree (\d+):/);
# this will open the door for tree structure
            $tag = 0;
        }
        elsif($tag == 0 && $_ !~ /Data matrix and reconstructed states for internal nodes/ && $_ =~ /^Tree \d+:$/){
            ($tree_id) = ($_ =~ /^Tree (\d+):/);
            next;
        }
        elsif($tag == 0 && $_ !~ /Data matrix and reconstructed states for internal nodes/ && $_ !~ /^Tree \d+:$/){
            next;
        } 
        elsif($tag == 0 && $_ =~ /Data matrix and reconstructed states for internal nodes/){
            $tag = 1;
            next;
        }
        elsif($tag == 1 && $_ !~ /------/){
            next;
        }
        elsif($tag == 1 && $_ =~ /------/){
            $tag = 2;
            next;
        }
        elsif($tag == 2 && $_ !~ /^\s+$/){
# now comes finally the first table
            chomp;
            my @a = split(/\s+/, $_);
            if(defined $h->{$tree_id}->{$a[0]}->{char}){
                $h->{$tree_id}->{$a[0]}->{char} = $h->{$tree_id}->{$a[0]}->{char} . $a[1];
            } 
            else{
                $h->{$tree_id}->{$a[0]}->{char} = $a[1];
            }
        }
        elsif($tag == 2 && $_ =~ /^\s+$/){
# now comes to the end of the first table of characters 
            $tag = 0;
            next;
        }
    }
    close fh_;
    return $h;
}

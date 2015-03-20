#!/usr/bin/perl -w

use strict;
use LWP::Simple;
use Data::Dumper;
use CGI; 
use JSON qw(decode_json);
use List::Util qw/shuffle/;

#print $cgi->header;
print "Content-type:text/html\n\n";

print <<END_HTML;

<html>
<head></head>
<body>
<form action="" method="post" enctype="multipart/form-data">
	Type: <input type="text" name="tag">
	<br/>
	<input type="submit" name="Submit" value="go">
	<input type="reset" name="Reset" value="again">
	<input type="submit" name="Random" value="try me">
</form>
</body>
</html>

END_HTML

my $cgi = new CGI;
my %data;
$data{tag} = $cgi->param('tag');

# --- Randomizer
my $wordlist = '/usr/share/dict/words';
my $length = int(rand(20));
my @words;

open WORDS, '<', $wordlist or die "Cannot open $wordlist:$!";

while (my $word = <WORDS>) 
{
	chomp($word);
	push @words, $word if (length($word) == $length);
}

close WORDS;

my @shuffled_words = shuffle(@words);
# Ends Randomizer


if ($data{tag} eq "")
{
$data{tag} = $shuffled_words[0];
}
else
{
	$data{tag} = $data{tag};
}

# Get the URL
my $url = 'https://api.instagram.com/v1/tags/' . $data{tag} . '/media/recent?client_id=1380a4aa6d864edf88f3e03439947c04';

my $json = get ($url);
die "not $url" unless defined $json;

my $decoded = decode_json ($json);

#print Dumper $decoded;

# Display
print "<p>$data{tag}</p><br/><br/>";
foreach my $f ( @{ $decoded->{'data'}})
	{
		print "<img src='$f->{'images'}{'low_resolution'}{'url'}' /><br/>";
	}

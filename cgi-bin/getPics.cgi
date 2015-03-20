#!/usr/bin/perl -w

use strict;
use LWP::Simple;
use Data::Dumper;
use JSON qw(decode_json);
use CGI; 

my $cgi = new CGI;

my %data;
$data{tag} = $cgi->param('tag');

my $url = 'https://api.instagram.com/v1/tags/' . $data{tag} . '/media/recent?client_id=1380a4aa6d864edf88f3e03439947c04';

my $json = get ($url);
die "not $url" unless defined $json;

my $decoded = decode_json ($json);

#print Dumper $decoded;
#print $cgi->header;

print "Content-type:text/html\n\n";

foreach my $f ( @{ $decoded->{'data'}})
	{
		print "<img src='$f->{'images'}{'low_resolution'}{'url'}' /><br/>";
	}

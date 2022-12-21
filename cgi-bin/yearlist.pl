#!/usr/bin/perl -W
#!/usr/bin/perl -X TODO this instead of -W

print "Content-Type: application/json\n\n";

my $imagestorage = $ENV{"PHOTO_PATH"} . '/';

#use strict; #TODO why results error??
use JSON;

my @years = ();

for (glob ( $imagestorage . "*")){
	my $year = substr $_, length($imagestorage);

	if ( length($year) != 4) {next;};
	if ( int($year)  < 1950 ) {next;};
	if ( int($year)  > 2099 ) {next;};

	push(@years, $year); 
}

print to_json(\@years);

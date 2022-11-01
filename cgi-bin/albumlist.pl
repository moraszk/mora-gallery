#!/usr/bin/perl -W
#!/usr/bin/perl -X TODO this instead of -W

print "Content-Type: application/json\n\n";

my $year = $ENV{"year"} || "2022";
my $albumstorage = "/media/mora_photo/" . $year . '/';

my $descfilename = "/description.json";

#use strict; #TODO why results error??
use JSON;

my @albums = ();

for (glob ( $albumstorage . "*")){
	my $albumname = (substr $_, length($albumstorage)); 
	my $desc = (substr $_, length($albumstorage));
	my $thumbnail = "null";

	eval {
		my $descfile = ($_ . $descfilename);
		my $json_desc = do {
		   open(my $json_fh, "<:encoding(UTF-8)", $descfile)
		      or die("Can't open description: $!\n");
		   local $/;
		   <$json_fh>
		};	

		my $json = JSON->new;
		my $data = $json->decode($json_desc);

		$desc = $data->{description};
		$thumbnail = $data->{thumbnail};
	};

	push(@albums, {
		'year' => $year,
		'name' => $albumname,
		'desc' => $desc,
		'thumbnail' => $thumbnail,
			});
}

print to_json(\@albums);

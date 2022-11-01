#!/usr/bin/perl -W
#!/usr/bin/perl -X TODO this instead of -W

print "Content-Type: application/json\n\n";

my $imagestorage = "/media/mora_photo/";
my $imageuriprefix = $ENV{"year"} . "/" . $ENV{"album"} . "/";
my $imageroot = $imagestorage . $imageuriprefix ;
my $size = $ENV{"size"} || "2048";

#use strict; #TODO why results error??
use Image::Info qw(image_info dim);
use JSON;

my @photoes = ();

for (glob ( $imageroot . "*.*")){
	my $w = 0;
	my $h = 0;
	eval{
		 my $info = image_info($_);
		 if (my $error = $info->{error}) {
			 next;
		 }
		 ($w, $h) = dim($info);
		 if ($w > $h){
			$h = int($h * $size / $w);
		 	$w = int($size);
		 } else {
			$w = int($w * $size / $h);
		 	$h = int($size);
		 }
	} or next;
	push(@photoes, {
		'filename' => (substr $_, length($imagestorage)),
		'height' => $h,
		'width' => $w,
			});
}

print to_json(\@photoes);

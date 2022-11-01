#!/usr/bin/perl -W
#!/usr/bin/perl -X TODO this instead of -W

#use strict; #TODO WHY THROWS AN ERROR?????
use CGI;
use Image::Magick;

my $imagestorage = "/media/mora_photo/";
my $imageuri = $ENV{"photo"};
my $format = $ENV{"format"} || "jpeg";

my $image = Image::Magick->new;
$image->Read( $imagestorage . $imageuri );
$image->Strip();
$image->Set(quality => 95);
$image->Thumbnail(geometry => $ENV{"size"},filter=>'Triangle');

if ( $ENV{"watermark"} ){
	my $logo = Image::Magick->new;
	$logo->Read( $ENV{"watermark"} );
	$logo->Thumbnail(geometry => "450");

	$image->Composite(
	    image   => $logo,
	    gravity => 'southeast',
	);
}

my $q = new CGI;

if ($format eq "webp"){
print $q->header( -type => "image/webp" );
binmode STDOUT;
$image->Write( "webp:-" );
}
else
{
print $q->header( -type => "image/jpeg" );
binmode STDOUT;
$image->Write( "jpeg:-" );
}

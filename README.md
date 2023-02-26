Móra Gallery
============

# Installation

 * Clone this repo to /srv/
 * Mount the gallery at /media/mora\_photo
 * Install the requirements:
```bash
apt install nginx spawn-fcgi fcgiwrap libjson-perl perlmagick libimage-info-perl libfcgi-perl libcgi-session-perl nginx-extras
apt install python3 python3-willow python3-opencv python3-waitress
```
 * Install the ```systemd``` unit
```bash
ln -s /srv/mora-gallery/gallery.system /etc/systemd/system/gallery.system
systemctl daemon-reload
systemctl enable gallery
systemctl start gallery
```
 * Configure other things
```bash
mkdir /var/run/nginx-cache /var/run/nginx-cache2
chown www-data /var/run/nginx-ca*
```

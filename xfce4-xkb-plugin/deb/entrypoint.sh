#!/bin/sh -x
# Workdir: /home/builder/build

if [ -n "$TARGET" ]; then
	DEBEMAIL='pod.pavel@gmail.com'
	DEBFULLNAME='Pavel Podkorytov'
	PATCHDIR='patches'
	
	# Build package
	[ ! -d 'DEBS' ] && mkdir -p DEBS
	apt-get source --download-only xfce4-xkb-plugin
	dpkg-source -x *.dsc

	WORKDIR=$(basename $(find ./ -maxdepth 1 -type d -iname "$TARGET*"))
	[ ! -d "$WORKDIR/$PATCHDIR" ] && mkdir -p "$WORKDIR/$PATCHDIR"
	cp $PATCHDIR/*.patch $WORKDIR/$PATCHDIR
	find $WORKDIR/$PATCHDIR -iname '*.patch' | xargs -n1 basename > $WORKDIR/$PATCHDIR/series
	cd $WORKDIR
	dch -i 'Added font-selection pathces'
	dpkg-buildpackage -rfakeroot -b
	mv ../*.deb ../DEBS
else
	echo 'Usage: TARGET=package entrypoint.sh'
	exit 1
fi

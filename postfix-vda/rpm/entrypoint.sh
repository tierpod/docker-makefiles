#!/bin/sh -x

if [ -n "$TARGET" ]; then
	# Create SOURCES directory
	[ -d 'SOURCES' ] || mkdir SOURCES
	# Download and extract src.rpm to SOURCES
	cd SOURCES
	yumdownloader --source postfix
	rpm2cpio *.src.rpm | cpio --extract --make-directories --verbose
	cd ../
	spectool -g -R SPECS/$TARGET
	# Build rpm package
	rpmbuild -ba SPECS/$TARGET
else
	echo 'Usage: TARGET=project.spec entrypoint.sh'
	exit 1
fi

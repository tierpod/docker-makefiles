#!/bin/sh -x

if [ -n "$TARGET" ] && [ -n "$BUILD_NUMBER" ]; then
	# Create SOURCES directory
	[ -d 'SOURCES' ] || mkdir SOURCES
	# Download and extract src.rpm to SOURCES
	cd SOURCES
	yumdownloader --source postfix
	rpm2cpio *.src.rpm | cpio --extract --make-directories --verbose
	cd ../
	spectool -g -R SPECS/$TARGET
	# Build rpm package
	rpmbuild --define "BUILD_NUMBER $BUILD_NUMBER" -ba SPECS/$TARGET
else
	echo 'Usage: TARGET=project BUILD_NUMBER=0 entrypoint.sh'
	exit 1
fi

#!/bin/sh -x

if [ -n "$TARGET" ] && [ -n "$BUILD_NUMBER" ]; then
	# Download source
	[ -d 'SOURCES' ] || mkdir SOURCES
	spectool -g -R SPECS/$TARGET
	# Build rpm package
	rpmbuild --define "build_number $BUILD_NUMBER" -ba SPECS/$TARGET
else
	echo 'Usage: TARGET=package.spec BUILD_NUMBER=0 entrypoint.sh'
	exit 1
fi

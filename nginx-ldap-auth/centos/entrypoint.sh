#!/bin/sh -x

if [ -n "$TARGET" ]; then
	# Create SOURCES directory
	[ -d 'SOURCES' ] || mkdir SOURCES
	spectool -g -R SPECS/$TARGET
	# Build rpm package
	rpmbuild -ba SPECS/$TARGET
else
	echo 'Usage: TARGET=project.spec entrypoint.sh'
	exit 1
fi

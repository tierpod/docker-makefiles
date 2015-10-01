#!/bin/sh -x
# Workdir: /home/builder/build

if [ -n "$TARGET" ]; then
	cd $TARGET
	cmake .
	make
else
	echo 'Usage: TARGET=package entrypoint.sh'
	exit 1
fi

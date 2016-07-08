#!/bin/bash

set -e

usage() {
	echo 'Usage: USER=builder USERID=1000 GROUPID=1000 TARGET=package.spec entrypoint.sh'
}

runas() {
	su $GUEST_USER -c "$@"
}

create_user() {
	echo "Create user: $GUEST_USER ($GUEST_USERID:$GUEST_GROUPID)"
	groupadd -g $GUEST_GROUPID $GUEST_USER
	useradd -m -s /bin/bash -u $GUEST_USERID -g $GUEST_GROUPID $GUEST_USER
}

build() {
	echo "Prepare rpmbuild directory tree"
	touch /home/$GUEST_USER/.rpmmacros
	chown $GUEST_USERID:$GUEST_GROUPID /home/$GUEST_USER/.rpmmacros
	runas "rpmdev-setuptree"
	cd /home/$GUEST_USER/rpmbuild

	echo "Download sources"
	[ -d 'SOURCES' ] || runas "mkdir SOURCES"
	runas "spectool -g -R SPECS/$TARGET"

	echo "Build rpm package from spec $TARGET"
	runas "rpmbuild --define 'release $RELEASE' -ba SPECS/$TARGET"
}

GUEST_USER=${USER:-builder}
GUEST_USERID=${USERID:-1000}
GUEST_GROUPID=${GROUPID:-1000}

if [ -n "$TARGET" ]; then
	create_user
	build
else
	usage
	exit 1
fi

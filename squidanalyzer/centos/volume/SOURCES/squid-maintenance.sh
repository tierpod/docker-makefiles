#!/bin/sh

set -e

PATH=/sbin:/bin:/usr/sbin:/usr/bin
PROGNAME=$(basename $0)

logger -t $PROGNAME 'Start squid maintenance'

logger -t $PROGNAME 'Rotate squid logs'
squid -k rotate

sleep 5

logger -t $PROGNAME 'Generate squidanalyzer reports'
squid-analyzer --no-year-stat --no-week-stat --preserve 2 -j 2

logger -t $PROGNAME 'End squid maintenance'

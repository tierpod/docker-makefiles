FROM builder-fedora23
MAINTAINER Pavel Podkorytov <pod.pavel@gmail.com>

ENV TARGET=xfce4-xkb-plugin.git.spec

# Install dependencies from spec-file
USER root
ADD ["volume/SPECS/$TARGET", "/tmp/"]
RUN dnf builddep -y /tmp/$TARGET
USER builder

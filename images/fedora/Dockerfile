FROM fedora:22
MAINTAINER Pavel Podkorytov <pod.pavel@gmail.com>

ENV USERID=1000
ENV GROUPID=1000

# Install main dependencies
RUN dnf install -y rpmdevtools make yum-utils '@Development Tools' 'dnf-command(builddep)' && \
    dnf clean all

# Create builder group and user
RUN groupadd -g $GROUPID builder && \
    useradd -m -s /bin/bash -u $USERID -g $GROUPID builder

# Setup user-specific settings
USER builder
RUN mkdir ~/build && \
    echo '%_topdir /home/builder/build' > ~/.rpmmacros

WORKDIR /home/builder/build
CMD /entrypoint.sh

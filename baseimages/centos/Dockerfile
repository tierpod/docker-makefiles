FROM centos:7
MAINTAINER Pavel Podkorytov <pod.pavel@gmail.com>

ENV USERID=1000
ENV GROUPID=1000

# Enable Centos-Sources repos
RUN sed -i 's/enabled=0/enabled=1/' /etc/yum.repos.d/CentOS-Sources.repo

# Install main dependencies
RUN yum install -y epel-release rpmdevtools make yum-utils '@Development Tools' && \
    yum clean all

# Create builder group and user
RUN groupadd -g $GROUPID builder && \
    useradd -m -s /bin/bash -u $USERID -g $GROUPID builder

# Setup user-specific settings
USER builder
RUN mkdir ~/build && \
    echo '%_topdir /home/builder/build' > ~/.rpmmacros

WORKDIR /home/builder/build

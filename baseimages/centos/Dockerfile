FROM centos:7
MAINTAINER Pavel Podkorytov <pod.pavel@gmail.com>

# Install main dependencies
RUN sed -i 's/enabled=0/enabled=1/' /etc/yum.repos.d/CentOS-Sources.repo && \
    yum install -y epel-release rpmdevtools make yum-utils '@Development Tools' && \
    yum clean all

# Add default entrypoint
ADD ["entrypoint.sh", "/entrypoint.sh"]
RUN chmod +x /entrypoint.sh
CMD /entrypoint.sh

# Install dependencies from spec
ONBUILD ARG TARGET
ONBUILD ADD ["volume/SPECS/$TARGET", "/tmp/"]
ONBUILD RUN yum-builddep -y /tmp/$TARGET

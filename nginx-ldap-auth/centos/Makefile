IMAGE = builder-centos_nginx-auth-ldap
TARGET = nginx.spec

include ../../include/common.mk

SOURCES = $(TMP_DIR)/volume/SOURCES
SPECS = $(TMP_DIR)/volume/SPECS

NGINX_NAME = nginx-1.8.0-1.el7.ngx.src.rpm
NGINX_URL = http://nginx.org/packages/rhel/7/SRPMS/$(NGINX_NAME)

prepare: $(SOURCES) $(SOURCES)/$(NGINX_NAME)
	cd $(SOURCES) && \
	rpm2cpio $(NGINX_NAME) | cpio --extract --make-directories --verbose

$(SOURCES):
	mkdir -p $(SOURCES)

$(SOURCES)/$(NGINX_NAME):
	curl $(NGINX_URL) -o $(SOURCES)/$(NGINX_NAME)

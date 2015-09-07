IMAGE = builder-nginx-auth-ldap
TARGET = nginx.spec

include ../../include/common.mk

SOURCES = build-env/SOURCES
SPECS = build-env/SPECS

NGINX_NAME = nginx-1.8.0-1.el7.ngx.src.rpm
NGINX_URL = http://nginx.org/packages/rhel/7/SRPMS/$(NGINX_NAME)

AUTH_LDAP_NAME = master.zip
AUTH_LDAP_URL = https://github.com/kvspb/nginx-auth-ldap/archive/$(AUTH_LDAP_NAME)

prepare: $(SOURCES) $(SOURCES)/$(NGINX_NAME) $(SOURCES)/$(AUTH_LDAP_NAME)
	cd $(SOURCES) && \
	rpm2cpio $(NGINX_NAME) | cpio --extract --make-directories --verbose && \
	unzip $(AUTH_LDAP_NAME) -d ../BUILD

$(SOURCES):
	mkdir -p $(SOURCES)

$(SOURCES)/$(NGINX_NAME):
	curl $(NGINX_URL) -o $(SOURCES)/$(NGINX_NAME)

$(SOURCES)/$(AUTH_LDAP_NAME):
	curl -L $(AUTH_LDAP_URL) -o $(SOURCES)/$(AUTH_LDAP_NAME)

IMAGE = builder-centos_postfix-vda
TARGET = postfix-vda.spec

include ../../include/common.mk

SOURCES = build-env/SOURCES
SPECS = build-env/SPECS

VDA_NAME = postfix-vda-v13-2.10.0.patch
VDA_URL = http://vda.sourceforge.net/VDA/$(VDA_NAME)

prepare: $(SOURCES) $(SOURCES)/$(VDA_NAME)

$(SOURCES):
	mkdir -p $(SOURCES)

$(SOURCES)/$(VDA_NAME):
	curl $(VDA_URL) -o $(SOURCES)/$(VDA_NAME)

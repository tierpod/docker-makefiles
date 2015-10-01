IMAGE = builder-xkb-switch
TARGET = xkb-switch

include ../../include/common.mk

SOURCES = build-env/$(TARGET)
SOURCES_GIT = git@github.com:ierton/xkb-switch.git

prepare: $(SOURCES)

$(SOURCES):
	git clone $(SOURCES_GIT) $(SOURCES)

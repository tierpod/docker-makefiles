USERID := $(shell id -u)
GROUPID := $(shell id -g)

BUILD_NUMBER ?= 0
TARGET ?= $(error TARGET is not defined)
IMAGE ?= $(error IMAGE is not defined)

ifdef COMMIT
RELEASE = $(BUILD_NUMBER).git$(COMMIT)
else
RELEASE = $(BUILD_NUMBER)
endif

TMP_DIR = /tmp/$(IMAGE)
DOCKER_VOLUME = -v $(TMP_DIR)/volume:/home/builder/rpmbuild
DOCKER_ENV = -e TARGET=$(TARGET) -e RELEASE=$(RELEASE)

.PHONY: all show clean clean-all package shell prepare

all: show image package

show:
	@echo '-------------------------------------------------------'
	@echo 'USERID=$(USERID) GROUPID=$(GROUPID) RELEASE=$(RELEASE)'
	@echo 'IMAGE=$(IMAGE) TARGET=$(TARGET) COMMIT=$(COMMIT)'
	@echo '-------------------------------------------------------'

Dockerfile:
	@cat Dockerfile.template \
		| sed -e "s@{userid}@$(USERID)@" -e "s@{groupid}@$(GROUPID)@" -e "s@{target}@$(TARGET)@" \
		| tee $@

image: show Dockerfile
	docker build -t $(IMAGE) .
ifneq ($(BUILD_NUMBER), 0)
	docker tag $(IMAGE):latest $(IMAGE):$(BUILD_NUMBER)
endif

clean:
	rm -rf Dockerfile $(TMP_DIR)

clean-all: clean
	-docker rmi $(IMAGE):$(BUILD_NUMBER)

build-env: $(TMP_DIR)
	-cp -r volume $(TMP_DIR)

package: build-env prepare
	docker run --rm $(DOCKER_VOLUME) $(DOCKER_ENV) $(IMAGE)

shell: build-env prepare
	docker run --rm -it -u root $(DOCKER_VOLUME) $(DOCKER_ENV) $(IMAGE) /bin/bash

$(TMP_DIR):
	mkdir -p $@

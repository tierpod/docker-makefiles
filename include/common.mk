# Variables
USERID := $(shell id -u)
GROUPID := $(shell id -g)
DOCKERFILE := Dockerfile

BUILD_NUMBER ?= latest
IMAGE ?= $(error IMAGE is not defined)

ifdef COMMIT
RELEASE := $(BUILD_NUMBER).git$(COMMIT)
else
RELEASE := $(BUILD_NUMBER)
endif

TMP_DIR := /docker-home/$(IMAGE)
DOCKER_VOLUME := -v $(TMP_DIR)/volume:/home/builder/rpmbuild
DOCKER_ENV := -e RELEASE=$(RELEASE) -e USERID=$(USERID) -e GROUPID=$(GROUPID)

ifdef TARGET
DOCKER_BUILDARG := --build-arg TARGET=$(TARGET)
DOCKER_ENV := -e TARGET=$(TARGET) $(DOCKER_ENV)
else
DOCKER_BUILDARG :=
endif

# Targets
.PHONY: all show clean clean-image build-env package shell prepare

all: show image package

show:
	@echo '-------------------------------------------------------'
	@echo '          IMAGE $(IMAGE)'
	@echo '     DOCKERFILE $(DOCKERFILE)'
	@echo '     DOCKER_ENV $(DOCKER_ENV)'
	@echo '  DOCKER_VOLUME $(DOCKER_VOLUME)'
	@echo 'DOCKER_BUILDARG $(DOCKER_BUILDARG)'
	@echo '-------------------------------------------------------'

image: show
	docker build $(DOCKER_BUILDARG) -t $(IMAGE) -f $(DOCKERFILE) .
ifneq ($(BUILD_NUMBER), latest)
	docker tag $(IMAGE):latest $(IMAGE):$(BUILD_NUMBER)
endif

clean:
	rm -rf $(TMP_DIR)

clean-image: clean
	-docker rmi $(IMAGE):$(BUILD_NUMBER)

build-env: $(TMP_DIR)
	-cp -r volume $(TMP_DIR)

package: show build-env prepare
	docker run --rm $(DOCKER_VOLUME) $(DOCKER_ENV) $(IMAGE)

shell: show build-env prepare
	docker run --rm -it -u root $(DOCKER_VOLUME) $(DOCKER_ENV) $(IMAGE) /bin/bash

$(TMP_DIR):
	mkdir -p $@


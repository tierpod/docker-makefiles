USERID = $(shell id -u)
GROUPID = $(shell id -g)

.PHONY: all show clean clean-all package shell prepare

BUILD_NUMBER ?= 0
TARGET ?= $(error TARGET is not defined)
IMAGE ?= $(error IMAGE is not defined)

ifdef COMMIT
RELEASE = $(BUILD_NUMBER).git$(COMMIT)
else
RELEASE = $(BUILD_NUMBER)
endif

DOCKER_OPTS = --rm -v $(PWD)/build-env/:/home/builder/build -e TARGET=$(TARGET) -e RELEASE=$(RELEASE)

all: show image package

show:
	@echo ' USERID=$(USERID) GROUPID=$(GROUPID) RELEASE=$(RELEASE)'
	@echo ' IMAGE=$(IMAGE) TARGET=$(TARGET) COMMIT=$(COMMIT)'
	@echo '-------------------------------------------------------'

Dockerfile:
	@cat Dockerfile.template | \
		sed -e "s@{userid}@$(USERID)@" -e "s@{groupid}@$(GROUPID)@" -e "s@{target}@$(TARGET)@" | \
		tee Dockerfile

image: show Dockerfile
	docker build -t $(IMAGE) .
ifneq ($(BUILD_NUMBER), 0)
	docker tag $(IMAGE):latest $(IMAGE):$(BUILD_NUMBER)
endif

clean:
	rm -rf Dockerfile build-env

clean-all: clean
	docker rmi $(IMAGE):$(BUILD_NUMBER)

build-env:
	cp -r volume build-env

package: build-env prepare
	docker run $(DOCKER_OPTS) $(IMAGE)

shell: build-env prepare
	docker run -it -u root $(DOCKER_OPTS) $(IMAGE) /bin/bash

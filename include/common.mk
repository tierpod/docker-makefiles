USERID = $(shell id -u)
GROUPID = $(shell id -g)

.PHONY: all show clean package shell prepare

ifndef BUILD_NUMBER
$(info BUILD_NUMBER set to 0)
BUILD_NUMBER = 0
endif

ifndef TARGET
$(error TARGET is not set)
endif

ifndef IMAGE
$(error IMAGE is not set)
endif

all: show image package

show:
	@echo '==> IMAGE=$(IMAGE) BUILD_NUMBER=$(BUILD_NUMBER) TARGET=$(TARGET) USERID=$(USERID) GROUPID=$(GROUPID)'

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

build-env:
	cp -r volume build-env

package: build-env prepare
	docker run --rm -v $(PWD)/build-env/:/home/builder/build \
		-e BUILD_NUMBER=$(BUILD_NUMBER) -e TARGET=$(TARGET) -t $(IMAGE)

shell: build-env prepare
	docker run -it --rm -v $(PWD)/build-env/:/home/builder/build \
		-e BUILD_NUMBER=$(BUILD_NUMBER) -e TARGET=$(TARGET) -t $(IMAGE) /bin/bash

# docker-makefiles

Пример совместного использования Makefile + docker. Компиляция софта внутри
docker контейнеров.

## Использование

```
cd sarg/rpm
make image
make package
```

## Makefile в поддиректориях

```
# имя docker image
IMAGE = builder
# цели для сборки
TARGET = project.spec
# добавить git commit в RELEASE
COMMIT = $(shell git rev-parse --short HEAD)
# либо
# COMMIT = $(shell cd /path/to/source/ && git rev-parse --short HEAD)

# действия, выполняемые до запуска компиляции на хосте
prepare:
	-mkdir build-env/SOURCES
	tar -cf build-env/SOURCES/project.tar path/to/project

# подключить общий makefile
include path/to/common.mk
```

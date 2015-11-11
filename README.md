# docker-makefiles

Пример совместного использования Makefile + docker. Компиляция софта внутри
docker контейнеров.

## Использование

* Собрать baseimage для нужного дистрибутива. Содержит все нужные
  инструменты для компиляции:

```
cd baseimage/fedora/
make image
cd -
```

* На основе собранного baseimage, собрать image, внутри которого будет
  компилироваться программа. Содержит все зависимости, для сборки программы.

```
cd sarg/centos
make image
```

* Запустить сборку самой программы.

```
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

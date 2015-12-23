# docker-makefiles

Пример совместного использования Makefile + docker. Компиляция программ внутри
docker контейнеров. Можно комбинировать с jenkins.

## Идея

Нужно создать docker-image, который будет содержать все инструменты,
необходимые для компиляции программ внутри него (назовём его, к примеру,
builder-fedora). Далее, используем его как базовый - если уже установленных
компонент нам достаточно, то просто запускаем docker container и запускаем
компиляцию. Если необходимы ещё какие-нибудь зависимости для сборки, то
собираем ещё один docker image для компиляции конкретной программы внутри этого
image-а (назовём его, к примеру, builder-fedora_keepassx).

Для этого нам понадобится 2 makefile-а. Они будут содержать описание действий
по созданию image-а и запуску container-а, а так же предварительные действия
для подготовки (prepare):

* Первый основной Makefile, который находится в 'include/common.mk'. Он содержит
  всю логику по работе с docker-ом и глобальный переменные.
* Второй дополнительный Makefile, который находится в поддиректории программы,
  которую нужно скомпилировать. Он содержит описание действия prepare (скачать
  исходный код, создать директории и подобное).

## Использование

* Сначала, нужно собрать baseimage для нужного дистрибутива:

```
cd baseimage/fedora/
make image
cd -
```

* На основе собранного baseimage, собрать image, внутри которого будем
  компилировать программу:

```
cd keepassx/fedora
make image
```

* Запустить container и скомпилировать программу внутри него:

```
make package
```

Примеры файлов Makefile-ов, entrypoint.sh можно посмотреть в этом репозитории.

## Использоваение в своём проекте

* include/common.mk общий, нужно его скачать в свой проект.
* project/Makefile:

```
# имя docker image
IMAGE = builder-fedora_project
# цели для сборки
TARGET = project.spec
# добавить git commit в переменную RELEASE
COMMIT = $(shell git rev-parse --short HEAD)
# COMMIT = $(shell cd /path/to/source/ && git rev-parse --short HEAD)

# действия, выполняемые до запуска компиляции на хосте
prepare:
	-mkdir build-env/SOURCES
	tar -cf build-env/SOURCES/project.tar path/to/project

# подключить общий makefile
include ../include/common.mk
```

* подготовить baseimages/Dockerfile.template, baseimages/entrypoint.sh (если
  необходимо), project/Dockerfile (если необходимо), project/entrypoint.sh
  (если необходимо).

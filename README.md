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
image-а.

Для этого нам понадобится 2 Makefile-а. Они будут содержать описание действий
по созданию image-а и запуску container-а, а так же предварительные действия
для подготовки к компиляции (prepare):

* Первый основной Makefile находится в 'include/common.mk'. Он содержит
  всю логику по работе с docker-ом и глобальный переменные.
* Второй дополнительный Makefile находится в поддиректории программы,
  которую нужно скомпилировать. Он содержит описание действия prepare (скачать
  исходный код или патчи, создать директории и подобное).

## Использование

* Создаём временную директорию TMP_DIR (по-умолчанию /docker-home, можно
  изменить в common.mk), в которой будет происходить сборка пакетов. Эта
  директорию пробрасывается в builder-container через опцию -v. На неё нужно
  выдать такие права, чтобы наш пользователь имел туда доступ rw.  Если мы
  используем selinux, то так же необходимо назначить правильный контекст.

```
mkdir /docker-home
chown -R myuser:myuser /docker-home
chcon -Rv --type=svirt_sandbox_file_t /docker-home
```

* Затем, нужно собрать baseimage для нужного дистрибутива:

```
cd baseimage/fedora/
make image
cd -
```

* На основе собранного baseimage, собрать builder-image, внутри которого будем
  компилировать программу:

```
cd squidanalyzer/centos
make image
```

* Запустить container и скомпилировать программу внутри него:

```
make package
```

* Все артефакты билдера находятся в TMP_DIR (по-умолчанию,
  /docker-root/builder-name)

Примеры файлов Makefile-ов, entrypoint.sh можно посмотреть в этом репозитории.

## Использоваение в своём проекте

* include/common.mk общий, нужно его скачать в свой проект.
* project/Makefile:

```
# имя docker image
IMAGE = builder-fedora_project
# цель для сборки
TARGET = project.spec
# добавить git commit в переменную RELEASE
COMMIT = $(shell git rev-parse --short HEAD)
# COMMIT = $(shell cd /path/to/source/ && git rev-parse --short HEAD)

# действия, выполняемые до запуска компиляции на хосте
prepare:
    -mkdir $(TMP_DIR)/SOURCES
    tar -cf $(TMP_DIR)/SOURCES/project.tar path/to/project

# подключить общий makefile
include ../include/common.mk
```

* подготовить baseimages/Dockerfile.template, baseimages/entrypoint.sh (если
  необходимо), project/Dockerfile (если необходимо), project/entrypoint.sh
  (если необходимо).

## selinux

Чтобы selinux не мешал нам работать.

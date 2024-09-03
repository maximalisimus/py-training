#!/bin/bash

# Archlinux
$ sudo pacman -S tk tcl

# Debian
$ sudo apt-get install tk tcl

# Fedora
$ sudo dnf -y install tk tcl

# RHEL, CentOS, Oracle Linux
$ sudo yum makecache --refresh
$ sudo yum -y install tk tcl


# search package lib
$ objdump -p ./helloworld | grep NEEDED
#   NEEDED			libc.so.6

$ dpkg -S libc.so.6
# libc6:i386: /lib/i386-linux-gnu/libc.so.6
# libc6:amd64: /lib/x86_64-linux-gnu/libc.so.6
# libc6:i386: /lib32/libc.so.6
# package name libc6

$ nano package/DEBIAN/control

Package: hellolosst
Version: 1.0
Section: unknown
Priority: optional
Depends: libc6
Architecture: amd64
Essential: no
Installed-Size: 20
Maintainer: losst.pro <admin@losst.pro>
Description: Print hello from losst line

Package - имя пакета;
Version - версия программы в пакете, будет использована при обновлении пакета;
Section - категория пакета, позволяет определить зачем он нужен;
Priority - важность пакета, для новых пакетов, которые ни с чем не конфликтуют обычно прописывают optional, кроме того доступны значения required, important или standard;
Depends - от каких пакетов зависит ваш пакет, он не может быть установлен, пока не установлены эти пакеты;
Recommends - необязательные пакеты, но тем не менее они обычно устанавливаются по умолчанию в apt;
Conflicts - пакет не будет установлен, пока в системе присутствуют перечисленные здесь пакеты;
Architecture - архитектура системы, в которой можно установить этот пакет, доступные значения: i386, amd64, all, последнее означает, что архитектура не имеет значения;
Installed-Size - общий размер программы после установки;
Maintainer - указывает кто собрал этот пакет и кто отвечает за его поддержку;
Description - краткое описание пакета.

$ nano package/DEBIAN/postinst

#!/bin/bash
echo "Hello from losst installed"

$ dpkg-deb --build ./package

$ sudo apt install ~/helloworld.deb

#!/bin/bash
for C in {40..47}; do
    echo -en "\e[${C}m$C "
done
echo ""
# цвета высокой интенсивности
for C in {100..107}; do
    echo -en "\e[${C}m$C "
done
echo ""
# 256 цветов
for C in {16..255}; do
    echo -en "\e[48;5;${C}m$C "
done
echo -e "\e(B\e[m"

exit 0

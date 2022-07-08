#!/bin/bash
for file in "$PWD"/* # Цикл
do
	if [ -d "$file" ] # Проверка что папка
		then tar -cvf ${file##"$PWD/"}.zip ${file##"$PWD/"}/; # Архивирование
	fi
done
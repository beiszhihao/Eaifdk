#!/bin/bash

. $EAIFDK_HOME/script/export.sh

number=0
for file_a in $1/*
do
	ext=${file_a##*.}
	if [ $ext = 'jpg' ];
	then
		number=$((number+1))
	fi
done

mark=''
speed=1
echo "Start auto label"
for file_a in $1/*
do
        ext=${file_a##*.}
        if [ $ext = 'jpg' ];
        then
		printf "Progress: %d/%d\n" "${speed}" "${number}"
                $PYTHON $AUTO_LABEL ${AUTO_LABEL_MODEL} ${file_a}
		speed=$((speed + 1))
        fi
done
echo "Auto label done"

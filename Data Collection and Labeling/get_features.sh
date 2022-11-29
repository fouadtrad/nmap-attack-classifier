#!/bin/sh

#Author: Fouad Trad

if [ $# -eq 2 ]
	then
	sudo build-files/src/kdd99extractor -e $1>>$2
elif [ $# -eq 1 ]
	then
	sudo build-files/src/kdd99extractor>>$1
fi

#!/bin/sh

export SDL_AUDIODRIVER=dsp
export SDL_NOMOUSE=1
export HOME=/mnt/int_sd

/mnt/game/PyMenu/setVolume 255

FILE="/tmp/run"
while true
do
	if [ -f $FILE ]; then
		echo "File $FILE exists"
		sh $FILE > /dev/ttyS1 2> /dev/ttyS1
		rm $FILE
	else
		sh /mnt/game/PyMenu/pymenu.sh > /dev/ttyS1 2> /dev/ttyS1
		echo "File $FILE does not exist"	
	fi
	sleep 1
done

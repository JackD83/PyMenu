#!/bin/sh

export SDL_AUDIODRIVER=dsp
export SDL_NOMOUSE=1
export HOME=/mnt/int_sd
export LD_LIBRARY_PATH=$LD_LIBRARY_PATH:$PWD/python/usr/lib
export PATH=$PATH:$PWD/python/usr/bin


python --version >> debug.txt 2>> debug.txt
python -c "print('test');" >>debug.txt 2>> debug.txt
find >> debug.txt 2>> debug.txt


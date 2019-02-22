#!/bin/sh

export SDL_AUDIODRIVER=dsp
export SDL_NOMOUSE=1
export HOME=/mnt/int_sd
export LD_LIBRARY_PATH=$PWD/python/usr/lib:$LD_LIBRARY_PATH
export PATH=$PWD/python/usr/bin:$PATH


python --version >> debug.txt 2>> debug.txt
python -c "print('test');" >>debug.txt 2>> debug.txt
find >> debug.txt 2>> debug.txt


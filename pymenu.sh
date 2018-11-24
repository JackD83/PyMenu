#!/bin/sh
export SDL_NOMOUSE=1
export SDL_AUDIODRIVER=dsp
cd "$(dirname "$0")"
python main.py >> /dev/ttyS1 2>> /dev/ttyS1

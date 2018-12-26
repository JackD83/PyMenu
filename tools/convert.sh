#!/bin/bash
#cd $(dirname "$0")
for var in "$@"
do
    filename=$(basename -- "$var")
    extension="${filename##*.}"
    filename="${filename%.*}"
    rm -r converterTemp
    mkdir converterTemp
    mkdir output
    ffmpeg -i "$var" -f image2 -vf fps=25 -vf scale=128:-1 -vframes 150 converterTemp/img%03d.png
    mogrify -gravity center -background none -extent 128x128 converterTemp/*.png
    montage converterTemp/*.png -geometry 128x -geometry '1x1+0+0<' -background none  png8:output/"$filename".anim.png
    rm -r converterTemp
done



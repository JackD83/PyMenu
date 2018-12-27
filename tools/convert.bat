rem download image magick from https://imagemagick.org/download/binaries/ImageMagick-7.0.8-20-Q16-x64-dll.exe
rem make sure to uncheck "install ffmpeg" during installation and install custom ffmpeg

@echo off


for %%x in (%*) do (
   echo Hey %%~x 
   call :encode "%%~x"
)

:encode
echo encoding "%~1"
for %%f in ("%~1") do SET filename=%%~nf

rmdir converterTemp /s /q
mkdir converterTemp
mkdir output
ffmpeg -i "%~1" -f image2 -r 25 -vf scale=128:-1 -vframes 156 "converterTemp\img%%03d.png"
magick mogrify -gravity center -background none -extent 128x128 converterTemp\*.png
magick montage converterTemp\*.png -geometry 128x -geometry "1x1+0+0<" -background none -quality 60 jpg:"output\%filename%.anim.jpg"
rmdir converterTemp /s /q

   


Menu System for the RS97

You need the custom firmware for your device.

RS97:
Only the RetroFW 1.1 and later is supported

https://github.com/retrofw/firmware

Install the provided ipk like any other emulator.
If you want to launch directly into PyMenu, run installer/install.dge with an app like commander.

Currently only the default gmenu2x is capable of installing new ipk packages!


Check https://boards.dingoonity.org/ingenic-jz4760-devices/ for any updates


Creation of animated previews:

The animated previews are a kind of custom format. Like the still preview images, their animated counterparts are just 128x128 pixel images stitched together in a grid and saved as one large image. To batch process a lot of videos, I created two converter scripts (windows and linux/macos) found under "tools" 

They rely on image magick and ffmpeg to convert any video to a 6 seconds preview animation.
Please use the latest versions of both tools. On windows, the version of ffmpg that comes with image magick is too old!

Simply call convert.sh with all the videos you want to convert as parameter (like ./convert.sh videos/* ). This will create a folder called "output" with all converted previews
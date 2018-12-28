Menu System for the RS97, PAP KIII Plus (K3P) and the Arcade Mini

You need the custom firmware for your device.

RS97:
Only the UselessRS97 internal firmware is supported
Follow the guides listed here:
https://boards.dingoonity.org/ingenic-jz4760-devices/uselessrs97-internal-firmware-for-revision-2-1/

K3P:
Install either https://drive.google.com/open?id=11AAbW4VpWk4XUtX9XjpKtyGHxVjmJlYL for the old device or 
https://drive.google.com/open?id=1thtFJg1ePUTPLdlulepzBM_tVpwg-gsV for the 16gb version.
(thx blackz1982)
They need to be installed on the internal sd-card

Arcade Mini:
Install instructions: https://boards.dingoonity.org/ingenic-jz4760-devices/custom-firmware-for-the-retro-arcade-mini/
 
1. Clone or copy the files from the repo next to the gmenu2x folder in /apps/. Folder has to be named "PyMenu"

2. PyMenu can be run by starting PyMenu/run.sh

3. If you want to make it your default launcher, run PyMenu/installer/install.dge. Run uninstall.dge to switch back to gmenunx. Try to start it using run.sh first!

Tested on UselessRS97 1.3 internal & external and K3P old version

Check https://boards.dingoonity.org/ingenic-jz4760-devices/ for any updatates


Creation of animated previews:

The animated previews are a kind of custom format. Like the still preview images, their animated counterparts are just 128x128 pixel images stiched together in a grid and saved as one large image. To batch process a lot of videos, I created two coverter scripts (windows and linux/macos) found under "tools" 

Thy rely on image magick and ffmpeg to convert any video to a 6 seconds preview animation.
Please use the latest versions of both tools. On windows, the version of ffmpg that comes with image magick is too old!

Simply call convert.sh with all the videos you want to convert as parameter (like ./convert.sh videos/* ). This will create a folder called "output" with all converted previews
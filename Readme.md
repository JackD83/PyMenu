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

1b. for the Arcade Mini or K3P
in the file config/config.json set:

RS97 = false
screenWidth = 480
screenHeight = 272

2. PyMenu can be run by starting PyMenu/run.sh

3. If you want to make it your default launcher, run PyMenu/installer/install.dge. Run uninstall.dge to switch back to gmenunx. Try to start it using run.sh first

Tested on UselessRS97 1.3 internal & external and K3P old version

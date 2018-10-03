Menu System for the RS97 and PAP KIII Plus

Currently only running on the RS97

Installation RS97:

1. You need the custom firmware for your device. Beginning with cf5836d4ccea7e006fff96060b4028d3c3c3abe7
only the UselessRS97 internal firmware is supported
Follow the guides listed here:
https://boards.dingoonity.org/ingenic-jz4760-devices/uselessrs97-internal-firmware-for-revision-2-1/
 

2. Clone or copy the files from this repo next to the gmenu2x folder in /apps/. Folder has to be named "PyMenu"

3. run PyMenu/python/install_useless.dge to install python

4. PyMenu can be run by starting PyMenu/run.sh

5. If you want to make it your default launcher, run PyMenu/installer/install.dge. Run uninstall.dge to switch back to gmenunx

Tested on UselessRS97 1.3 internal

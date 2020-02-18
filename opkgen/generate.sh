#!/bin/bash
mkdir tmp

VERSION=$(cat ../config/config_OpenDinguX.json | grep version | cut -d \" -f4)
echo "Version is: $VERSION"


mkdir -p tmp/data/pymenu
cp ../*.py tmp/data/pymenu/
cp ../*.sh tmp/data/pymenu/
cp ../*.dge tmp/data/pymenu/
cp ../*.png tmp/data/pymenu/
cp -r ../scandir tmp/data/pymenu/
cp -r ../config tmp/data/pymenu/
rm tmp/data/pymenu/config/lastPlayedData.json 2> /dev/null
rm tmp/data/pymenu/config/favourites.json 2> /dev/null
rm tmp/data/pymenu/config/config.json 2> /dev/null
mv tmp/data/pymenu/config/config_OpenDinguX.json tmp/data/pymenu/config/config.json


cp -r ../images tmp/data/pymenu/
cp -r ../installer tmp/data/pymenu/
#cp -r ../python tmp/data/home/retrofw/apps/pymenu/
cp -r ../theme tmp/data/pymenu/
cp ../setVolume tmp/data/pymenu/
cp ../setCPU tmp/data/pymenu/


cp install.dge tmp/data
cp pymenu.lnk tmp/data

OPK_NAME=PyMenu-Installer-${VERSION}.opk
echo ${OPK_NAME}

# create default.gcw0.desktop
cat > default.gcw0.desktop <<EOF
[Desktop Entry]
Name=PyMenu Installer 
Comment=Install PyMenu ${VERSION} on the device
Exec=install.dge
Terminal=true
Type=Application
StartupNotify=true
Icon=pymenu
Categories=applications;
EOF

# create opk
FLIST="default.gcw0.desktop"
FLIST="${FLIST} tmp/data/pymenu/pymenu.png"
FLIST="${FLIST} tmp/data/install.dge"
FLIST="${FLIST} tmp/data/pymenu.lnk"
FLIST="${FLIST} tmp/data/pymenu"

rm -f ${OPK_NAME}
mksquashfs ${FLIST} ${OPK_NAME} -all-root -no-xattrs -noappend -no-exports

cat default.gcw0.desktop
rm -f default.gcw0.desktop

rm -rf tmp





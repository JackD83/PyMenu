#!/bin/bash
mkdir tmp
mkdir tmp/control

VERSION=$(cat ../config/config.json | grep version | cut -d \" -f4)
echo "Version is: $VERSION"

cp debian-binary tmp
cp conffiles tmp/control/
cp control tmp/control/
#cp postinst tmp/control/
#cp preinst tmp/control/

sed -i s/{{VERSION}}/$VERSION/g tmp/control/control

mkdir -p tmp/data/home/retrofw/apps/pymenu
cp ../*.py tmp/data/home/retrofw/apps/pymenu/
cp ../*.sh tmp/data/home/retrofw/apps/pymenu/
cp ../*.dge tmp/data/home/retrofw/apps/pymenu/
cp ../*.png tmp/data/home/retrofw/apps/pymenu/
cp -r ../config tmp/data/home/retrofw/apps/pymenu/
cp -r ../images tmp/data/home/retrofw/apps/pymenu/
cp -r ../installer tmp/data/home/retrofw/apps/pymenu/
#cp -r ../python tmp/data/home/retrofw/apps/pymenu/
cp -r ../theme tmp/data/home/retrofw/apps/pymenu/

mkdir -p tmp/data/home/retrofw/apps/gmenu2x/sections/applications/
cp pymenu.lnk tmp/data/home/retrofw/apps/gmenu2x/sections/applications/

cd tmp/control

tar -czvf ../control.tar.gz --owner=0 --group=0 *

cd ../data
tar -czvf ../data.tar.gz --owner=0 --group=0 *

cd ..
ar rv ../pymenu-$VERSION.ipk control.tar.gz data.tar.gz debian-binary

cd .. 
rm -rf tmp







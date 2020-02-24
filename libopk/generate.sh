#!/bin/bash
mkdir tmp
mkdir tmp/control


cp debian-binary tmp
cp conffiles tmp/control/
cp control tmp/control/
#cp postinst tmp/control/
cp preinst tmp/control/


mkdir -p tmp/data/
cp -r ./usr tmp/data/


cd tmp/control

tar -czvf ../control.tar.gz --owner=0 --group=0 *

cd ../data
tar -czvf ../data.tar.gz --owner=0 --group=0 *

cd ..
ar rv ../libopk-1.0.0.ipk control.tar.gz data.tar.gz debian-binary

cd .. 
rm -rf tmp







#!/bin/bash -e

. /var/cache/build/packages-manual/common.sh

download_and_verify \
    smithlab \
    makedb \
    1.01 \
    6b8b21818c89cf7cd2cfc67e4d135ce87f13688d715c71f056cca70a03927e74 \
    https://github.com/smithlabcode/walt/archive/v\${version}.tar.gz \
    walt-\${version}

make --directory=src/walt makedb

mv src/walt/makedb .

shopt -s extglob
rm -rf !(makedb)
mv makedb makedb-walt

add_binary_path \
    smithlab \
    makedb

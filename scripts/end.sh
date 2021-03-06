#!/bin/bash
set -e
realpath() {
    [[ $1 = /* ]] && echo "$1" || echo "$PWD/${1#./}"
}
DIR=$(dirname "$(realpath "$0")")
source $DIR'/util.sh'
cd $TIDB_GIT
make_bin_info

tar -czvf $gzFile bin/*
mkdir -p $BIN
mv "$TIDB_GIT/$gzFile" "$BIN$gzFile"

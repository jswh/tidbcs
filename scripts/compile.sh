#!/bin/bash
set -e
realpath() {
    [[ $1 = /* ]] && echo "$1" || echo "$PWD/${1#./}"
}
DIR=$(dirname "$(realpath "$0")")
source $DIR'/util.sh'
cd $TIDB_GIT
make clean
make

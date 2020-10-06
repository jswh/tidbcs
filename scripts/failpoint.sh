#!/bin/bash
set -e
realpath() {
    [[ $1 = /* ]] && echo "$1" || echo "$PWD/${1#./}"
}
DIR=$(dirname "$(realpath "$0")")
source $DIR'/util.sh'
cd $TIDB_GIT
if [ -f tools/bin/failpoint-ctl ]
then
    find $TIDB_GIT -type d | xargs tools/bin/failpoint-ctl $1
fi


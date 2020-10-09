#!/bin/bash
set -e
realpath() {
    [[ $1 = /* ]] && echo "$1" || echo "$PWD/${1#./}"
}
DIR=$(dirname "$(realpath "$0")")
source $DIR'/util.sh'
CHECKOUT_TARGET=$1
update_tidb_code() {
    echo $TIDB_GIT
    if [ -d $TIDB_GIT"/.git" ]
    then
        cd $TIDB_GIT
        git fetch --all --tags
        cd $WORKSPACE
    else
        echo "workspace not empty"
        exit 1
    fi
}

init_tidb_code() {
    mkdir -p $TIDB_GIT
    cd $TIDB_GIT
    git clone $TIDB_SOURCE $TIDB_GIT
    cd $WORKSPACE
}


if [ -d $TIDB_GIT ]
then
    info "update tidb codebase"
    update_tidb_code
else
    info "init tidb codebase"
    init_tidb_code
    update_tidb_code
fi
cd $TIDB_GIT
make clean
git add .
git reset --hard
if [ -f owner/new_session:12379 ]
then
    rm owner/new_session:12379
fi

git checkout $CHECKOUT_TARGET
make_bin_info
if [ -f "$BIN$gzFile" ]
then
    echo 'alreay complile: '$gzFile
    exit 1
fi

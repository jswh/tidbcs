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
git reset --hard
git checkout $CHECKOUT_TARGET


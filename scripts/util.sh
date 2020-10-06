#!/bin/bash
WORKSPACE='/home/jswh/Codes/tidbcs/workspace/'
TIDB_GIT=$WORKSPACE"tidb"
TIDB_SOURCE="https://github.com/pingcap/tidb.git"
#get into worksapce before all operations
mkdir -p $WORKSPACE
info() {
    echo "[info] "$1
}
CGO_ENABLED=1
GO111MODULE=on

make_bin_info() {
    cd $TIDB_GIT
    version=$(git describe --exact-match --all)
    commitHash=$(git log -n1 --pretty='%h')
    if [[ $version == fatal* ]]
    then
        version='commit'
        commitHash=$(git log -n1 --pretty='%H')
    fi
    fullVersion=$version"-"$commitHash
    fullVersion=${fullVersion//'/'/'-'}
    gzFile=$fullVersion'.tar.gz'
    BIN=$WORKSPACE'/../binaries/'
}

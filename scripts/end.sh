#!/bin/bash
set -e
realpath() {
    [[ $1 = /* ]] && echo "$1" || echo "$PWD/${1#./}"
}
DIR=$(dirname "$(realpath "$0")")
source $DIR'/util.sh'
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
tar -czvf $gzFile bin/*
cd $WORKSPACE
BIN=$WORKSPACE'/../binaries/'
mkdir -p $BIN
mv "$TIDB_GIT/$gzFile" "$BIN$gzFile"

#!/bin/bash
realpath() {
    [[ $1 = /* ]] && echo "$1" || echo "$PWD/${1#./}"
}
DIR=$(dirname "$(realpath "$0")")
source $DIR'/util.sh'
cd $TIDB_GIT
#make test
if [[ $1 == '' ]]
then
    make gotest
else
    LOG_DIR='/tmp/tidbtest/'$1
    LOG=$LOG_DIR'/output.log'
    mkdir -p $LOG_DIR
    go test -p 8 -ldflags '-X "github.com/pingcap/tidb/config.checkBeforeDropLDFlag=1"' -cover $1 > $LOG
    TEST_STATE=$?
    tail $LOG
    exit $TEST_STATE
fi

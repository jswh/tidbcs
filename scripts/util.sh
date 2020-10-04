
#!/bin/bash
WORKSPACE='/home/jswh/Codes/tidbcs/workspace/'
TIDB_GIT=$WORKSPACE"tidb"
TIDB_SOURCE="https://github.com/pingcap/tidb.git"
#get into worksapce before all operations
mkdir -p $WORKSPACE
cd $WORKSPACE
info() {
    echo "[info] "$1
}

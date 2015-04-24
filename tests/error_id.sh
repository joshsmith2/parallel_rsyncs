#!/bin/bash

RSYNC_FLAGS="-n -r --stats"
RSYNC_BINARY="/opt/local/bin/rsync"
SOURCES=( folder/source\ 1 folder/source\ 2 )


perform_rsync() {
    log_path=$( basename "${1}" )
    "${RSYNC_BINARY}" ${RSYNC_FLAGS} /tmp/source/"${1}" /tmp/dest/ --log-file=/tmp/log/"${log_path}"
}

parallelise() {
    # Export functions and variables needed for perform_rsync
    export -f perform_rsync
    export RSYNC_FLAGS
    export RSYNC_BINARY
    parallel perform_rsync {} ::: "${SOURCES[@]}"
}

parallelise
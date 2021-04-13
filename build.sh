#!/bin/bash

#----------------------------------------------------------------------------------------------
#
#      MAIN
#
#----------------------------------------------------------------------------------------------

# declarations of MUST HAVE globals
PROGRAM_DIR="$(dirname "$(readlink -f "${BASH_SOURCE[0]}")")"
PROGRAM_NAME="$(basename "${BASH_SOURCE[0]}")"
LOGFILE="$(pwd)/${PROGRAM_NAME}.log"

declare -r LIB_NAME='build'
declare -A OPTS=( [cmd]='build.all' )
declare -a ARGS=()

# load our libraries
declare -r loader="${PROGRAM_DIR}/bashlib/appenv.bashlib"
if [ ! -e "$loader" ]; then
    echo 'Unable to load libraries' >&2
    exit 1
fi
source "$loader"
appenv.initialize "$@"
build.checkSetup

# our main script
declare -i status=0
{

    if [ "${#ARGS[*]}" -gt 0 ]; then
        "${OPTS['cmd']}" ${OPTS['oper']:-} "${ARGS[@]:-}" && status=$? || status=$?
    else
        "${OPTS['cmd']}" ${OPTS['oper']:-} && status=$? || status=$?
    fi
    [ -d "$logDir" ] && [ $(ls -1A "$logDir" | wc -l) -gt 0 ] || rmdir "$logDir"
    exit $status 

} 2>&1 | tee "$LOGFILE"

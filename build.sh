#!/bin/bash

#----------------------------------------------------------------------------------------------
#
#      MAIN
#
#----------------------------------------------------------------------------------------------

# declarations of MUST HAVE globals
declare -r PROGRAM_DIR="$(dirname "$(readlink -f "${BASH_SOURCE[0]}")")"
declare -r PROGRAM_NAME="$(basename "${BASH_SOURCE[0]}")"
declare -r LOGFILE="$(pwd)/${PROGRAM_NAME}.log"
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

# our main script
declare -i status=0
{
    "${OPTS['cmd']}" "${ARGS[@]}" && status=$? || status=$?  
#    eval echo 'build.all "${args[@]:1}"'
#    (build.all "${args[@]:2}") && status=$? || status=$?

    [ -d "$logDir" ] && [ $(ls -1A "$logDir" | wc -l) -gt 0 ] || rmdir "$logDir"
} 2>&1 | tee "$LOGFILE"

exit $status

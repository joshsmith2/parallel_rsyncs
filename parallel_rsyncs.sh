#!/usr/bin/env bash

# Requirements:
#
# ESSENTIAL:
# - Copy to destination, with full logs on errors etc
# - --ignore-existing, regular transfer or --delete options
# - Move or copy options
# - Ability to specify a binary
# - Ability to specify how many threads to run
#
# NICE BUT NOT STRICTLY NECESSARY:
# - Ability to specify a file containing paths to move



# Initialise command line arguments
# Defaults for switches:
while getopts "hs:d:l:p:b:cvmx" opt; do
    case $opt in
        s)
            #source: str, path - the source directory to copy
            source="$OPTARG"
            ;;
        d)
            #dest: str, path - the destination directory
            DEST="$OPTARG"
            ;;
        l)
            #log_file: str, path - path to the log file for this copy.
            LOG_PATH="$OPTARG"
            ;;
        p)
            PARALLEL_SYNCS=$OPTARG
            ;;
        b)
            alternative_rsync_binary=$OPTARG
            ;;
        c)
            create_dest=true
            ;;
        v)
            verbose=true
            ;;
        m)
            move_mode=true
            ;;
        x)
            copy_extended_attributes=true
            ;;
        h)

            # To be put back into here
            #-m : move_mode : bool : default false
            #    Delete files from source after copy. Off by default.


            echo """
            Sync files from source to dir using multiple instances of rsync.

            The original version of this script was developed by Stephen Buckley in Late July
            and early August 2013, and has since been developed by Josh
            Smith into the form you have before you today.

            It was written in response to torrents of water flooding through
            the ceiling of one of our machine rooms, and the subsequent
            discovery of the poor condition of the fileservers' disk directories.

            Hopefully it can help you copy lots of data elsewhere at speed too.


            -s = source : str - path
                The source directory to copy.

            -d = dest : str - path
                The destination directory

            -l = logs: str - path
                A directory in which to create logs for this move

            -p = parallel_rsyncs : int
                The number of rsync instances to run in parallel when moving these files.
                Default: 20

            -b = alternative_rsync_binary : str - path
                Full path to an alternative rsync binary to use for the
                transfer. Otherwise, use the system default.

            -c : create_dest : bool : default false
                If true, create destination directory (and any necessary
                intermediates) if it does not exist.

            -v : bool : default false
                Verbose - if true, print info to stdout as opposed to only errors.

            -x : copy_extended_attributes : bool : default false
                Copy extended attributes.

            -h : bool
                Help - Print this help and exit.
                                                                                                                                                          for Gruffyydd"""
            exit 0
            ;;
    esac
done

set_up_default_arguments() {
    if [[ ${alternative_rsync_binary} ]]; then
        rsync_app=${alternative_rsync_binary}
    else
        rsync_app=`which rsync`
    fi

    if [[ ! $parallel_rsyncs ]]; then
        parallel_rsyncs=20
    fi
}

# Check that the destination directory exists - create it if not
check_dest() {
    if [[ ! -e ${DEST} ]]; then
        if [[ $create_dest ]]; then
            echo "Destination does not exist. Creating ${DEST}"
            mkdir -vp -m 777 ${DEST}
        else
            echo "Destination ${DEST} does not exist. Run with -c flag if you'd like to create it."
            exit 1
        fi
    fi
}

check_source() {
    if [[ ! ${source} ]]; then
        echo "Please specify a source with the '-s' flag."
        exit 1
    else
        if [[ ! -e ${source} ]]; then
            echo "Source ${source} does not exist. Nothing to do."
            exit 1
        fi
    fi
}

construct_argument() {
    if [[ $move_mode ]]; then
        copy_or_move_command=" --remove-source-files "
    fi
    if [[ ${copy_extended_attributes} ]]; then
        if [[ "$rsync_version" -eq "2" ]]; then
            extended_attribute_flag="E"
        elif [[ "$rsync_version" -eq "3" ]]; then
            extended_attribute_flag="X"
        fi
    fi
    #RSYNC_OPTIONS="-WrltD${extended_attribute_flag}$copy_or_move_command --safe-links --stats"
    RSYNC_OPTIONS="-WrltD${extended_attribute_flag}$copy_or_move_command --stats --no-links"
}

run_rsync_with_defined_source() {
    source_path="${1}"
    log_filename=$(basename "${source_path}")
    "${RSYNC_BINARY}" ${RSYNC_OPTIONS} "${source_path}" "${DEST}" --log-file "${LOG_PATH}/${log_filename}.log"
}

get_rsync_version() {
    if [[ ${alternative_rsync_binary} ]]; then
        RSYNC_BINARY=${alternative_rsync_binary}
    else
        RSYNC_BINARY=$(which rsync)
    fi
    rsync_version=$(${RSYNC_BINARY} --version | grep version | awk '{print $3}' | cut -d '.' -f 1)
}

run_parallel_arguments() {

    #Read source directory contents into an array
    source_arr=("${source}"/*)

    # Export functions needed by defined_source, since parallel runs in a different shell
    export -f run_rsync_with_defined_source
    export RSYNC_BINARY
    export RSYNC_OPTIONS
    export DEST
    export LOG_PATH
    export PARALLEL_SYNCS

    # Pass array to parallel
    parallel -v -u -j 20 run_rsync_with_defined_source "{}" 1>> /dev/null 2> ${LOG_PATH}/rsync_errors.log ::: "${source_arr[@]}"
}

# MAIN
check_source
check_dest
get_rsync_version
construct_argument

echo "You are using rsync version $rsync_version"
echo "Command to be run: ${RSYNC_BINARY} ${RSYNC_OPTIONS}"

run_parallel_arguments




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



#Initialise command line arguments
# Defaults for switches:
while getopts "hs:d:l:p:cvm" opt; do
    case $opt in
        s)
            #source: str, path - the source directory to copy
            source=$OPTARG
            ;;
        d)
            #dest: str, path - the destination directory
            dest=$OPTARG
            ;;
        l)
            #log_file: str, path - path to the log file for this copy.
            log_path=$OPTARG
            ;;
        p)
            no_of_parallel_syncs=$OPTARG
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
        h)

             echo """
             Sync files from source to dir using multiple instances of rsync.

             The original version of this script was developed by Stephen Buckley in Late July
             and early August 2013, and has since been developed by Josh
             Smith into the form you have before you today.

             It was written in response to torrents of water flooding through
             the ceiling of one of our machine rooms, and the subsequent
             discovery of the poor condition of the fileservers' disk directories.

             Hopefully it can help you copy lots of data elsewhere at speed too.


             -s=source : str - path
                The source directory to copy.

             -d=dest : str - path
                The destibnation directory

             -l=logs: str - path
                A directory in which to create logs for this move

             -p=parallel_rsyncs: int.
                The number of rsync instances to run in parallel when moving these files.
                Default: 20

             -c : bool : default false
                If true, create destination directory (and any necessary
                intermediates) if it does not exist.

             -v : bool
                Verbose - if true, print info to stdout as opposed to only errors.

             -m move_mode: bool
                Delete files from source after copy.

             -h : bool
                Help - Print this help and exit.
                                                                                                                                                           for Gruffyydd"""
             exit 0
             ;;
    esac
done

# Check that the destination directory exists - create it if not
check_dest() {
    if [[ ! -e ${dest} ]]; then
        if [[ $create_dest ]]; then
            echo "Destination does not exist. Creating ${dest}"
            mkdir -vp -m 777 ${dest}
        else
            echo "Destination does not exist. Run with -c flag if you'd like to create it."
        fi
    fi
}

check_dest


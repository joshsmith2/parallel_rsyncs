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
while getopts "hs:d:l:p:vm" opt; do
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
        v)
            verbose=true
            ;;
        c)
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

             -p=parralel_rsyncs: int.
                The number of rsync instances to run in parallel when moving these files.
                Default: 20

             -m move_mode: bool
                Delete files from source after copy.

             -v : bool
                Verbose - if true, print info to stdout as opposed to only errors.

             -h : bool
                Help - Print this help and exit.
                                                                                                                                                           for Gruffyydd"""
             exit 0
             ;;
    esac
done
#!/usr/bin/env python
#
# Parses inode-list given in output from e2undel and extracts all inodes
# using debugfs. Gives them a name with their number and type

from sys import argv,exit
from os import system
import re

if __name__ == "__main__":
    if(len(argv) < 4):
        print "Usage: " + argv[0] + " inode-list device destination"
        exit(0)
    else:
        #14     8397  Oct 13 19:45 2007 * application/x-gzip
        regexp = re.compile("\s+(\d+)\s+\d+\s+.+\s\d+\s\d+:\d+\s\d+\s.\s(.*)")

        inodes = {}
        f = open(argv[1])
        for line in f: 
            m = regexp.match(line)
            if m is not None:
                type = m.group(2).replace('/','---')
                type = type.replace(' ', '-')
                inodes[m.group(1)] = type
        f.close()
        print "Found " + str(len(inodes)) + " inodes to copy!"

        for inode in inodes.keys():
#            print str(inode) + ' : ' + inodes[inode]
            system('echo "dump <' + inode + '> ' + argv[3] + '/' + \
                    inodes[inode] + '---' + inode + '" | debugfs ' +\
                    argv[2])


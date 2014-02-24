#!/usr/bin/env python
#
# Parses inode-list given in output from e2undel and extracts all inodes
# using debugfs. Gives them a name with their number and type
#
# Copyright (C) 2007, Pascal Mainini <http://mainini.ch>
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program.  If not, see <http://www.gnu.org/licenses/>.


from sys import argv,exit
from os import system
import re

if __name__ == "__main__":
    if(len(argv) < 4):
        print "Usage: " + argv[0] + " inode-list device destination"
        exit(0)
    else:
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


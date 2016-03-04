#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
# Some small functions for playing around with cyclic groups and other crypto stuff.
# DON'T USE FOR ANY SERIOUS CRYPTOGRAPHIC PURPOSES!
#
# Copyright (C) 2016, Michael Bolli <http://bolli.us>
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

from groupthy.numbthy import *
from random import randint

def diffiehellman(p, g):
    print "Exercise 1: Diffie-Hellman key-exchange"
    print "---------------------------------------"
    a = randint(0,p-1)
    A = (g**a)%p
    b = randint(0,p-1)
    B = (g**b)%p
    kA = (B**a)%p
    kB = (A**b)%p

    print "Alice picks random a: " + str(a)
    print "Alice computes A: " + str(A)
    print "Alice sends A = " + str(A) + " to Bob"
    print "Bob picks random b: " + str(b)
    print "Bob computes B: " + str(B)
    print "Bob sends B = " + str(B) + " to Alice"
    print "Alice computes k = " + str(kA)
    print "Bob computes k = " + str(kB)
    print "\n"

diffiehellman(11, 2)

def breakdiffiehellman(p, g, A, B):
    print "Exercise 2: Brute-force attempt to break Diffie-Hellman"
    print "-------------------------------------------------------"
    print "p: " + str(p) + " g: " + str(g) + " A: " + str(A) + " B: " + str(B)
    for num in range(0,p-1):
        if (g**num)%p == B:
            key = str((A**num)%p)
            print "FOUND! " + str(g) + "^" + str(num) + "%" + str(p) + " = " + str(A) + " -- the key is " + key + "\n"
            return
        else:
            print "NOPE: " + str(g) + "^" + str(num) + "%" + str(p) + " != " + str(A)
    print "Brute-force attempt failed."

breakdiffiehellman(11, 6, 7, 5)

def primitiveroots(p, maxX, maxY):
    print "Exercise 3: Find primitive roots in output"
    print "------------------------------------------"

    for x in range(0,maxX+1):
        if(x != 0):
            print str(x),
        print "\t⧫",

        digits = []
        for y in range(0,maxY+1):
            if(x == 0):
                print str(y),
            else:
                out = (x**y)%p
                digits.append(out)
                print out,

            # EOL
            if(y == maxY):
                if(set(digits) == set(range(1,maxX+1))):
                    print " ← primitive root!",
                print ""
            else: print "\t|",

primitiveroots(11,10,9)

def maninthemiddle(pk):
    print "Exercise 4: MITM-Attack if pk is transmitted over insecure channel"
    print "------------------------------------------------------------------"
    print "NOPE"

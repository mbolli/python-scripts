#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
# entropw.py
#
# A demonstrator to show entropy in passwords.
# THIS SHALL NOT BE USED AS A PASSWORD GENERATOR, IT SERVES ONLY DEMONSTRATIVE
# PURPOSES!
#
# Copyright (C) 2015, Pascal Mainini <http://mainini.ch>
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

from __future__ import print_function
import math
import sys
import argparse
from random import SystemRandom

#################### Initialisation ####################

# Default alphabet for passwords, numbers and letters in lower-/uppercase
NUMS_LETTERS = '0123456789ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz'

parser = argparse.ArgumentParser(description='Generate a random password based on required entropy and alphabet.')
parser.add_argument('-s','--strength', default=128, type=int, help='Desired strength of the password in bits of entropy')
parser.add_argument('-a','--alphabet', default=NUMS_LETTERS, help='Alphabet with characters allowed in the password')
args = parser.parse_args()

strength=args.strength
alphabet=args.alphabet
entropy = math.log(len(alphabet), 2)            # log2(possible characters)
pwlen = int(math.ceil(strength/entropy))        # required length, rounded up

pw = ''
for i in range(0, pwlen):
    # We blatantly assume that SystemRandom is cryptographically secure...
    # In Linux systems, /dev/urandom is used.
    pw += alphabet[SystemRandom().randrange(len(alphabet))]

print('Desired strength:\t%d' % strength)
print('Alphabet:\t\t"%s" (len: %d)' % (alphabet, len(alphabet)))
print('Entropy:\t\t%.3f' % entropy)
print('Password length:\t%d' % pwlen)
print('Password: %s' % pw)

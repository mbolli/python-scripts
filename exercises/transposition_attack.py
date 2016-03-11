#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
# Some small exercises for playing around with crypto stuff.
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

import collections

# Breaking transposition ciphers with chosen plaintext attack
def break_transposition():
	cleartext_a = "abcdefghijklmnopqrstuvwxyz"
	cyphertext_a = "cadbehfigjmknlorpsqtwuxvyz"
	replace = collections.defaultdict(str)
	diff = collections.defaultdict(int)
	modulo = 0

	# save cleartext/cyphertext allocation
	for i, l in enumerate(cleartext_a):
		replace[i] = cyphertext_a.index(l)

	# try to find repeating blocks while saving difference
	for i, l in enumerate(replace):
		print replace[i]-l,
		diff[i] = replace[i]-l
		if diff[0] == replace[i]-l: # found loop/block length?
			if modulo != 0: # re-test modulo validity
				if i%modulo == 0:
					print "ok! modulo candidate verified: " + str(modulo),
				else:
					modulo = i
					print "not ok! new modulo candidate: " + str(i)
			else:
				modulo = i
			print " -- " + str(i) + "%" + str(modulo) + "\n"

	# output needed allocation
	print "\n\nAllocation: "
	for i in range(0,modulo):
		print diff[i],

	# decode cyphertext
	print "\n\n" + " ".join(cyphertext_a)
	for i, l in enumerate(cyphertext_a):
		id = i+diff[(i%modulo)]
		if id < len(cyphertext_a):
			print cyphertext_a[id],
		else:
			print cyphertext_a[i],

break_transposition()
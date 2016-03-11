#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
# Some small exercises for playing around with rypto stuff.
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
import collections
import operator

replacements = collections.defaultdict(int)
replacements["\n"] = ""
frequencies = collections.defaultdict(int)
text = ""

def analyze_frequency(textfile):
	# english language character frequencies according to wikipedia:
	# a:8.167%, b:1.492%, c:2.782%, d:4.253%, e:12.702%, f:2.228%, g:2.015%, h:6.094%, i:6.966%, j:0.153%, k:0.772%, l:4.025%, m:2.406%, n:6.749%, o:7.507%, p:1.929%, q:0.095%, r:5.987%, s:6.327%, t:9.056%, u:2.758%, v:0.978%, w:2.361%, x:0.150%, y:1.974%, z:0.074%,

	# only execute the first time
	global replacements, frequencies, text
	if len(text) == 0:
		with open(textfile) as f_in:
			text = f_in.read()
			for line in text:
				for char in line:
					if char.isalpha():
						frequencies[char.lower()] += 1
		frequencies = [(count, char) for char, count in frequencies.iteritems()]
		frequencies.sort(key=operator.itemgetter(0), reverse=True)

	# print text (replacements taken into account)
	print "".join([replacements.get(c, c) for c in text.lower()]), "\n"
	print frequencies, "\n"
	print replacements, "\n"

	# take user input replacements
	replace = raw_input("Replace character: ")
	rvalues = replace.split("=")
	print rvalues, "\n"
	replacements[rvalues[0]] = rvalues[1]

	# recursively work through the text
	analyze_frequency(textfile)

#analyze_frequency("crypto-1.txt")

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
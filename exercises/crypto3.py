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

from groupthy.numbthy import *
from groupthy.groupthy import *
from math import log, floor
from decimal import Decimal
from random import randint

small_primes = [2, 3, 5, 7, 11, 13, 17, 19, 23, 29, 31] # etc.

def probably_prime(n, k):
	"""Return True if n passes k rounds of the Miller-Rabin primality test (and is probably prime). Return False if n is proved to be composite."""
	if n<2 : return False

	# trivial cases
	for p in small_primes:
		if n < p * p: return True
		if n % p == 0: return False

	r, s = 0, n-1

	while s % 2 == 0:
		r += 1
		s //= 2

	for i in range(k):
		a = randint(2, n-1)
		x = pow(a, s, n)

		if x == 1 or x == (n-1):
			print "nope"
			continue
		for j in range(r-1):
			x = pow(x, 2, n)
			if x == (n-1):
				break
		else:
			return False
	return True

def findprime(max):
	"""Miller-Rabin Primality Test: Write an algorithm that finds for an odd input n > 2 a pair (r; u) of positive
integers such that u is odd and n - 1 = (2**r)*u. Use it to generate the n smallest prime numbers."""
	for i in range(2, max):
		if probably_prime(i, 10):
			print i, "is prime"

findprime(222)

"""Algorithm and Extended Algorithm of Euclid: Compute Euclid(48; 174), ExtEuclid(48; 174), and MultInv(48; 127)."""
def euclid(a,b):
	r = b%a
	if r == 0:
		return a
	else:
		return euclid(r,a)

print "Euclid:", euclid(48,174)

def extEuclid(a,b):
	r = b%a
	q = b/a
	if r == 0:
		return a, 1, 0
	else:
		(d, X, Y) = extEuclid(r,a)
		print d, X, Y
		return d, Y-X*q, X

print "extEuclid:", extEuclid(48, 174)

def multInv(a, n):
	d,X,Y = extEuclid(a,n)
	return X

print "multInv:", multInv(48,127)

def modExp(x, y, n):
	m = 1
	while y != 0:
		if y%2 == 0:
			x = x*x % n
			y /= 2
		else:
			m = m*x % n
			y -= 1
	return m
print "modPow:", power_mod(3, 37, 13)
print "modExp:", modExp(3, 37, 13)
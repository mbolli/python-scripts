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
from exercises.pubkey1 import primitiveroots
from math import log, floor
from decimal import Decimal

def estimateprimes(min, max):
	minprimes = Decimal(min)/Decimal(log(min)-1)
	maxprimes = Decimal(max)/Decimal(log(max)-1)
	estimated = Decimal(maxprimes-minprimes)
	print "\nEstimated about " + str(estimated) + " primes between " + str(min) + " and " + str(max) + "."
	return estimated

def chanceofprime(p):
	print "\nChance of prime " + str(p) + " is " + str(1/log(p,10)) + "."

def findprimes(min, max):
	estimated = estimateprimes(min, max)
	count = 0
	for i in range(min, max):
		if is_prime(i):
			count += 1
	print str(count) + " primes found."

findprimes(1000,10000)
estimateprimes(2**1024, (2**1025)-1)
chanceofprime(2**1024)

def primefactors(p):
	print str(p) + " has the following prime factors:", prime_divisors(p)

primefactors(41140)

def eulertotient(min, max):
	for i in range(min, max):
		print i, ": euler totient =", euler_phi(i)

eulertotient(11, 20)
eulertotient(41140, 41141)

def eulerstheorem(n):
	for a in range(0, 100):
		if gcd(a, n) == 1:
			print a, "**", euler_phi(n), "mod", n, "=", a**euler_phi(n) % n

eulerstheorem(9)
eulerstheorem(10)

primitiveroots(7, 6, 5)
primitiveroots(8, 7, 6)
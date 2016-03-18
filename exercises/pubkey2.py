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

# 1024 bit numbers have about 1/1000 prime numbers
# 2048 bit numbers have about 1/2000 prime numbersr
def estimateprimes(min, max):
	minprimes = Decimal(min)/Decimal(log(min)-1)
	maxprimes = Decimal(max)/Decimal(log(max)-1)
	estimated = Decimal(maxprimes-minprimes)
	print "\nEstimated about " + str(estimated) + " primes between " + str(min) + " and " + str(max) + "."
	return estimated

def chanceofprime(p):
	print "\nChance of prime " + str(p) + " is " + str(1/log(p)) + "."

def findprimes(min, max):
	estimated = estimateprimes(min, max)
	count = 0
	for i in range(min, max):
		if is_prime(i):
			count += 1
	print count, " primes found."

# Exercise 1: Estimate the number of primes in the range between 1000 and 10000.
findprimes(1000,10000)

# Exercise 1 cont.: Estimate the number of 1024-bit primes (leftmost bit set to 1) and the probability that a random 1024-bit integer is prime.
estimateprimes(2**1023, (2**1024)-1)
chanceofprime(2**1023)

def primefactors(p):
	print str(p) + " has the following prime factors:", prime_divisors(p)

# Exercise 2: Compute the prime factors of 41140.
primefactors(41140)

def eulertotient(min, max):
	for i in range(min, max):
		print i, ": euler totient =", euler_phi(i)

def eulertotient_alt(num):
	for i in prime_divisors(num):
		num *= 1-i**-1
		print num

# Exercise 3: Compute corresponding values of Euler's totient function (n) for n = 11; 12; ... ; 20.
eulertotient(11, 20)

# Exercise 3 cont.: Compute ϕ(41140).
eulertotient(41140, 41141)
eulertotient_alt(41140)

# generalization of fermat's theorem: a^(phi(n)) == 1 mod n
def eulerstheorem(n):
	for a in range(0, n):
		if gcd(a, n) == 1:
			print a, "**", euler_phi(n), "mod", n, "=", a**euler_phi(n) % n

# Exercise 4: Check that Euler's theorem holds for n = 9 and n = 10.
eulerstheorem(9)
eulerstheorem(10)

# Exercise 5: Determine the primitive roots modulo n for n = 7 and n = 8.
primitiveroots(7, 6, 5)
primitiveroots(8, 7, 6)
#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
# Some small functions for playing around with cyclic groups and other crypto stuff.
# DON'T USE FOR ANY SERIOUS CRYPTOGRAPHIC PURPOSES!
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

import numbthy

########## Groups ##########

def generate(g, n):
    """Generate a (sub-)group using g as generator in modulus n"""
    result = []
    for i in range(1,n):
        val = g ** i % n
        if val != None and val > 0:
            result.append(val)
        if val < 2:
            return result

def generateFull(n):
    """Generates the full group Z*_n using each element from 1...n as a generator for generate(g,n)"""
    result = []
    for i in range(1,n):
        current = generate(i,n)
        if current != None:
            result.append(current)
    return result

def groupOp(pair1, pair2, n1, n2):
    """Apply group operation to two pairs:
       (g1,h1) x (g2, h2) 
       G beeing multiplicative, H additive, thus
       (g1*g2 , h1+h2)"""
    return ((pair1[0] * pair2[0]) % n1, (pair1[1] + pair2[1]) % n2)

def groupGenerate(generatorpair, n1, n2):
    """Generates a (sub-)group of G x H with G beeing multiplicative and H additive.
       The modulus of G is n1, of H it's n2."""
    result = [(1,0)]
    pair = generatorpair
    while True:
        pair = groupOp(pair, generatorpair, n1, n2)
        if pair[0] == 1 and pair [1] == 0:
            return result
        else:
            result.append(pair)

def groupGenerateFull(n1, n2):
    """Generates the full group G x H with the given moduli n1 for G and n2 for H"""
    result = []
    for i in range(1,n1):
        for j in range(0,n2):
            result.append(groupGenerate((i,j),n1,n2))
    return result

def safePrimeGenerate(n):
    """Assuming that n is a safe-prime (q = (p-1)/2, q prime), this checks that indeed every value of 1 ... p-1 is a generator for Z_q"""
    q = int((n-1) / 2)
    print("\nq is %d" % q)

    print("\n<x²> as generator for Z_q:\n")
    for x in range(1,n):
        subgroup =  generate(x**2,n)
        print("%02d², len %02d:\t%s" % (x, len(subgroup), subgroup))

    print("\n<p-x²> as generator for Z_p:\n")
    for x in range(1,n):
        subgroup =  generate((n-x**2)%n,n)
        print("%02d (%02d-%02d²), len %02d:\t%s" % (n-x**2 % n, n, x, len(subgroup), subgroup))

def schnorrGenerate(p, k):
    """Calculate subgroups of Z*_p using Schnorr: p = kq + 1, p and q prime, Z*_p has a subgroup of order q"""
    print("\nq is %d" % int((p-1)/k))
    subgroup = []
    for x in range(2, p):
        g = x**k % p
        subgroup.append(g)
        if g == 1: break
    subgroup = set(subgroup)
    print("G_q, len %02d:\t%s\n" % (len(subgroup), subgroup))

def multiplicativeInverse(a, n):
    """Efficiently calculate the multiplicative inverse using extended GCD algorithm"""
    (d,X,Y) = numbthy.xgcd(a,n)
    if d != 1: return None
    else: return X % n

def multiplicativeInverseBrute(a, n):
    """Bruteforce the multiplicative inverse of a in group with modulus n"""
    for i in range(n):
       if (a*i) % n == 1:
           return i 
    return None

def allMultiplicativeInverse(n):
    """For all elements in the multiplicative group with modulus n, calculate the multiplicative inverse"""
    result = []
    for i in range(n):
        inverse = multiplicativeInverse(i, n)
        if inverse:
            result.append((i, inverse))
    return result

def root(a, e, n):
    """Efficiently find the modular root: find x where x^e = a mod n"""
    d = multiplicativeInverse(e, numbthy.eulerphi(n))
    return (a ** d) % n
    
def testLagrange(n):
    """Tests for each element x of Z*_n if x^phi(n) is 1"""
    order = numbthy.eulerphi(n)
    result = True
    for i in range(1,n):
        inverse = (i**order) % n
        if inverse != 1:
            print('Test failed for ' + str(i) + ': ' + str(inverse))
            result = False
    return result

def prettyPrint(group):
    """Print out nicely a group generated using generateAll"""
    i = 1
    for current in group:
        if current != None:
            print('%04d (%d):\t\t%s' % (i,len(current),current))
        else:
            print('%04d (0):\tNone' % i)
        i += 1


########## Pedersen commits ##########

def pedersenCommit(n,g,h,m,r):
    """Calculate a pedersen commit. Arguments:
       n    modulus (i.e. Z*_n)
       g    generator 1
       h    generator 2
       m    message
       r    random"""
    return g**m*h**r % n

def pedersenOpen(n,g,h,m,r,c):
    """Open a pedersen commit. Arguments:
       n    modulus (i.e. Z*_n)
       g    generator 1
       h    generator 2
       m    message
       r    random
       c    commit generated by pedersenCommit() to verify"""
    if c == g**m*h**r % n:
        return True
    else:
        return False

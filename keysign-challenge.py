#!/usr/bin/env python
# -*- coding: utf-8 -*-

#
# Future improvments:
# - make targets specifiable via cmd-line
# - directly send mail, possible template:
# 
#Hello!
#
#we have recently (or not so) personally met and verified our keys
#for keysigning. In order to sign your key, I need a proof that
#the email-address on each uid of your key is valid and can be read
#by you. Please decrypt the attached challenge(s) and send me
#back the contained challenge-string in a signed mail.
#I will not publish the signed key(s) but only send them back to you.
#
#Thanks and kind regards!
#
#Pascal
#

import gpgme
import subprocess
from StringIO import StringIO

my_key = 'E284ED60'
targets = ['DEADBEEF']
values = {}

def hashfunc():
    return subprocess.Popen(["/usr/bin/apg", "-a0", "-m24", "-x24", "-n1", "-MSNCL"], stdout=subprocess.PIPE).communicate()[0][:-1]

ctx = gpgme.Context()
ctx.armor = True
for id in targets:
    k = ctx.get_key(id)
    v = []
    for uid in k.uids:
        if uid.revoked: continue

        if len(uid.email) == 0:
            v.append([uid.uid])
            continue
        else:
            v.append([uid.uid, uid.email, hashfunc()])
    values[id] = v

f = open('hashes.out', 'w')
for key in values.keys():
    f.write(key + '\n')
    for entry in values[key]:
        if len(entry) == 3:
            plain =  StringIO('\n\nChallenge:\n' + entry[2] + '\n\n')
            cipher = open(key + '-' + entry[1] + '.asc', 'w')
            ctx.encrypt([ctx.get_key(my_key), ctx.get_key(key)], gpgme.ENCRYPT_ALWAYS_TRUST, plain, cipher)
            cipher.close()
            f.write('\t' + entry[2] + '\t' + entry[1] + '\t(' + entry[0] + ')\n')
        else:
            f.write('\t-                       \t-                        \t(' + entry[0] + ')\n')
    f.write('\n')
f.close()

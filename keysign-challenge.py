#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
# A helper for creating per-recipient-UID encrypted challenges for keysigning.
#
# Copyright (C) 2010,2013, Pascal Mainini <http://mainini.ch>
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
#
# Future improvments:
# - make targets specifiable via cmd-line
# - directly send mail, possible template

import gpgme
import subprocess
from StringIO import StringIO

my_key = 'A9A71917D900A399'
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

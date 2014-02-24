#!/usr/bin/env python
#
# aspsms.py - a Python module for sending SMS over aspsms.com
#
# Copyright (C) 2007, Pascal Mainini <http://mainini.ch>
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

import urllib
from xml.dom.minidom import parseString

SERVICE='http://xml1.aspsms.com:5061/xmlsvr.asp'

def sendtextsms(userkey, password, originator, destination, data):
    xml = """<?xml version="1.0" encoding="ISO-8859-1"?>
      <aspsms>
        <Userkey>%s</Userkey>
        <Password>%s</Password>
        <Originator>%s</Originator>
        <Recipient>
          <PhoneNumber>%s</PhoneNumber><TransRefNumber/>
        </Recipient>
        <MessageData>%s</MessageData>
        <Action>SendTextSMS</Action>
      </aspsms>
    """ % (userkey, password, originator, destination, data)

    f = urllib.urlopen(SERVICE, xml)
    response = f.read()
    f.close()

    dom = parseString(response)
    code = int(dom.getElementsByTagName('ErrorCode')[0].childNodes[0].data)
    descr = dom.getElementsByTagName('ErrorDescription')[0].childNodes[0].data
    dom.unlink()

    return (code, descr)


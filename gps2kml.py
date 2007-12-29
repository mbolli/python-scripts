#!/usr/bin/env python

import re
from sys import argv

def parseMXMap(filename):
    """Parses data from gpstrans in mxmap-format"""

    regexp = re.compile("^\d (\d+\.\d+) (\d+\.\d+) (\d+\.\d+).*(\d+/\d+/\d+) (\d+:\d+:..)")
    return parse(filename, regexp)

def parse(filename, regexp):
    """Parses gps coordinates using the given regular expression.
    Returns a list containing lists, called groups. A new group is started 
    every time a blank line is detected in the data. A group contains tuples
    with the effective GPS-data as for values (lat., long., alt., date and time)."""

    data = []
    group = []
    file = open(filename, 'r')
    for line in file:
       match = regexp.match(line)
       if match is not None:
            group.append((match.group(1), match.group(2), match.group(3), match.group(4), match.group(5)))
       else:
            if line.isspace() and len(group) > 0:
                data.append(group)
                group = []
    file.close()
    return data

def optimize(data):
    for group in data:
        prevlong = 0.0
        prevlat = 0.0
        for entry in group:
            difflong = float(entry[0]) - prevlong
            difflat = float(entry[1]) - prevlat
#            print 'difflat: ' + str(difflat) + ' difflong: ' + str(difflong)
            if difflat > 0.0005 or difflong > 0.0005:
                if difflat < 0.1 or difflong < 0.1:
                    print str(entry[1] + '   ' + entry[0])
            prevlong = float(entry[0])
            prevlat = float(entry[1])

def generatePlacemarks(data, name):
    """Generates a list of strings, each containing a placemark representing 
    a group from the data"""

    count = 1
    placemarks = []
    for group in data:
        coordinates = ''
        for entry in group:
           coordinates = coordinates + entry[1] + ',' + entry[0] + ',' + entry[2] + ' ' 
        coordinates = coordinates[:-1]

        pm = '<Placemark>\n'
        pm += '<name>' + name + '-' + str(count) + '</name>\n'
        pm += '<visibility>1</visibility>\n'
        pm += '<LineString>\n'
        pm += '<tessellate>1</tessellate>\n'
        pm += '<altitudeMode>clampToGround</altitudeMode>\n'
        pm += '<coordinates>' + coordinates + '</coordinates>\n'
        pm += '</LineString>\n'
        pm += '</Placemark>\n\n'
        count += 1
        placemarks.append(pm)
    return placemarks

def generateKMLDocument(placemarks, name, datefromstring=None, datetostring=None):
    """Generates a KML-Document-element containing all the placemarks"""

    doc = '<?xml version="1.0" encoding="UTF-8"?>\n\n'
    doc += '<Document>\n'
    doc += '<description>Generated using gps2kml\n'
    doc +='See http://impressionet.ch for more information.\n'
    if datefromstring is not None and datetostring is not None:
        doc += 'GPS data captured between ' + datefromstring + ' and ' + \
                datetostring + '.'
    doc += '</description>\n\n'
    for placemark in  placemarks:
        doc += placemark
    return doc + '</Document>\n'


data = parseMXMap(argv[1])
pms = generatePlacemarks(data, 'test')

if len(data) > 1:
    datefrom = str(data[0][0][3]) + '/' + str(data[0][0][4])
    last = len(data) - 1
    dateto = str(data[last][len(data[last])-1][3]) + ' ' + str(data[last][len(data[last])-1][4])
    doc = generateKMLDocument(pms, 'test', datefrom, dateto)
else:    
    doc = generateKMLDocument(pms, 'test')

file = open('/tmp/test.kml','w')
file.write(doc)
file.close()


#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
# Workflow and Data structures
# ============================
# 
# Data from the GPS gets first parsed using the appropriate parsing method
# depending on the datatype selected (one of the parse*-methods from the 
# parse-section).
# All parse-methods return the same datastructure, so parsing additional 
# filetypes should be easy. Structure of data is as follows:
#
#   [                                   <--- enclosing list
#       [                               <--- data group
#           (coordinate-tuple)
#           (coordinate-tuple)
#           ...
#       ]
#       [                               <-- another data group
#       ]
#        ...
#   ]
#
# Multiple data groups are possible, at least one must be present.
# Data groups should represent some state from the data if possible,
# like the GPS-device out of satelite range or turned off.
#
# A coordinate-tuple looks as follows:
#
# (name,latitude,longitude,altitude,date,time)
#
# name, altitude, date and time can be replaced with None
#
# Data is then fed into one of the handling methods for generating either
# a KML-file or plotting the data with GNUPlot
#
# Multi-segment-patch for gpsman-format by Alexis Domjan - adomjan <at> horus <dot> ch
#

import re
from colorsys import hsv_to_rgb
from sys import argv
from optparse import OptionParser
from datetime import datetime

VERSION = '0.1'


##############################################################################
## Helpers
##############################################################################

def generateColors(count):
    """Generates an array with rgb-tuples depending on the options given by
    the user and the amount of groups."""

    colors=[]
    if options.bicolor:
        for n in range(0, count):
            if n % 2 == 0:
                colors.append((1,0,0))
            else:
                colors.append((0,0,1))
    elif options.rainbow:
        dist = 1.0/count
        i = 0
        while i <= count*dist:
            colors.append(hsv_to_rgb(i, 1, 1))
            i += dist            
    return colors

def calculateOverallTime(data):
    """Extracts start and endtime from the data and returns it as a string-tuple"""

    if data is None or len(data) is 0:
        return None
    if data[0] is None or len(data[0]) is 0:
        return None
    if data[0][0] is None or len(data[0][0]) is 0:
        return None
    if len(data[0][0]) < 6:
        return None
    if data[0][0][4] is None or data[0][0][5] is None:
        return None

    datefrom = str(data[0][0][4]) + ',' + str(data[0][0][5])
    last = len(data) - 1
    dateto = str(data[last][len(data[last])-1][4]) + ',' + str(data[last][len(data[last])-1][5])
    return (datefrom, dateto)

def optimize(data):
    """A testbed for trying out optimizations - DON'T USE."""
    for group in data:
        prevlong = 0.0
        prevlat = 0.0
        for entry in group:
            difflong = float(entry[0]) - prevlong
            difflat = float(entry[1]) - prevlat
#            print 'difflat: ' + str(difflat) + ' difflong: ' + str(difflong)
            if difflat > 0.00001 or difflong > 0.00001:
                #if difflat < 0.1 or difflong < 0.1:
                    print str(entry[1] + '   ' + entry[0])
            prevlong = float(entry[0])
            prevlat = float(entry[1])


##############################################################################
## Parsing methods
##############################################################################

def parseGpsTrans(filename):
    """Parses data in gpstrans-format. See data structure description on top
       of this file."""

    # Groups: date, time, altitude, latitude, longitude
    regexp = re.compile('^T\s+(\d+\/\d+\/\d+) (\d+:\d+:..)\s+([-|\d]+\.\d+)\s+m\s+([-|\d]+.\d+.\d+.\d+).*([-|\d]+.\d+.\d+.\d+).*')
    coordreg = re.compile('(\d+).(\d+).(\d+\.\d).*')
    data = []
    group = []
    last = None
    file = open(filename, 'r')
    for line in file:
        match = regexp.match(line)
        if match is not None:
            cmatch = coordreg.match(match.group(4))
            lat = float(cmatch.group(1))
            lat += (float(cmatch.group(2)) * 60 + float(cmatch.group(3)))/3600

            cmatch = coordreg.match(match.group(5))
            long = float(cmatch.group(1))
            long += (float(cmatch.group(2)) * 60 + float(cmatch.group(3)))/3600

            last = (None, str(lat), str(long), match.group(3), match.group(1),\
                match.group(2))
            group.append(last)
        else:
            if line.startswith('H') and len(group) > 0:
                data.append(group)
                group = []
                if options.join:
                    group.append(last)

    if len(group) > 0:
        data.append(group)

    file.close()
    return data

def parseMXMap(filename):
    """Parses data in mxmap-format. See data structure description on top
       of this file."""

    # Groups: latitude, longitude, x-speed, altitude, date, time
    regexp = re.compile("^\d ([-|\d]+\.\d+) ([-|\d]+\.\d+) ([-|\d]+\.\d+) ([-|\d]+) (\d+/\d+/\d+) (\d+:\d+:..)")
    data = []
    group = []
    last = None
    file = open(filename, 'r')
    for line in file:
        match = regexp.match(line)
        if match is not None:
            last = (None, match.group(1), match.group(2), match.group(4),\
                match.group(5), match.group(6))
            group.append(last)
        else:
            if line.isspace() and len(group) > 0:
                data.append(group)
                group = []
                if options.join:
                    group.append(last)

    if len(group) > 0:
        data.append(group)

    file.close()
    return data

def parseGpsman(filename):
    """Parses data in gpsman-format. See data structure description on top
       of this file."""

    # Groups: altitude, latitude, longitude, unixtime
    regexp = re.compile('^.*altitude="([-|\d]+)"\s+latitude="\s*([-|\d]+\.\d+)"\s+longitude="\s*([-|\d]+\.\d+)"\s+unixtime="(\d+)".*')
    newseg = re.compile('.*newsegment="yes"');

    data = []
    group = []
    last = None
    file = open(filename, 'r')
    for line in file:
        match = regexp.match(line)
        nmatch = newseg.match(line)

        if nmatch is not None:
            if len(group) > 0:
                data.append(group)
                group = []

        if match is not None:
            then = datetime.fromtimestamp(float(match.group(4)))
            thendate = then.strftime('%m/%d/%Y')
            thentime = then.strftime('%H:%M')
            last = (None, match.group(2), match.group(3), match.group(1),\
                thendate, thentime)
            group.append(last)

    if len(group) > 0:
        data.append(group)

    file.close()
    return data
    
def parseWaypoint(filename):
    """Parses data in gpstrans' waypoint-format. See data structure description on top
       of this file."""

    # Groups: name, altitude, latitude, longitude
    regexp = re.compile('^W\s+(.*)([-|\d+]\.\d+)\s+m\s+([-|\d]+.\d+.\d+.\d+)"\s+([-|\d]+.\d+.\d+.\d+).*')
    coordreg = re.compile('(\d+).(\d+).(\d+\.\d).*')
    data = []
    group = []
    last = None
    file = open(filename, 'r')
    for line in file:
        match = regexp.match(line)
        if match is not None:
            cmatch = coordreg.match(match.group(3))
            lat = float(cmatch.group(1))
            lat += (float(cmatch.group(2)) * 60 + float(cmatch.group(3)))/3600

            cmatch = coordreg.match(match.group(4))
            long = float(cmatch.group(1))
            long += (float(cmatch.group(2)) * 60 + float(cmatch.group(3)))/3600

            name = match.group(1)
            i = len(name)-1
            while i >= 0:
                if not name[i].isspace():
                    break
                else:
                    i -= 1
            name = name[:i+1]

            last = (name, str(lat), str(long), match.group(2),\
                None, None)
            group.append(last)
        else:
            if line.isspace() and len(group) > 0:
                data.append(group)
                group = []

    if len(group) > 0:
        data.append(group)

    file.close()
    return data


##############################################################################
## GNUplot
##############################################################################

def plot(data, outfile):
    """Plots data using gnuplot"""

    import Gnuplot

    plotdata = []
    for group in data:
        plotgroup = []
        for entry in group:
            plotgroup.append((float(entry[2]),float(entry[1])))
        plotdata.append(plotgroup)

    g = Gnuplot.Gnuplot()
    if options.data:
        g('set title')
        g('set xlabel')
        g('set ylabel')
        g('unset border')
        g('unset tics')
    else:
        g('set grid')
        times = calculateOverallTime(data)
        if times is not None:
            g('set title "GPS Data from ' + times[0] + ' to ' + times[1] + '"')
        else:
            g('set title "GPS Data"')
    g('set size square')
    g('set output \'' + outfile + '\'')
    if options.svg:
        g('set terminal svg size 800,600')
    else:
        if options.rainbow or options.bicolor:
            colors = generateColors(len(data))
            colorstring = ''
            for color in colors:
                colorstring += 'x%02x%02x%02x ' % (color[0]*255, color[1]*255, color[2]*255)
            g('set terminal png medium size 800,600 xffffff x000000 xa0a0a0 ' + colorstring)
        else:
            g('set terminal png medium size 800,600')

    plotitems = []
    if options.waypoint:
        style = "point"
    else:
        style = "lines"

    for group in plotdata:
        plotitems.append(Gnuplot.PlotItems.Data(group, with=style))
    g.plot(*plotitems)


##############################################################################
## KML-generating methods
##############################################################################

def generateStyles(name, count):
    """Generates styles according to color-options"""

    stylestring = ''
    if options.waypoint:
        stylestring += '<Style id="style_' + name + '">\n'
        stylestring += '<IconStyle>\n'
        stylestring += '<scale>1.1</scale>\n'
        stylestring += '<Icon><href>http://maps.google.com/mapfiles/kml/pushpin/ylw-pushpin.png</href></Icon>\n'
        stylestring += '<hotSpot x="20" y="2" xunits="pixels" yunits="pixels"/>\n'
        stylestring += '</IconStyle>\n'
        stylestring += '</Style>\n\n'
    else:
        if options.rainbow or options.bicolor:
            colors = generateColors(count)
            counter = 1
            for color in colors:
                colorstring = 'ff%02x%02x%02x' % (color[2]*255, color[1]*255, color[0]*255)
                stylestring += '<Style id="style_' + name + '_' + str(counter) + '">\n'
                stylestring += '<LineStyle><color>' + colorstring + '</color><width>2</width></LineStyle>\n'
                stylestring += '</Style>\n\n'
                counter += 1
        else:
            stylestring += '<Style id="style_' + name + '">\n'
            stylestring += '<LineStyle><color>ffff0000</color><width>2</width></LineStyle>\n'
            stylestring += '</Style>\n\n'

    return stylestring

def generatePlacemarks(data, name):
    """Generates a list of strings, each containing a placemark representing 
    a group from the data"""

    count = 1
    placemarks = []
    for group in data:
        coordinates = ''
        for entry in group:
           coordinates = coordinates + entry[2] + ',' + entry[1] + ',' + entry[3] + ' ' 
        coordinates = coordinates[:-1]
        timefrom = str(group[0][4]) + ',' + str(group[0][5])
        timeto = str(group[len(group)-1][4]) + ',' + str(group[len(group)-1][5])

        pm = '<Placemark>\n'
        pm += '<name>' + name + '-' + str(count) + '</name>\n'
        pm += '<visibility>1</visibility>\n'
        pm += '<description>GPS-Data from ' + timefrom + ' to ' + timeto + '.</description>\n'
        if options.rainbow or options.bicolor:
            pm += '<styleUrl>style_' + name + '_' + str(count) + '</styleUrl>\n'
        else:
            pm += '<styleUrl>style_' + name + '</styleUrl>\n'
        pm += '<LineString>\n'
        pm += '<tessellate>1</tessellate>\n'
        pm += '<altitudeMode>clampToGround</altitudeMode>\n'
        pm += '<coordinates>' + coordinates + '</coordinates>\n'
        pm += '</LineString>\n'
        pm += '</Placemark>\n\n'
        count += 1
        placemarks.append(pm)
    return placemarks

def generatePlacemarksWP(data, name):
    """Generates a list of strings, each containing a placemark for each waypoint"""

    placemarks = []
    for group in data:
        for entry in group:
            pm = '<Placemark>\n'
            pm += '<name>' + entry[0] + '</name>\n'
            pm += '<visibility>1</visibility>\n'
            pm += '<styleUrl>style_' + name + '</styleUrl>\n'
            pm += '<Point>\n'
            pm += '<tessellate>1</tessellate>\n'
            pm += '<altitudeMode>clampToGround</altitudeMode>\n'
            pm += '<coordinates>' + entry[2] + ',' + entry[1] + ',' + entry[3] + '</coordinates>\n'
            pm += '</Point>\n'
            pm += '</Placemark>\n\n'
            placemarks.append(pm)
    return placemarks

def generateKML(data, filename):
    """Generates a KML-File"""

    if filename.endswith('.kml'):
        name = filename[:-4]
    else:
        name = filename

    if options.waypoint:
        placemarks = generatePlacemarksWP(data, name)
    else:
        placemarks = generatePlacemarks(data, name)

    times = calculateOverallTime(data)

    doc = '<?xml version="1.0" encoding="UTF-8"?>\n\n'
    doc += '<Document>\n'
    doc += '<description>Generated using gps2kml\n'
    doc +='See http://impressionet.ch for more information.\n'
    if times is not None:
        doc += 'GPS data captured between ' + times[0] + ' and ' + \
                times[1] + '.'
    doc += '</description>\n\n'
    doc += generateStyles(name, len(data))
	
    for placemark in  placemarks:
        doc += placemark
    doc += '</Document>\n'

    file = open(filename,'w')
    file.write(doc)
    file.close()


##############################################################################
## MAIN
##############################################################################

if __name__ == "__main__":
    """Parses commandline arguments and dispatches them"""

    parser = OptionParser(usage='%prog [options] gpsdata outfile', version='%prog ' + VERSION)
    parser.add_option('-b', '--bicolor', help='only use two colors (red and blue).', action='store_true', default=False)
    parser.add_option('-d', '--data', help='for plot-mode (-p): only plot data, no grid, scales, etc.', action='store_true', default=False)
    parser.add_option('-g', '--gpsman', help='inputdata is in gpsman-format', action='store_true', default=False)
    parser.add_option('-j', '--join', help='join end of a group and beginning of the next.', action='store_true', default=False)
    parser.add_option('-m', '--mxmap', help='input data is in mxmap-format.', action='store_true', default=False)
    parser.add_option('-p', '--plot', help='plot data using gnuplot as png. needs python-gnuplot.', action='store_true', default=False)
    parser.add_option('-r', '--rainbow', help='use different color for each segment. png-plots and kml only.', action='store_true', default=False)
    parser.add_option('-s', '--svg', help='use svg output for plot (-p).', action='store_true', default=False)
    parser.add_option('-w', '--waypoint', help='input data is waypoint-format from gpstrans', action='store_true', default=False)
    (options, args) = parser.parse_args(argv)

    if len(args) < 3:
        parser.error('You must at least specify a file containing gps-data and the name of the file to generate')
    if (options.svg and options.rainbow) or (options.svg and options.bicolor):
        print 'Ignoring color-option when plotting SVG as not possible with GNUplot!'
    if (options.waypoint and options.rainbow) or (options.waypoint and options.bicolor):
        print 'Note: rainbow and bicolor don\'t work with waypoint data!'
    if options.waypoint and options.join:
        print 'Ignoring join-option when in waypoint-mode!'

    if options.mxmap:
        data = parseMXMap(args[1])
    elif options.gpsman:
        data = parseGpsman(args[1])
    elif options.waypoint:
        data = parseWaypoint(args[1])
    else:
        data = parseGpsTrans(args[1])

    if data is None or len(data) is 0:
        print 'Oops, no data found. Check if it\'s there!'
    else:
        if options.plot:
            plot(data, args[2])
        else:
            generateKML(data, args[2])


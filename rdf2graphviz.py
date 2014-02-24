#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
# Simple rdf to graphviz converter
#
# Copyright (C) 2008, Pascal Mainini <http://mainini.ch>
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


from rdflib.Graph import Graph as rdfGraph
from sys import argv
import pydot

if __name__ == "__main__":
    g = rdfGraph()        
    g.parse(argv[1], format=argv[2])

    edges = []
    edgeslabels = []
    for triple in g:
        sub = str(triple[2])
        pre = str(triple[1])
        obj = str(triple[0])
    
        # hack: remove full path from string
        sub = sub[47:]  
        pre = pre[47:]
        obj = obj[47:]

        edges.append((obj, sub))
        edgeslabels.append((obj, sub, pre))
                
    vg = pydot.graph_from_edges(edges,directed=True)
    vg.set_overlap('scale')

    # per-edge configuration
    for triple in edgeslabels:
        edge = vg.get_edge(triple[0], triple[1])
        edge.set_label(triple[2])
 
    vg.write_svg(argv[1] + '.svg', prog='dot') 
 

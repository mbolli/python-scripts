#!/usr/bin/env python
# -*- coding: utf-8 -*-

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
 

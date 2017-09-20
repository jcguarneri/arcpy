# -*- coding: utf-8 -*-
"""
Created on Tue May 24 16:23:27 2016


one-off script


@author: guarneri
"""

import arcpy

thisMap = arcpy.mapping.MapDocument("CURRENT")

df = arcpy.mapping.ListDataFrames(thisMap)[0]

sdeLayers = arcpy.mapping.ListLayers(thisMap,'*Manholes')

gridCursor = arcpy.da.SearchCursor("expandedGrid",['SHAPE@','PageNum'])

for layer in sdeLayers:
    with arcpy.da.UpdateCursor(layer,['SHAPE@','DBID','ASSETID']) as nodeCursor:
        for grid in gridCursor:
            gridGeom = grid[0]
            gridNum = str(grid[1])
            for node in nodeCursor:
                if gridGeom.contains(node[0]):
                    node[2] = gridNum + '-' + str(node[1])
                    nodeCursor.updateRow(node)
            nodeCursor.reset()
        gridCursor.reset()
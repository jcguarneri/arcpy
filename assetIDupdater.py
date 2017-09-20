# -*- coding: utf-8 -*-
"""
Spyder Editor

This temporary script file is located here:
C:\Python27\WinPython-32bit-2.7.6.4\settings\.spyder2\.temp.py
"""

import arcpy


#create Search Cursor to iterate through nodes and extract node ID
nodes = arcpy.da.SearchCursor("mergeJunctions",['SHAPE@','CITYID'])

#collect number of node records
numNodes =0
for node in nodes:
    numNodes += 1
nodes.reset()


#create update cursor to update the pipe id of each segment
pipes = arcpy.da.UpdateCursor("swPipes selection",['SHAPE@','CITYID','UPNODE','DOWNNODE'])

#iterate through segments
for pipe in pipes:

#store first and last point geometries        
    firstPoint = pipe[0].firstPoint
    lastPoint = pipe[0].lastPoint

#reset upstream and downstream IDs for use in while loop    
    upStreamID = -1
    downStreamID = -1
    count =0
#iterater through nodes and check for spatial overlap    
#use while loop to break as soon as both IDs are collected
       
    while (upStreamID == -1 or downStreamID == -1) and count < numNodes:    
                  
            for node in nodes:
                        
                if node[0].equals(firstPoint):
                    upStreamID = node[1]
                   
                    count += 1
                elif node[0].equals(lastPoint):
                    downStreamID = node[1]
                    
                    count += 1
                else:
                    count += 1
        
#assemble output row, retaining original geometry
    outRow = [pipe[0],str(upStreamID) + "-" + str(downStreamID),str(upStreamID),str(downStreamID)]
    print(outRow[1], count)
#update feature with output row values and reset search cursor
    pipes.updateRow(outRow)
    nodes.reset()


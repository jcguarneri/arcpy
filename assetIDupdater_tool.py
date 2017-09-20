# -*- coding: utf-8 -*-
"""
Spyder Editor

This temporary script file is located here:
C:\Python27\WinPython-32bit-2.7.6.4\settings\.spyder2\.temp.py
"""

import arcpy

#collect input parameters


inNodes = arcpy.GetParameterAsText(0)
inIDField = arcpy.GetParameterAsText(1)
inPipes = arcpy.GetParameterAsText(2)
outIDField = arcpy.GetParameterAsText(3)
outUpField = arcpy.GetParameterAsText(4)
outDownField =arcpy.GetParameterAsText(5)
#arcpy.SetParameterAsText(6,inPipes)

#create Search Cursor to iterate through nodes and extract node ID
nodes = arcpy.da.SearchCursor(inNodes,['SHAPE@',inIDField])

#collect number of node records
numNodes = 0
for node in nodes:
    numNodes += 1
nodes.reset()


#create update cursor to update the pipe id of each segment
pipes = arcpy.da.UpdateCursor(inPipes,['SHAPE@',outIDField,outUpField,outDownField])


#iterate through segments
for pipe in pipes:

#store first and last point geometries        
    firstPoint = pipe[0].firstPoint
    lastPoint = pipe[0].lastPoint

#reset upstream and downstream IDs for use in while loop    
    upStreamID = None
    downStreamID = None
    count =0
#iterater through nodes and check for spatial overlap    
#use while loop to break as soon as both IDs are collected
       
    while (count < numNodes) and (upStreamID == None or downStreamID == None) :    
                  
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
    
#update feature with output row values and reset search cursor
    pipes.updateRow(outRow)
    nodes.reset()


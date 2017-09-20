# -*- coding: utf-8 -*-
"""
Created on Thu Sep 11 11:52:28 2014

@author: guarneri
"""

import arcpy

#set input features and label field
inFeatures = r"local"
labelField = 'label'
largeGrid = r"km1"




#call update cursor with shape and label fields and iterate through rows
with arcpy.da.UpdateCursor(inFeatures,('SHAPE@',labelField)) as rows:
    for row in rows:
         
        #create geometry object from shape field
        geom = row[0]
        
        
        #arcpy.SelectLayerByLocation_management(largeGrid,"CONTAINS",geom,0,"NEW_SELECTION")
        for grid in arcpy.da.SearchCursor(largeGrid,('GRID1MIL','GRID100K','SHAPE@')):
            gridGeo = grid[2]
            if gridGeo.contains(geom):            
                labelA = grid[0]
                labelB = grid[1]
        #extract grid labels from minimum X and Y Values
        xMin = str(int(geom.extent.XMin))[1:4]
        yMin = str(int(geom.extent.YMin))[2:5]
         
        #set label field         
        
        row[1] = '%s %s %s %s'%(labelA,labelB,xMin,yMin)
        
        #commit changes        
        rows.updateRow(row)
        
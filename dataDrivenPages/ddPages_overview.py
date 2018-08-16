"""
Script to create polygons from the extents of each page in a data driven page set.
"""

import arcpy
import os
#collect input parameters
inName = arcpy.GetParameterAsText(0)
nameOrNumber = arcpy.GetParameter(1)
#inName = arcpy.GetParameterAsText(2)

#arcpy.env.workspace = inPath

#create map document object from current map
thisMap = arcpy.mapping.MapDocument("CURRENT")

#create data driven pages object
ddPages = thisMap.dataDrivenPages

#get spatial reference from data frame
frame = arcpy.mapping.ListDataFrames(thisMap)[0]
inRef = frame.spatialReference

#get page name field if "Name" option is selected
if nameOrNumber == True:
    nameField = str(ddPages.pageNameField.name)
else:
    pass

inPath = os.path.split(inName)[0]
inTable = os.path.split(inName)[1]


#create feature class to hold overview polygons and add label field
arcpy.CreateFeatureclass_management(inPath,inTable,"POLYGON",'',"DISABLED","DISABLED",inRef)
arcpy.AddField_management(inName,"label",'TEXT')


with arcpy.da.InsertCursor(inName,['SHAPE@','label']) as polyCursor:
    for pageNum in range(1, ddPages.pageCount + 1):
        ddPages.currentPageID = pageNum

#set overview polygon labels as either page number or page name        
        if  nameOrNumber == True:       
            zone = ddPages.pageRow.getValue(nameField)
        else:
            zone = ddPages.currentPageID
           
#create polygon from extents of Data Driven Page Extent           
        Ext = ddPages.dataFrame.extent 
        bbox = (Ext.lowerLeft,Ext.lowerRight,Ext.upperRight,Ext.upperLeft)
        array = arcpy.Array()
        for i in bbox:
            array.append(i)
        
        poly = arcpy.Polygon(array)           
        
#create new row with polygon object and label field        
        polyCursor.insertRow([poly,zone])
    

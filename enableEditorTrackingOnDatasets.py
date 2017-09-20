# -*- coding: utf-8 -*-
"""
Created on Mon Aug 10 16:52:30 2015

@author: martinson
"""
import arcpy
import os
workspace = raw_input("Enter workspace:\n")
walk = arcpy.da.Walk(workspace)
for dirpath, dirnames, filenames in walk:
     for filename in filenames:
         dataset = os.path.join(dirpath,filename)
         filedesc = arcpy.Describe(dataset)
         if not filedesc.editorTrackingEnabled:
             print "Enabling Editor Tracking on " + filename
             arcpy.EnableEditorTracking_management(dataset,"CREATOR","CREATED","LASTEDITOR","LASTEDITED","NO_ADD_FIELDS","DATABASE_TIME")
         else:
             print "Did not enable Editor Tracking on" + filename    
             continue
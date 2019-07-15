"""
Script to copy layer info between maps in a pro project. Useful for rebuilding
a map with errors. You will first have to add the feature classes to the new 
map and import symbology. All layers must match the layer name in the source
map. To copy between pro projects, change destproj from None to the path of the
destination project.
"""


import arcpy

projpath = 	#path to pro project
destproj = None	#path to destination pro project (if different from projpath) 
oldMapName =	#name of map to copy info from
newMapName =	#name of map to copy info to
excludeLayers = ()	#list of layer names to exclude (list all excluded layers in source and destination)

#connect to pro project and specify map
thisProj = arcpy.mp.ArcGISProject(projPath)
oldMap = thisProj.listMaps(oldMapName)[0]
#list layers to copy info from
oldLayers = oldMap.listLayers()
#create blank dictionary to store layer info
layerDict = {}
#iterate through layers and store info in dictionary
for layer in oldLayers:
	if layer.name == excludeLayers:
		pass
	else:
		name = layer.name
		layerDict[name] = {
		"definitionQuery" : layer.definitionQuery,
		"maxThreshold" : layer.maxThreshold,
		"minThreshold" : layer.minThreshold,
		"visible" : layer.visible}

#connect to destination project if applicable
if destproj is not None:
	thisProj = arcpy.mp.ArcGISProject(destproj)
else:
	pass

#specify name of map to copy info to	
newMap = thisProj.listMaps(newMapName)[0]
#list layers in new map to copy info to
newLayers = newMap.listLayers()
#iterate through layers in new map and copy layer info
for layer in newLayers:
	if layer.name not in excludeLayers:
		pass
	else:
		name = layer.name
		layer.definitionQuery = layerDict[name]["definitionQuery"]
		layer.maxThreshold = layerDict[name]["maxThreshold"]
		layer.minThreshold = layerDict[name]["minThreshold"]
		layer.visible = layerDict[name]["visible"]
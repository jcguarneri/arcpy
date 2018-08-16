#set map document
thisMap = arcpy.mapping.MapDocument("CURRENT")

#set layer to be varied
layer = arcpy.mapping.ListLayers(thisMap,"No response*")[0]




#create list of query selection terms
stations = ['1','2', '3', '4', '5']


#iterate through query terms
for station in stations:

    #update layer definition query and map dynamic text label
    layer.definitionQuery = "\"labels\" NOT LIKE" +"'%"+station+"%'"
    thisMap.author = station
    arcpy.RefreshActiveView()

    #place appropriate text box
    textBox = arcpy.mapping.ListLayoutElements(thisMap,"TEXT_ELEMENT",station)[0]
    textBox.elementPositionX = 6.7282
    textBox.elementPositionY = 4.9709
    
    #set PDF destination and export
    outPDF = r"C:/temp/response_zones%s"%station
    arcpy.mapping.ExportToPDF(thisMap,outPDF,"PAGE_LAYOUT",640,480,'300',"BEST",
                              "RGB",True,"ADAPTIVE","RASTERIZE_BITMAP",False,
                              False,"LAYERS_ONLY",True,100)

#move text box back out of frame, laid out for easy editing
    textBox.elementPositionX = 6.2*int(station)-9
    textBox.elementPositionY = -1

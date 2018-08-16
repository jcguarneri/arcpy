"""
Script to move title box around for different pages during export.
This specific script was for a series of maps of city quadrants that
required 4 unique positions, but it could be easily modified to simply
work with left or right pages (use modulus to find even/odd page numbers),
or to move inset maps around.
"""


#specify output pdf base name
outPDF = r"X:\GIS_BASE_MAP\Map Database\manhattan_fire\Maps\Driver Maps\NEW\unlabeled.pdf"

#specify the current map as the working document
thisMap = arcpy.mapping.MapDocument("CURRENT")

#create an object referencing the title box
#previously named "TitleGroup" to aid in python location)
titleBox = arcpy.mapping.ListLayoutElements(thisMap,'',"TitleGroup")[0]

#create data driven pages object
ddPages = thisMap.dataDrivenPages

#create dictionary to set position of the title box based on page #
#title box is set to anchor to top left corner
#positions are inches from bottom left of page
titlePos = {1:(1,18.07),
            2:(22.26,18.07),
            3:(1,1),
            4:(22.26,1)}

#iterate through data driven pages and export to PDF
for pageNum in range(1, ddPages.pageCount + 1):
    ddPages.currentPageID = pageNum

    #set X and Y positions of the title box
    titleBox.elementPositionX = titlePos[pageNum][0]
    titleBox.elementPositionY = titlePos[pageNum][1]

    arcpy.refreshActiveView()
    #export current page to pdf
    ddPages.exportToPDF(outPDF,"CURRENT","","PDF_MULTIPLE_FILES_PAGE_NAME",
                        300,"BEST","RGB",True,"ADAPTIVE","RASTERIZE_BITMAP",
                        False,True,"LAYERS_ONLY",False,100)

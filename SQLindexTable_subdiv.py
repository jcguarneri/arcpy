"""
Script to create index tables for streets, zoning,
and other feature classes.

Output is a tab-delimited text file that can then
be formatted in any spreadsheet or word processing
program.

__author__ = "Jay Guarneri"
__credits__ = ["Jay Guarneri"]
__license__ = "GPL"
__version__ = "0.9"
__maintainer__ = "Jay Guarneri"
__email__ = "guarneri@cityofmhk.com"
__status__ = "Development"
"""



#collect input parameters
inFeatures = arcpy.GetParameterAsText(0) #features to be indexed
inQuery = arcpy.GetParameterAsText(1) #optional query to filter features
inGrid = arcpy.GetParameterAsText(2) #reference grid features
outFile = arcpy.GetParameterAsText(3) #output text file
nameField = arcpy.GetParameterAsText(4) #name/ID field for index display
gridField = arcpy.GetParameterAsText(5) #name of grid field
numField  = arcpy.GetParameterAsText(6) #name of number field

#ensure in_memory can be written to
arcpy.Delete_management(r"in_memory/")

#apply subset query
if inQuery !='':
        arcpy.SelectLayerByAttribute_management(inFeatures,"NEW_SELECTION",inQuery)

#perform spatial join
joinTable = r"in_memory/joinTable"
arcpy.SpatialJoin_analysis(inFeatures,inGrid,joinTable,"JOIN_ONE_TO_MANY","KEEP_ALL")

#clear any selections
if inQuery != '':
	arcpy.SelectLayerByAttribute_management(inFeatures,"CLEAR_SELECTION")

#create summary table
statFields = [[nameField,"COUNT"]]
caseFields = [nameField,gridField,numField]
summaryTable = r"in_memory/indexTable"

arcpy.Statistics_analysis(joinTable,summaryTable,statFields,caseFields)

#open output file in write mode
f = open(outFile,"w")

#create search cursor query to exclude null/blank values
query = "%s IS NOT NULL AND %s <> '' AND %s IS NOT NULL"%(nameField,nameField,gridField)


#initialize variables for file lines
usedNames = []
gridCells =""
name=''
num ='' 

#use a sorted search cursor to generate text file
for row in sorted(arcpy.da.SearchCursor(summaryTable,caseFields,query), key = lambda s:s[0].lower()):

    #check to see if name has been encountered
    if str(row[0]) not in usedNames:
        #add name to list of names
        usedNames.append(str(row[0]))
        #write existing entry to file (blank line if first name)
        f.write(num + "\t" + name + "\t" + gridCells[:-2] + "\n")
        #start new entry
        gridCells = ""
        name = str(row[0])
        num = str(int(row[2]))
        gridCells += "%s, "%(str(row[1]))

    #add grid cells to entry if on a name already used
    else:
        gridCells += "%s, "%(str(row[1]))

#write last line
f.write(num + "\t" + name + "\t" + gridCells[:-2] + "\n")
#save output text file
f.close()

#delete temporary files
arcpy.Delete_management(joinTable)
arcpy.Delete_management(summaryTable)


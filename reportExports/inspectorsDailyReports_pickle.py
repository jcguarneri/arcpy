"""
Inspector's Daily Report export script.

Goes through all records in daily report feature service, checks
if the report for that OBJECTID has already been exported, then exports it.
Afterwards, the list of completed reports is stored for future reference
"""
#import modules for arcgis, date/time functionality, file system navigation, and regular expressions
import arcpy
import datetime
import os
import re
import pickle

#print start time. for testing purposes only, currently disabled.
print "Start time: %s"%datetime.datetime.now()

#set input variables
inMap = r'J:\GIS\MapDocuments\InspectorsDailyReports\InspectorsDailyReport.mxd' #map document to work from
reportSource = r'J:\GIS\MapDocuments\InspectorsDailyReports\InspectorsDailyReport.rlf' #report template file
outFolder = r'P:\2018\reportTest' #output folder for reports
dateStr = r'(\d+/\d+/\d+)' #regular expression to look for dates in project titles
dirName = os.path.dirname(__file__) #gets current directory to save pickle file
pickleFile = os.path.join(dirName,r'finishedReports.pk') #file to store list of already exported reports

#retrieve list of finished reports from pickle file
if os.path.exists(pickleFile):

	with open(pickleFile,'rb') as fi:
		doneList = pickle.load(fi)


	doneStr = '('

	for i in doneList:
		doneStr += '%s,'%i
	doneStr = doneStr[:-1] + ')'
	
else:
	doneStr = '(-1)'
	doneList = []


#create a MapDocument object from input map, and create a layer object for the feature service
reportMap = arcpy.mapping.MapDocument(inMap)
layer = arcpy.mapping.ListLayers(reportMap,'Inspectors_Daily_Report')[0]

#create a SearchCursor to iterate through entries in feature service table
#exclude reports that have already been exported
inForms = arcpy.da.SearchCursor(layer,
	('OBJECTID','report_date','project_title'),
	"OBJECTID not in %s"%doneStr)

#start list of successfully exported OBJECTIDs
outList = []	
	
#iterate through rows, and create reports if necessary
for row in inForms:
     
	#extract date information from timestamp
	date = datetime.datetime.date(row[1])
	
	#create string with date in mm/dd/yyyy format
	outDate = '%s_%s_%s'%(date.month,date.day,date.year)
	
	#build report title string using report name and date
	#use regex and .strip() to clean up extraneous dates and whitespace in report name
	title = '%s_%s'%(re.sub(dateStr,'',row[2]).strip(),outDate)
	outPDF = os.path.join(outFolder,'%s.pdf'%title)
	
	

 
	#create definition query for report to only export current entry
	queryStr = """"report_date" = '%s' AND "project_title" = '%s'"""%(row[1],row[2])

	#export report to specified location
	try:
		arcpy.mapping.ExportReport(layer,reportSource,outPDF,"DEFINITION_QUERY",title,report_definition_query = queryStr)
		#if successful, add OBJECTID of report to master list
		outList.append(row[0])
		
	#error handling for reports that won't export properly
	except IOError as e:
		print "Failed on %s."%title,"I/O error({0}): {1}".format(e.errno, e.strerror)
	except ValueError as e:
		print "Failed on %s."%title,e
	except NameError as e:
		print "Failed on %s."%title,e
	except TypeError as e:
		print "Failed on %s."%title,e,row[0],type(row[0])
	except:
		print "Failed on %s."%title,"Unexpected error:", sys.exc_info()[0] 
			

#append list of newly exported reports to list and write new pickle file
newList = doneList + outList
with open(pickleFile, 'wb') as fi:
	pickle.dump(newList,fi)			

		
#print end time. for testing purposes only, currently disabled.		
print "End time: %s."%datetime.datetime.now()

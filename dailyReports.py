"""
Inspector's Daily Report export script.

Goes through all records in daily report feature service, checks
if the PDF already exists, and exports the report if it isn't there yet.
"""
#import modules for arcgis, date/time functionality, file system navigation, and regular expressions
import arcpy
import datetime
import os
import re

#print start time. for testing purposes only, currently disabled.
#print "Start time: %s"%datetime.datetime.now()

#set input variables
inMap = r'J:\GIS\MapDocuments\InspectorsDailyReports\InspectorsDailyReport.mxd' #map document to work from
reportSource = r'J:\GIS\MapDocuments\InspectorsDailyReports\InspectorsDailyReport.rlf' #report template file
outFolder = r'P:\2018\reportTest' #output folder for reports
dateStr = r'(\d+/\d+/\d+)' #regular expression to look for dates in project titles

#create a MapDocument object from input map, and create a layer object for the feature service
reportMap = arcpy.mapping.MapDocument(inMap)
layer = arcpy.mapping.ListLayers(reportMap,'Inspectors_Daily_Report')[0]

#create a SearchCursor to iterate through entries in feature service table
inForms = arcpy.da.SearchCursor(r"Inspectors Daily Report v2\Inspectors_Daily_Report",('report_date','project_title'))

#iterate through rows, and create reports if necessary
for row in inForms:
     
	#extract date information from timestamp
	date = datetime.datetime.date(row[0])
	
	#create string with date in mm/dd/yyyy format
	outDate = '%s_%s_%s'%(date.month,date.day,date.year)
	
	#build report title string using report name and date
	#use regex and .strip() to clean up extraneous dates and whitespace in report name
	title = '%s_%s'%(re.sub(dateStr,'',row[1]).strip(),outDate)
	outPDF = os.path.join(outFolder,'%s.pdf'%title)
	
	#check to see if PDF of report already exists
	#if not, create new PDF. if yes, skip to next entry
	if not os.path.exists(outPDF):
	 
		#create definition query for report to only export current entry
		queryStr = """"report_date" = '%s' AND "project_title" = '%s'"""%(row[0],row[1])
	
		#export report to specified location
		try:
			arcpy.mapping.ExportReport(layer,reportSource,outPDF,"DEFINITION_QUERY",title,report_definition_query = queryStr)
		
		#error handling for reports that won't export properly
		except IOError as e:
			print "Failed on %s."%title,"I/O error({0}): {1}".format(e.errno, e.strerror)
		except ValueError as e:
			print "Failed on %s."%title,e
		except NameError as e:
			print "Failed on %s."%title,e
		except:
			print "Failed on %s."%title,"Unexpected error:", sys.exc_info()[0] 
			
		
	else:
		pass

		
#print end time. for testing purposes only, currently disabled.		
#print "End time: %s."%datetime.datetime.now()
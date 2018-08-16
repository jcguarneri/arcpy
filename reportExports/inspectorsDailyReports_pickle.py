"""
Inspector's Daily Report export script.

Goes through all records in daily report feature service, checks
if the PDF already exists, and exports the report if it isn't there yet.
"""
#import modules for arcgis, date/time functionality, file system navigation, regular expressions and pickle
import arcpy
import datetime
import os
import re
import pickle

#set input variables
inMap = r'J:\GIS\MapDocuments\InspectorsDailyReports\InspectorsDailyReport.mxd' #map document to work from
reportSource = r'J:\GIS\MapDocuments\InspectorsDailyReports\InspectorsDailyReport.rlf' #report template file
outFolder = r'J:\ENGINEER\Engineering Projects\Inspector Daily Reports' #output folder for reports
dateStr = r'(\d+/\d+/\d+)' #regular expression to look for dates in project titles
dirName = os.path.dirname(__file__) #directory of this script to save pickle file and log file
pickleFile = os.path.join(dirName,r'finishedReports.pk') #file to store list of already exported reports
logFile = os.path.join(dirName,'log.txt') #log file to store list of failed reports

#collect and store start time
t1 = datetime.datetime.now()

with open(logFile,'w') as log:

	#log start time
	log.write('Start time: %s\n'%t1.ctime())

	
	
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
		
		#store pdf in folder by year
		yearFolder = os.path.join(outFolder,str(date.year))
		
		#create year folder if it doesn't exist
		if not os.path.exists(yearFolder):
			os.makedirs(yearFolder)
		
		#build report title string using report name and date
		#use regex and .strip() to clean up extraneous dates and whitespace in report name
		title = '%s_%s'%(re.sub(dateStr,'',row[2]).strip(),outDate)
		outPDF = os.path.join(yearFolder,'%s.pdf'%title)
		
		

	 
		#create definition query for report to only export current entry
		queryStr = """"report_date" = '%s' AND "project_title" = '%s'"""%(row[1],row[2])

		#export report to specified location
		try:
			arcpy.mapping.ExportReport(layer,reportSource,outPDF,"DEFINITION_QUERY",title,report_definition_query = queryStr)
			#if successful, add OBJECTID of report to master list
			outList.append(row[0])
			
		#error handling for reports that won't export properly
		#log all errors in log file
		except IOError as e:
			log.write("Failed on {0}.\t{1}{2}".format((title,"I/O error({0}): {1}".format(e.errno, e.strerror),'\n')))
		except ValueError as e:
			log.write("Failed on {0}.\t{1}{2}".format(title,e,'\n'))
		except NameError as e:
			log.write("Failed on {0}.\t{1}{2}".format(title,e,'\n'))
		except:
			log.write("Failed on {0}.\t{1} {2}{3}".format(title,"Unexpected error:", sys.exc_info()[0],'\n'))
				

	#append list of newly exported reports to list and write new pickle file
	newList = doneList + outList
	with open(pickleFile, 'wb') as fi:
		pickle.dump(newList,fi)			

	
	
	#log end time and run duration		
	t2 = datetime.datetime.now()
	
	delta = t2 - t1
	minutes = delta.seconds//60
	seconds = delta.seconds%60
	
	log.write("End time: %s.\n"%t2.ctime())
	log.write("Elapsed time: {0} m {1} s.".format(minutes,seconds))

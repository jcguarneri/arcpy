import PyPDF2

inFile = r'C:\path\to\file.pdf'
inAppendPages = PyPDF2.pdf.PdfFileReader(inFile)

#create dictionary index of pages that need to be rotated, and the required rotation
#page numbers are 0 based
pageKey = {2:180,4:180,5:180,7:180,8:270,9:180,10:180,14:180,17:180,19:180}

pdf_in = open(inFile,'rb')

#create pdf reader object
inAppendPages = PyPDF2.pdf.PdfFileReader(pdf_in)

#create pdf writer object
outAppendPages = PyPDF2.pdf.PdfFileWriter()

#read pages from original pdf in to output pdf
#if page is in index, rotate by specified amount
for pageNum in range (inAppendPages.numPages):
	page = inAppendPages.getPage(pageNum)
	if pageNum in pageKey:
		page.rotateClockwise(pageKey[pageNum])
	outAppendPages.addPage(page)

#create output file and write output pdf to file
outFile = open(r'C:\path\to\output.pdf','wb')
outAppendPages.write(outFile)
pdf_in.close()
outFile.close()

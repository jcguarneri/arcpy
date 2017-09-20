import PyPDF2

inFile = r'C:\Users\guarnerij\Desktop\temp\bostonPost.pdf'
inAppendPages = PyPDF2.pdf.PdfFileReader(inFile)

pageKey = {2:180,4:180,5:180,7:180,8:270,9:180,10:180,14:180,17:180,19:180}

pdf_in = open(inFile,'rb')

inAppendPages = PyPDF2.pdf.PdfFileReader(pdf_in)

outAppendPages = PyPDF2.pdf.PdfFileWriter()


for pageNum in range (inAppendPages.numPages):
	page = inAppendPages.getPage(pageNum)
	if pageNum in pageKey:
		page.rotateClockwise(pageKey[pageNum])
	outAppendPages.addPage(page)


outFile = open(r'C:\Users\guarnerij\Desktop\temp\bostonPostFixed.pdf','wb')
outAppendPages.write(outFile)
pdf_in.close()
outFile.close()
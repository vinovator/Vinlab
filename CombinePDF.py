#Python 3
#CombinePDF.py
#Gets inputs of 2 PDF file names from user and combines them into 1

import PyPDF2
import os

def getFileNameFromUser (file):
	pdf_file_name = input("Enter {0} name: ".format(file))
	if pdf_file_name in os.listdir():
		return pdf_file_name
	else:
		print ("The file specified is not present in the directory")
		#Use recursive call to the same function until user gets it right
		getFileNameFromUser(file)

		
def addPageToWriter(pdfReader, pdfWriter):
	for pageNum in range(pdfReader.numPages):
		pageObj = pdfReader.getPage(pageNum)
		pdfWriter.addPage(pageObj)
	
	
def getFinalPdfNameFromUser():
	return input("Enter the final pdf file name with .pdf extn: ")

if __name__ == "__main__":

	#Change the current folder path to the one containing PDF files
	pdf_path = ".\PDF"
	os.chdir(pdf_path)

	#Get the name of the 2 pdf files from user
	#file 2 will be appended into file 1
	pdf1 = getFileNameFromUser("File 1")
	pdf2 = getFileNameFromUser("File 2")

	#Create file objects for both the files
	pdf1FileObj = open(pdf1, "rb")
	pdf2FileObj = open(pdf2, "rb")

	#Pass the file objects to the file reader
	pdf1Reader = PyPDF2.PdfFileReader(pdf1FileObj)
	pdf2Reader = PyPDF2.PdfFileReader(pdf2FileObj)
	
	#create a Pdf writer object
	pdfWriter = PyPDF2.PdfFileWriter()
	
	#Add individual pages from pdf files to writer object
	addPageToWriter(pdf1Reader, pdfWriter)
	addPageToWriter(pdf2Reader, pdfWriter)
	
	pdfOutputFileObj = open(getFinalPdfNameFromUser(), "wb")
	print (".. Appending file 2 to file 1....")
	pdfWriter.write(pdfOutputFileObj)
	print ("... done...")
	pdfOutputFileObj.close()
	pdf1FileObj.close()
	pdf2FileObj.close()
#Python 2.7.6
#DemergePDF.py
#Gets raw_inputs of 1 PDF file names from user and demerge into 2

import PyPDF2
import os

def getFileNameFromUser (file, path):
	pdf_file_name = raw_input("Enter {0} name: ".format(file))
	if pdf_file_name in os.listdir(path):
		return pdf_file_name
	else:
		print ("The file specified is not present in the directory")
		#Use recursive call to the same function until user gets it right
		getFileNameFromUser(file)

		
def addPageToWriter(pdfReader, pdfWriter, start, end):
	for pageNum in range(start, end):
		pageObj = pdfReader.getPage(pageNum)
		pdfWriter.addPage(pageObj)
	
	
def getFinalPdfNameFromUser():
	return raw_input("Enter the final pdf file name with .pdf extn: ")

if __name__ == "__main__":

	#Change the current folder path to the one containing PDF files
	pdf_path = "./PDF/"
	#os.chdir(pdf_path)

	#Get the name of the parent pdf files from user
	#This file will be demerged into 2 files
	parent_pdf = getFileNameFromUser("Give parent PDF name with .pdf extn", pdf_path)

	#Create file objects for both the files
	pdfFileObj = open(os.path.join(pdf_path + parent_pdf), "rb")

	#Pass the file objects to the file reader
	pdfReader = PyPDF2.PdfFileReader(pdfFileObj)
	
	#create a Pdf writer object
	pdfWriter1 = PyPDF2.PdfFileWriter()
	pdfWriter2 = PyPDF2.PdfFileWriter()
	
	#Add individual pages from pdf files to writer object
	addPageToWriter(pdfReader, pdfWriter1, 0, pdfReader.numPages/2)
	addPageToWriter(pdfReader, pdfWriter2, pdfReader.numPages/2, pdfReader.numPages)
	
	pdfOutputFileObj1 = open(os.path.join(pdf_path + getFinalPdfNameFromUser()), "wb")
	pdfOutputFileObj2 = open(os.path.join(pdf_path + getFinalPdfNameFromUser()), "wb")
	print (".. Demerging parent pdf file....")
	pdfWriter1.write(pdfOutputFileObj1)
	pdfWriter2.write(pdfOutputFileObj2)
	print ("... done...")
	pdfOutputFileObj1.close()
	pdfOutputFileObj2.close()
	pdfFileObj.close()
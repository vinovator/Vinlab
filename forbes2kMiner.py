# forbes2kMiner.py
# Python 3.4


"""
Extracts the Forbes Global 2000 list of companies and imports into a CSV file
Since Forbes is a JS rendered site, selenium is used to mimic user action
BeautifulSoup is used to scrape html content
Since selenium is used, Firefox is needed as webdiver
"""


from bs4 import BeautifulSoup
# import requests # Not needed since selenium is used
# import csv # Not needed as pandas to_csv is used
import os
import logging
import json  # to persist dict
import re
from urllib.parse import urljoin  # to join base and relative urls
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By  # For waiting till continue button is enabled
from selenium.webdriver.support.ui import WebDriverWait  # For waiting till continue button is enabled
from selenium.webdriver.support import expected_conditions as ec  # For waiting till continue button is enabled
from selenium.common.exceptions import NoSuchElementException, WebDriverException, ElementNotVisibleException
import time  # to insert wait time to browser
import pandas as pd


"""
Fobes G2k list is found in url - "http://www.forbes.com/global2000/list/"
Company info list is found in url - http://www.forbes.com/companies/<company name>/
"""


logging.basicConfig(filename = "ForbesG2KMiner_Logger.log", 
					format = "%(asctime)s: %(levelname)s: %(funcName)s: %(lineno)d: %(message)s",
					datefmt = "%m-%d-%Y %I:%M:%S %p",
					filemode = "w", 
					level = logging.INFO) # All DEBUG logs will be skipped

forbes = "http://www.forbes.com"

#g2k = "/global2000/list/120/#tab:overall"
g2k = "/global2000/list/"

forbes_g2k = urljoin(forbes, g2k)

json_dump_path = "./JSON_DUMP"  # Folder where each company level detailed info are persisted
os.makedirs(json_dump_path, exist_ok = True)

output_path = "./Forbes2000" # Folder where all output csv files will be generated
os.makedirs(output_path, exist_ok = True)

g2k_csv_file = "g2k_list.csv" # Holder of complete g2k list

output_csv_file = "output_csv_g2k.csv" # csv file with filter applied

output_excel_file = "output_excel_g2k.xlsx" # Excel file with filter applied

is_csv_data_source = True # If true dataframe will be imported from CSV; else scraped from website

is_populate_missing_detailed_data = True # If true, assumes detailed data is already extracted; and missing data will be fetched again

csv_data_source_file_name = "g2k_list_2000.csv" # If import from CSV is turned on, this will be imported


def write_final_output(df):
	""" Write final output to csv and excel file

	The final output is the detailed forbes g2k data
	Get pandas dataframe and write it to csv and excel file
	"""
	# Write the results into a csv file
	try:
		logging.info("Writing final output to csv file")
		df.to_csv(os.path.join(output_path + "/" + output_csv_file), index = False, encoding="utf-8")
		print ("{0} generated successfully at {1}\n".format(output_csv_file, output_path))
	except Exception as e:
		logging.exception("Error writing final output to csv file")
		print ("Error generating csv file: ", e)


	# Write the results into a excel file using xlsx writer
	try:
		# Using xlsxwriter as engine throws byte stream treated as string error
		# So using openpyxl as engine
		logging.info("Writing final output to excel file")
		xl_writer = pd.ExcelWriter(os.path.join(output_path + "/" + output_excel_file), engine = "openpyxl")
		df.to_excel(xl_writer, index = False, sheet_name = "g2k")
		xl_writer.save()
		print ("{0} generated successfully at {1}\n".format(output_excel_file, output_path))
	except Exception as e:
		logging.exception("Error writing final output to excel file")
		print ("Error generating excel file: ", e)


def extract_detailed_company_info(g2k_df):
	""" Extract detailed company information from json files

	Once all the json files are extracted, combine it with the base data
	Return the combined data set
	"""

	# Extract the url column from the dataframe
	# If any filter required, apply it here 
	# so that additional info is only fetched for relevant rows
	company_url = g2k_df["Forbes_site_url"] # this is a pandas series

	comp_lst = list()

	for index, url in company_url.iteritems():
		comp_lst.append(extract_dict_from_json(index, url, json_dump_path))

	# Create data frame from list of dictionaries
	additional_info_df = pd.DataFrame(comp_lst)

	# drop duplicate columns from dataframe
	additional_info_df = additional_info_df.drop(["Country", "Sales"], axis=1) 

	# Create a inner join between additional info data frame and full g2k list data frame
	# Inner join because, we want matching rows from additional info and corresponding rows from G2k list
	# join based on "url" column
	combined_info_df = pd.merge(left = g2k_df, 
								right = additional_info_df,
								how = "inner", 
								left_on = "Forbes_site_url",
								right_on = "Forbes_site_url")

	return combined_info_df


def extract_dict_from_json(index, url, path):
	""" From a given path, extract json and return as dict

	Pass the company index, url and path to extract the json files from
	"""
	try:
		json_file_name = "{0}-{1}.json".format(index+1, url.split("/")[-2])
		logging.info("Extracting dict from json file {0}".format(json_file_name))
		with open(os.path.join(path + "/" + json_file_name), mode="r") as json_file:
			return json.load(json_file)
	except Exception as e:
		logging.exception("Error extracting dict from json file:")
		print("Error extracting dict from json file:", e)
		return {}


def persist_dict_as_json(comp_dict, index, url, path):
	""" Persist each row of detailed company info as json file

	Pass the company index, relative url and path to save the file
	"""
	try:
		#print(comp_dict)
		json_file_name = "{0}-{1}.json".format(index+1, url.split("/")[-2])
		logging.info("Saving the dict as json file {0}".format(json_file_name))
		with open(os.path.join(path + "/" + json_file_name), mode="w") as json_file:
			json.dump(comp_dict, json_file)
		return True
	except Exception as e:
		logging.exception("Error saving dict as json file:")
		print("Error saving dict as json file:", e)
		return False


def wrangle_data(g2k_df):
	""" Wrangle the data using pandas library

	The dataframe passed consists of base data
	Extract the url from this dataframe and scrap each company page
	The output dataframe will have additional company level data
	"""
	
	# Extract the url column from the dataframe
	# If any filter required, apply it here 
	# so that additional info is only fetched for relevant rows
	company_url = g2k_df["Forbes_site_url"] # this is a pandas series

	for index, url in company_url.iteritems():
 
		# Pass the url to selenium to automate bypassing ad page
		# For company info page dynamic scroll down is not required
		# This distinction is indicated by the page_type parameter
		logging.info("{0} : Scraping {1}".format(index + 1, url))
		print ("{0} : Scraping {1}".format(index + 1, url))

		logging.info("Start - Extracting html source from company info web page")
		html_company_info = mimic_user(url, "company_info")
		#print(html_company_info)
		logging.info("End - html source from company info web page extracted")

		soup = BeautifulSoup(html_company_info, "lxml")

		comp_dict = dict() # This holds company's basic information

		# Extract company basic information
		logging.info("Extracting basic company information")
		for block in soup.find_all("div", {"class": "data has_image"}):
			for dl in block("dl"):
				# Sometimes there are issues in retrieving values, catch those
				try:
					# Some attributes could be url links. Read accordingly.
					if (dl("dd")[0].has_attr("a")):
						#comp_dict[dl("dt")[0].string] = dl("dd")[0].a.string.encode("utf-8")
						comp_dict[dl("dt")[0].getText().strip()] = dl("dd")[0].a.getText().strip()
					else:
						#comp_dict[dl("dt")[0].string] = (dl("dd")[0].string.encode("utf-8") if dl("dd")[0].string is not None else dl("dd")[0].getText().strip())
						comp_dict[dl("dt")[0].getText().strip()] = dl("dd")[0].getText().strip()
				except AttributeError as e:
					logging.exception("Error extracting basic company info")
					print ("Error retrieving {0} : {1}".format(comp_dict[dl("dt")[0].string]), e)
					comp_dict[dl("dt")[0].getText().strip()] = "ERROR"

		# Extract company forbes ranking information
		logging.info("Extracting company ranking information")
		for block in soup.find_all("div", {"class": "forbes-list"}):
			for li in block("li"):
				#forbes_data[li.a.string] = li.getText().strip()
				try:
					# comma is used as 1000 separator. So get full string instead of digits
					comp_dict[li.a.getText()] = re.findall(r"#(\d+,{0,1}\d*)", li.getText().strip())[0] # Extract the digit following "#"
					#comp_dict[li.a.getText()] = li.getText().strip()
				except IndexError as e:
					# Sometimes the "#" character is not present, then keep key and value same
					logging.exception("Error retrieving ranking information")
					print ("Ranking info cannot be retrieved for {0}".format(li.a.getText()))
					comp_dict[li.a.getText()] = li.a.getText()

		# Append the url value as one of the dict key-value pairs
		comp_dict["Forbes_site_url"] = url

		# Persist the dict by saving as json file; if unsuccessful log as error
		if not (persist_dict_as_json(comp_dict, index, url, json_dump_path)):
			logging.error("Error saving dict as json file for {0}".format(url))

	# Return successfully if all rows are processed
	return True


def mimic_user(url, page_type):
	""" Use selenium to mimic user action

	Wait for 3 to 5 seconds to have forbes "continue" button enabled
	Click the continue button to enter forbes g2k list page
	Keep scrolling the page down to render more and more rows
	Return the html to calling block
	"""


	# Firefox and chromedriver are gui based browser webdriver option
	# PhantomJs is a headless browser
	try:
		# driver = webdriver.Firefox()
		driver = webdriver.PhantomJS()
		driver.set_window_size(1024,768) # Needed only for phantomjs
		logging.info("Opening webdriver")
		driver.get(url)
	except WebDriverException as e:
		logging.exception("Error using webdriver")
		print ("Error using webdriver: ", e)

	# Click on the enabled continue button automatically after waiting
	# Sometimes the site skips the welcome page, in those case skip this
	try:
		# Forbes site has the annoying welcome page
		# Wait for 3 to 5 seconds to have the continue button enabled
		#time.sleep(3)
		#driver.find_element_by_class_name("continue-button").click()

		# Code below checks every 500 millisecond, if the continue button is clickable
		logging.info("Welcome page! wait begins")

		# First check if the element is there. If this fails then NoSuchElementException
		continue_button = driver.find_element_by_class_name("continue-button")
		element = WebDriverWait(driver, 20).until(
			ec.element_to_be_clickable((By.CLASS_NAME, "continue-button")))
		element.click()
		logging.info("Welcome page! Wait ended")

	except NoSuchElementException:
		# Sometimes the welcome page is skipped and the company page is directly opened
		logging.warning("Welcome page skipped")
		pass
	except ElementNotVisibleException:
		# Code below checks every 500 millisecond, if the continue button is clickable
		logging.warning("Welcome page! Button not visible. Wait for more")
		element = WebDriverWait(driver, 20).until(
			ec.element_to_be_clickable((By.CLASS_NAME, "continue-button")))
		element.click()
		logging.info("Welcome page! Button visible now, Wait ended")
	except Exception as e:
		logging.exception("Welcome page! Error for {0}: {1}".format(url,e))
		pass

	if page_type == "g2k":
		print ("Extracting info from site {0}".format(url))
		html_Elem = driver.find_element_by_tag_name('html')

		logging.info("Forbes base data! Scroll down begins")
		# Mimic user scrolling to render more rows
		# TO:DO - find the number of loops to render all 2000 rows
		# 10 loops approximately fetches 200 rows
		for i in range(5):
			time.sleep(0.5)
			print("Scrolling down..{0}".format(i))
			html_Elem.send_keys(Keys.END)
		logging.info("Forbes base data! Scroll down ends")

	html_source = driver.page_source

	driver.quit()

	# Extract the html content of the source for BeautifulSoup
	return html_source


def get_base_data_from_csv():
	""" Get the base g2k data from csv file if csv data source is turned on

	If the parameter is turned off, then the base data is scraped from Forbes website
	"""

	print ("Importing base data from csv file..")

	# Extract dataframe from csv file
	g2k_df = pd.read_csv(os.path.join(output_path + "/" + csv_data_source_file_name))
						#nrows=2,
						#skiprows = range(1,1905))

	numrows, numcols = g2k_df.shape

	logging.info("Imported {0} rows and {1} columns from csv file".format(numrows, numcols))
	print("Read the csv file into dataframe. Number of rows: {0}; Number of columns: {1}".format(numrows, numcols))

	return g2k_df


def get_missing_rows_from_csv():
	""" Get the information of missing rows from detailed data csv output

	If the parameter is turned off, then the base data is imported from csv
	"""
	print ("Importing missing data from csv file..")

	# Extract dataframe from csv file
	g2k_df = pd.read_csv(os.path.join(output_path + "/" + output_csv_file))
						#nrows=2,
						#skiprows = range(1,1905))

	# From the output csv file, extract rows where the detailed info is empty
	g2k_df = g2k_df.loc[pd.isnull(g2k_df["Global 2000 "]) == True]

	# Select first 7 columns only, which makes this similar to base data df
	g2k_df = g2k_df[g2k_df.columns[0:8]]

	numrows, numcols = g2k_df.shape

	logging.info("Missing rows extracted from output CSV. Number of rows: {0}; Number of columns: {1}".format(numrows, numcols))
	print("Missing rows extracted from output CSV. Number of rows: {0}; Number of columns: {1}".format(numrows, numcols))

	return g2k_df


def get_base_data_from_forbes():
	""" Get the base g2k data from forbes website if csv data source is turned off

	If the parameter is turned on, then the base data is imported from csv
	"""

	#res = requests.get(htmwl_source)
	#soup = BeautifulSoup(res.content)

	logging.info("Start - Get source html from Forbes website")
	html_source = mimic_user(forbes_g2k, "g2k")
	logging.info("End - Source html extracted from Forbes website")

	soup = BeautifulSoup(html_source, "lxml")

	#print (soup.prettify(encoding="utf-8"))

	#table = soup.find_all("table", {"id": "the_list"})

	# This carries the header row for G2K list
	headers = []

	# This list of lists carries the data rows for G2K list
	g2k_rows = []

	logging.info("Extracting headers")
	print ("Extracting g2k list headers..\n")
	for tr in soup.find_all("thead"):
		for th in tr("th"):
			for label in th("a"):
				headers.append(label.getText())

	# Add an extra column header to hold url informaton
	headers.append("Forbes_site_url")
	#print(headers)

	# table = soup.find_all("tbody", {"id": "list-table-body"})


	logging.info("Extracting rows")
	print ("Extracting g2k list rows..\n")
	for block in soup.find_all("tbody", {"id": "list-table-body"}):
		# An ad row is plugged in every 10 rows. Exclude ads by selecting class = data
	    for tr in block("tr", {"class":"data"}):

    		tr_list = [tr("td")[1].string, # class = rank
    			# Some company names has unicode characters
    			tr("td")[2].a.string.encode("utf_8"), 	# class = name
    			tr("td")[3].string.encode("utf-8"), 	# Country
    			tr("td")[4].string.encode("utf-8"), 	# Sales
    			tr("td")[5].string.encode("utf-8"), 	# Profits
    			tr("td")[6].string.encode("utf-8"), 	# Assets
    			tr("td")[7].string.encode("utf-8"),	# Market Value
    			tr("td")[0].a.get("href")]	# relative url
    		
    		g2k_rows.append(tr_list)

	#print (g2k_rows)

	print ("g2k list rows extracted..\n")

	# Add the rows and header to pandas dataframe
	g2k_df = pd.DataFrame(g2k_rows, columns=headers)

	# Convert from relative path to absolute path
	# Lambda basically does a for loop over each row, but necessary if url join has to be used
	#g2k_pd["Forbes_site_url"] = g2k_pd["Forbes_site_url"].map(lambda x : urljoin(forbes, x))
	# Simply concatenate to join urls, but be careful with leading or missing "/" character
	g2k_df["Forbes_site_url"] = forbes + g2k_df["Forbes_site_url"]

	#g2k_pd.loc[g2k_pd.Forbes_site_url] = g2k_pd.loc[urljoin(forbes, g2k_pd.Forbes_site_url)]

	# Write the g2k list into a csv file
	try:
		g2k_df.to_csv(os.path.join(output_path + "/" + g2k_csv_file), index = False, encoding="utf-8")
		logging.info("Base data written to csv file")
		print ("{0} generated successfully at {1}".format(g2k_csv_file, output_path))
		print ("{0} rows added\n".format(len(g2k_df.index)))
	except Exception as e:
		logging.exception("Error writing base data to csv file")
		print ("Error generating csv file: ", e)

	return g2k_df


def main():
	""" Starting block """

	print("Let's begin..")
	logging.info("Start")

	# Import dataframe from csv file when this variable is turned on
	if (is_csv_data_source):

		if (is_populate_missing_detailed_data):
			# Import missing rows from detailed info csv file
			logging.info("Importing missing rows from detailed info csv file")
			df = get_missing_rows_from_csv()
		else:
			# Import base data from csv file
			logging.info("Importing base data from csv file")
			df = get_base_data_from_csv()

	# Extract rows from forbes site only when variable import_from_csv is turned off
	else:
		# Extract base data by scraping forbes site
		logging.info("Extracting base data from scraping Forbes website")
		df = get_base_data_from_forbes()

	# Extract detailed company information from base data
	logging.info("Base data extracted. Extracting detailed company information")

	if(wrangle_data(df)):
		logging.info("Detailed company info saved as json")
		# consider the entire 2000 rows set when adding missing rows
		if (is_populate_missing_detailed_data):
			df = get_base_data_from_csv()
		detailed_df = extract_detailed_company_info(df)

		# Write final output to csv and excel file
		logging.info("Detailed company level information extracted from json dump. Writing the output")
		write_final_output(detailed_df)

		# Once the full data set is retrieved check if any rows are missing from output data set
		missing_df = get_missing_rows_from_csv()

		missing_rows, missing_cols = missing_df.shape

		# If there are missing rows, then repeat the exercise for missing rows again
		if(missing_rows > 0):
			if(wrangle_data(missing_df)):
				logging.info("Missing Detailed company info saved as json")

				# consider the entire 2000 rows set when adding missing rows
				missing_detailed_df = extract_detailed_company_info(df)
				# Write final output to csv and excel file
				logging.info("Detailed company level information extracted from json dump. Writing the output")
				write_final_output(detailed_df)
		else:
			logging.info("No missing rows")
			print("No missing rows")

	else:
		logging.error("Error wrangling data")


if __name__ == "__main__":
	main()

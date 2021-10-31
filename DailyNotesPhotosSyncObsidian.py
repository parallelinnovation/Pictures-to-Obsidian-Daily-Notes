#----------------------------------------------#
#---- Pictures to Obsidian Daily Notes --------#
#----------------------------------------------#
# Author: Adrian Papineau
# Date created: October 31st, 2021



import glob
import os
import time
import platform
from datetime import datetime
from mdutils import *
import pyimgur

ObsidianVaultPath = "" # Example "C:/Users/YourName/ObsidianVault/VaultName/DailyNotesFolder"
CLIENT_ID = "" # Get your imgur client ID from: https://api.imgur.com/oauth2/addclient
'''
Program requirements:
- Needs to:
	- Return newest file incrimentally
	- If it isn't already present in markdown file, add it to the file. 
	
'''
# Find newest file in folder
def SearchNewFile():
	list_of_files = glob.glob('C:/Users/adria/Pictures/*') # * means all if need specific format then *.csv
	latest_file = max(list_of_files, key=os.path.getctime)
	return latest_file
print(SearchNewFile())

# Upload to imgur
PATH = SearchNewFile()
im = pyimgur.Imgur(CLIENT_ID)
uploaded_image = im.upload_image(PATH, title="Uploaded with PyImgur")
print(uploaded_image.title)
print(uploaded_image.link)
print(uploaded_image.size)
print(uploaded_image.type)

ImageLink = uploaded_image.link

# Extract date from file
def creation_date(path_to_file):
    if platform.system() == 'Windows':
        return os.path.getctime(path_to_file)
    else:
        stat = os.stat(path_to_file)
        try:
            return stat.st_birthtime
        except AttributeError:
            return stat.st_mtime

dateExtract = creation_date(SearchNewFile())

# Convert weird date format to Roam-style format (example: October 31st, 2021)
dateExtractFirstFormat = datetime.fromtimestamp(dateExtract).strftime('%Y-%m-%d %H:%M:%S')
print(dateExtractFirstFormat)
dateExtractMonth = datetime.fromtimestamp(dateExtract).strftime('%B')
dateExtractDay = datetime.fromtimestamp(dateExtract).strftime('%d')
dateExtractYear = datetime.fromtimestamp(dateExtract).strftime('%Y')
dateExtractTime = datetime.fromtimestamp(dateExtract).strftime('%H:%M')
print(dateExtractTime)

if dateExtractDay[0] == "0":
	dateExtractDay = dateExtractDay[-1]
def dayFormatter(): #Can be improved
	if dateExtractDay[-1] == "0":		
		dateExtractNUM = str(dateExtractDay + "th")
	if dateExtractDay[-1] == "1":		
		dateExtractNUM = str(dateExtractDay + "st")
	if dateExtractDay[-1] == "2":		
		dateExtractNUM = str(dateExtractDay + "nd")
	if dateExtractDay[-1] == "3":		
		dateExtractNUM = str(dateExtractDay + "rd")
	if dateExtractDay[-1] == "4":		
		dateExtractNUM = str(dateExtractDay + "th")
	if dateExtractDay[-1] == "5":		
		dateExtractNUM = str(dateExtractDay + "th")
	if dateExtractDay[-1] == "6":
		dateExtractNUM = str(dateExtractDay + "th")
	if dateExtractDay[-1] == "7":
		dateExtractNUM = str(dateExtractDay + "th")
	if dateExtractDay[-1] == "8":
		dateExtractNUM = str(dateExtractDay + "th")
	if dateExtractDay[-1] == "9":
		dateExtractNUM = str(dateExtractDay + "th")
	if dateExtractDay[-1] == "10":
		dateExtractNUM = str(dateExtractDay + "th")
	return(dateExtractNUM)
RoamFormat = str(dateExtractMonth + " " + str(dayFormatter()) + ", " + dateExtractYear)
print(RoamFormat)

# Write file to end of each daily note in markdown folder

DailyNoteName = (RoamFormat + ".md")
print(DailyNoteName)
fileName = (ObsidianVaultPath +"/" + DailyNoteName)
md = MdUtils(fileName)
md.read_md_file(fileName) 
imgLink = str("- " + dateExtractTime + " ![](" + ImageLink + ")")
md.new_line(imgLink)
md.create_md_file() 

# Future improvements:
# - Needs to be able to search the markdown document and see if the picture already exists,
#   so that it can ignore uploading to avoid duplicates. 
# - Needs to run incrementally. Not sure how I will aprroach this yet. 
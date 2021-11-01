import time
from watchdog.observers import Observer
from watchdog.events import PatternMatchingEventHandler
import glob
import os
import time
import platform
from datetime import datetime
from mdutils import *
import pyimgur

ObsidianVaultPath = "" # Example "C:/Users/YourName/ObsidianVault/VaultName/DailyNotesFolder"
ImageFolderPath = ""
CLIENT_ID = "" # Get your imgur client ID from: https://api.imgur.com/oauth2/addclient


# Search filesystem for new files(photos)
if __name__ == "__main__":
    patterns = ["*"]
    ignore_patterns = None
    ignore_directories = False
    case_sensitive = True
    my_event_handler = PatternMatchingEventHandler(patterns, ignore_patterns, ignore_directories, case_sensitive)

def on_created(event):
    print(f"{event.src_path} has been created")
    #upload_to_imgur({event.src_path})
    ModifyMDFile(dayFormatter(creation_date(SearchNewFile())))

def on_modified(event):
    print(f"{event.src_path} has been modified")

my_event_handler.on_created = on_created
my_event_handler.on_modified = on_modified

go_recursively = True
my_observer = Observer()
my_observer.schedule(my_event_handler, ImageFolderPath, recursive=go_recursively)

# Upload to Imgur
def upload_to_imgur(PATH):
    im = pyimgur.Imgur(CLIENT_ID)
    uploaded_image = im.upload_image(PATH, title="Uploaded with PyImgur")
    print(uploaded_image.title)
    print(uploaded_image.link)
    print(uploaded_image.size)
    print(uploaded_image.type)
    ImageLink = uploaded_image.link   
    return(ImageLink)

def SearchNewFile():
    ImageFolderPathPlusAll = str(ImageFolderPath + "/*")
    list_of_files = glob.glob(ImageFolderPathPlusAll) # * means all if need specific format then *.csv
    latest_file = max(list_of_files, key=os.path.getctime)
    return latest_file

# Extract date from file
def creation_date(PATH):
    if platform.system() == 'Windows':
        return os.path.getctime(PATH)
    else:
        stat = os.stat(PATH)
        try:
            return stat.st_birthtime
        except AttributeError:
            return stat.st_mtime

# Convert weird date format to Roam-style format (example: October 31st, 2021)
def dayFormatter(Extract):
    dateExtractMonth = datetime.fromtimestamp(Extract).strftime('%B')
    dateExtractDay = datetime.fromtimestamp(Extract).strftime('%d')
    dateExtractYear = datetime.fromtimestamp(Extract).strftime('%Y')

    # Get rid of the beginning 0 in day of the month. 
    if dateExtractDay[0] == "0":
        dateExtractDay = dateExtractDay[-1]
    # Add the "th" or similar
    if (dateExtractDay[-1] == "0") or ((int(dateExtractDay[-1]) >=4) and (int(dateExtractDay[-1]) <10)):       
        dateExtractNUM = str(dateExtractDay + "th")
    elif dateExtractDay[-1] == "1":       
        dateExtractNUM = str(dateExtractDay + "st")
    elif dateExtractDay[-1] == "2":       
        dateExtractNUM = str(dateExtractDay + "nd")
    elif dateExtractDay[-1] == "3":       
        dateExtractNUM = str(dateExtractDay + "rd")
    RoamFormat = str(dateExtractMonth + " " + dateExtractNUM + ", " + dateExtractYear)
    print(RoamFormat)
    return(RoamFormat)
    
    RoamFormat = str(dateExtractMonth + " " + dateExtractNUM + ", " + dateExtractYear)
    print(RoamFormat)
    return(RoamFormat)

# Write file to end of each daily note in markdown folder
def ModifyMDFile(RoamFormatDate):
    dateExtractTime = datetime.fromtimestamp(creation_date(SearchNewFile())).strftime('%H:%M')
    print(dateExtractTime)
    DailyNoteName = (RoamFormatDate + ".md")
    print(DailyNoteName)
    fileName = (ObsidianVaultPath +"/" + DailyNoteName)
    md = MdUtils(fileName)
    md.read_md_file(fileName) 
    imgLink = str("- " + dateExtractTime + " ![](" + upload_to_imgur(SearchNewFile()) + ")")
    md.new_line(imgLink)
    md.create_md_file() 


# Start monitoring 
my_observer.start()
try:
    while True:
        time.sleep(1)
except KeyboardInterrupt:
    my_observer.stop()
    my_observer.join()


            

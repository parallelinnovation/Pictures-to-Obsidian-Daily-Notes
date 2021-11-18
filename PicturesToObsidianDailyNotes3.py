# Pictures to Obsidian Daily Notes
# Author: Adrian Papineau
# Date: 2021-11-18


import time
from watchdog.observers import Observer
from watchdog.events import PatternMatchingEventHandler
import glob
import os
from os import path
import time
import platform
from datetime import datetime, date
import shutil
import imghdr
from pathlib import Path

DailyNotesPath = ""
ObsidianVaultPathImages = ""
ImageFolderPath = ""


# Search filesystem for new files(photos)
if __name__ == "__main__":
    patterns = ["*"]
    ignore_patterns = None
    ignore_directories = False
    case_sensitive = True
    my_event_handler = PatternMatchingEventHandler(patterns, ignore_patterns, ignore_directories, case_sensitive)

def on_created(event):
	print(f"{event.src_path} has been created")
	PhotoName({event.src_path}) 
	ConvertBackslash({event.src_path})

    

def on_modified(event):
    print(f"{event.src_path} has been modified")

my_event_handler.on_created = on_created
my_event_handler.on_modified = on_modified

go_recursively = True
my_observer = Observer()
my_observer.schedule(my_event_handler, ImageFolderPath, recursive=go_recursively)

#-----------------#

#return current daily note file path

today = date.today()
def CurrentDate(): 
    dateExtractMonth = today.strftime('%B')
    dateExtractDay = today.strftime('%d')
    dateExtractYear = today.strftime('%Y')
    # Get rid of the beginning 0 in day of the month. 
    if dateExtractDay[0] == "0":
        dateExtractDay = dateExtractDay[-1]
    # Add the "th" or similar
    if ((int(dateExtractDay) >= 10) and (int(dateExtractDay) <20)) or (dateExtractDay[-1] == "0") or ((int(dateExtractDay[-1]) >=4) and (int(dateExtractDay[-1]) <10)):       
        dateExtractNUM = str(dateExtractDay + "th")
    elif dateExtractDay[-1] == "1":       
        dateExtractNUM = str(dateExtractDay + "st")
    elif dateExtractDay[-1] == "2":       
        dateExtractNUM = str(dateExtractDay + "nd")
    elif dateExtractDay[-1] == "3":       
        dateExtractNUM = str(dateExtractDay + "rd")
    RoamFormat = str(dateExtractMonth + " " + dateExtractNUM + ", " + dateExtractYear)
    return RoamFormat
print(CurrentDate())

def CurrentDailyNote():
    DailyNoteName = (CurrentDate() + ".md")
    return DailyNoteName

#-----------------#

# check if uploaded files are image files:

def ConvertBackslash(path):
	str_val = " ".join(path)
	newPath = str_val.replace(os.sep, '/')
	print(newPath)
	CheckFile(newPath)

def PhotoName(PhotoPath):
	str_val = " ".join(PhotoPath)
	newPath = str_val.replace(os.sep, '/')
	BaseName = os.path.basename(newPath)
	BaseNameWithoutSpaces = BaseName.replace(' ','')
	return BaseNameWithoutSpaces

def CheckFile(file):
	My_file = Path(ObsidianVaultPathImages + "/" + PhotoName(file))
	print(My_file)
	if My_file.is_file():
		print("duplicate present")
	else:
		if (imghdr.what(file) != None) or (".HEIC" in file):
			CopyImage(file)

#copy image from folder to vault folder

def CopyImage(source):
	shutil.copy2(source, ObsidianVaultPathImages)
	print(source + " copied!")
	AppendImageLink(source)

# Append image link to Daily note

def AppendImageLink(Basename):
	t = time.localtime()
	current_time = time.strftime("%H:%M", t)
	dailyPath = DailyNotesPath + "/" + CurrentDailyNote()
	print(dailyPath)
	Notefile = open(dailyPath, encoding="utf8")

	NoteContent = Notefile.read()
	Notefile.seek(0)
	Notefile = open(dailyPath, "w", encoding="utf8")
	Notefile.write(NoteContent + "\n" + "- " + current_time + " ![[Photos/" + PhotoName(Basename) + "]]" + "\n")
	Notefile.seek(0)
	Notefile.close()


# Start monitoring 

my_observer.start()
try:
    while True:
        time.sleep(1)
except KeyboardInterrupt:
    my_observer.stop()
    my_observer.join()



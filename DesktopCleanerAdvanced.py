import os
import sys
import shutil
import logging
from pathlib import Path

LOG_FORMAT = "%(levelname)s %(asctime)s - %(message)s"
logging.basicConfig(filename = os.path.expanduser('~') + '\\Documents\\pythonlogging.log',
                    level = logging.info,
                    format = LOG_FORMAT,
                    filemode = 'w')
logger = logging.getLogger()



"""
Created by Jonathon Scofield
Desktop Cleaner Advance is a python application designed to organize files on your computer.
Primary development has been on a Windows machine, though it seems to work well on other platforms.

Selecting to do basic clean on desktop or downloads directories will move basic filetypes to their
respective user folders, create folders for shotcuts and executables within desktop/downloads
for those filetypes, and move folders present in those directories (with the exception of the folders
created by this application) into a created directory called 'Folders'.

Advanced organization will do a more thorough move of files within specified folders. 
If more than 3 (more, no less) of one filetype is discovered at that location, a folder is created
and all files of that filetype are moved to it. Folders are named either based on 
a dictionary value, or if the value is not present, based on the file extension.
Folders discovered during advanced organization are not moved.

Full scan does everything
"""


#file type dictionary
trueLocation = {"Documents": ["TXT", "FNT", "FON", "TEX", "TOAST", "OTF", "WPD", "CUE", "WPS", "DMG", "ODT", "BIN", "TTF", "XML","CSV", "DAT", "GED", "TORRENT", "ICS", "MSG", "KEY", "PAGES", "VCD", "RTF", "KEYCHAIN", "PPS", "PPT", "PPTX", "SDF", "TAR", "TAX2016", "TAX2017", "MDF", "VCF", "ISO", "PY", "LOG", "DOCX", "PDF", "XLR", "XLS", "XLSX", "ACCDB", "DB", "DBF", "MDB", "PDB", "SQL", "7Z", "CBR", "DEB", "GZ", "PKG", "RAR", "RPM", "SITX", "TAR.GZ", "ZIP", "ZIPX", "DOC", "ASP", "ASPX", "CER", "CFM", "CSR", "CSS", "DCR", "HTM", "HTML", "JS", "JSP", "PHP", "RSS", "XHTML"],
                "Pictures": ["BMP", "DDS", "GIF", "JPG", "PNG", "PSD", "PSPIMAGE", "TGA", "THM", "TIF", "TIFF", "YUV", "JPEG"],
                "Videos": ["3G2", "3GP", "ASF", "AVI", "FLV", "M4V", "MOV", "MP4", "MPG", "RM", "SRT", "SWF", "VOB", "WMV", "MPEG-4"],
                "Music": ["AIF", "IFF", "M3U", "M4A", "MID", "MP3", "MPA", "WAV", "WMA"],
                "Shortcut": ["LNK"],
                "Executables": ["EXE", "APK", "APP", "BAT", "SH", "CGI", "COM", "GADGET", "JAR", "WSF", "MSI"]}
#folder naming dictionary
advancedDictionary = {"Word Documents": ["DOC", "DOCX", "ODT", "WPD", "WPS"],
                      "Spreadsheets": ["XLS", "XLSX", "XLR"],
                      "Plain Text Files": ["TXT", "LOG", "PAGES", "TEX", "RTF"],
                      "Database Files": ["ACCDB", "DB", "DBF"],
                      "Presentations": ["PPS", "PPT", "PPTX", "KEY"],
                      "Image Files": ["BIN", "CUE", "DMG", "ISO", "MDF", "TOAST", "VCD"]}
#don't move these
dontMove = ["Folders", "Shortcuts", "Executables"]

#for yes and no questions
okDictionary = {"YES", "Y", "OK", "OKAY", "PLEASE", "PLEASE DO", "I HAVE BEEN WAITING FOR THIS MOMENT"}
noDictionary = {"NO", "HELL NO!", "N", "NEIN", "PLEASE DON'T", "I DO NOT BELIEVE THAT WILL BE NECESSARY"}

#the center of the universe (location)
loc = ''

#OneDrive sucks
oneLocation = {"OneDrive/Documents", "OneDrive/Pictures", "OneDrive/Music", "OneDrive/Videos", "OneDrive/Desktop"}

"""
Making folder for folders and placing folders in folder

Arguments:
    home: home directory
    location: folder item is in
    Item: Item to be moved
"""
def dealWithFolders(h, l, i):
    logger.info("# dealWithFolders({0}, {1}, {2})".format(h, l, i))
    place = h + "/" + l + "/Folders"
    nname = place + "/" + i
    if not os.path.exists(place):
        logger.debug("# Path does not exist. Creating folder")
        os.mkdir(place)
    if (not os.path.exists(nname) and (i not in dontMove)):
        logger.debug("# Folder to move does not already exist in new location.")
        if(i[0] != '~' and i[0] != '.'):
            logger.debug("# Folder is not hidden or special folder")
            try:
                shutil.move(h + "/" + loc + "/" + i, place + "/" + i)
                logger.debug("# Moving folder {0} to new location {1}".format(i, nname))
                print(i + " moved to Folders")
            except FileNotFoundError as err:
                logger.error("# Problem: " + err)
                print(i + " not Found")
            except PermissionError as pe:
                logger.error("# Problem: " + pe)
                print(i + " can't be moved")
        else:
            logger.debug("# Folder does not begin with '~' or with '.'")
            print(i + " was left alone")
    else:
        logger.debug("# Folder exists in new location already, or is unmovable folder")
        print(i + " was left alone")


"""
I'm sure you love all those new onedrive folders in 1809. Let's oraganize them.
Arguments:
    stype - the type of scan to be run (options are BASIC or ADVANCED)
    run - should the function be run?
    q - boolean, has the question been asked already. If false (default) will ask question in function


"""

def dealwithOneDrive(stype, run=False, q=False):
    logger.info("# dealwithOneDrive({0}, {1}, {2})".format(stype, run, q))
    loopy = False
    global loc
    if (os.path.isdir(str(Path.home()) + "/OneDrive/" + loc) and (run == True) and (stype.upper() == "BASIC" or stype.upper() == "ADVANCED")):
        logger.debug("# OneDrive directory exists. User said to scan through directory. Scan type is 'Basic' or 'Advanced'")
        if(q == False):
            logger.debug("# Not auto-running OneDrive folder scans")
            while loopy == False:
                scanme = input("Would you like to scan the OneDrive " + loc + " folder?")
                if scanme.upper() in okDictionary:
                    logger.debug("# User agreed to scan")
                    loc = "OneDrive/" + loc
                    loopy = True
                    if stype.upper() == "BASIC":
                        logger.debug("# Running Basic scan on OneDrive folder {}".format(loc))
                        basicClean(1)
                    elif stype.upper() == "ADVANCED":
                        logger.debug("# Running Advanced scan on OneDrive folder {}".format(loc))
                        advancedClean()
                    else:
                        logger.debug("# Error in stype")
                        print("Error in stype")
                elif scanme.upper() in noDictionary:
                    logger.debug("# User said no to scanning OneDrive folder")
                    loopy = True
                    print("Avoiding OneDrive folder")
                else:
                    logger.debug("# User input incorrect")
                    print("Please respond 'yes' or 'no'\n")
        else:
            logger.debug("# Auto-running OneDrive Scans")
            loc = "OneDrive/" + loc
            if stype.upper() == "BASIC":
                logger.debug("# Running Basic scan of OneDrive folder {}".format(loc))
                basicClean(1)
            elif stype.upper() == "ADVANCED":
                logger.debug("# Running Advanced scan of OneDrive folder {}".format(loc))
                advancedClean()


"""
Basic Cleaning function. 
Uses dictionary of file extensions to determine where all files within specified folder should go.
Moves files to their designated directories.
Folders within directories other than desktop/downloads are not organized, so fol is 0 by default

Arguments:
    fol: determines if folder organization within directory is enabled(1) or disabled(0)

"""
def basicClean(fol=0):
    logger.info("basicClean({})".format(fol))
    #get list of all files and subdirectories on desktop or downloads
    home = str(Path.home())
    files = os.listdir(home + "/" + loc)

    for item in files:
        logger.debug("# Getting all files in directory {}".format(loc))
        t = os.path.splitext(item)
        #Test if file is directory, if it is make a 'folders' directory on desktop and place them there
        if os.path.isdir(home + "/" + loc + "/" + item):
            logger.debug("# Directory Found")
            if fol == 1:
                logger.debug("# Dealing with directory")
                dealWithFolders(home, loc, item)
        #If item is a file
        else:
            #Check file extension against truelocation (list of file extensions)
            for key, value in trueLocation.items():
                for e in value: 
                    if t[1][1:].upper() == e:
                        logger.debug("# Found filetype in sorting list")
                        #Make folders to put Shortcuts and Executables and move those files there
                        if (key == "Shortcut") or (key == "Executables"):
                            logger.debug("# File is shortcut or executable")
                            s = home + "/" + loc + "/" + key
                            if not os.path.exists(s):
                                logger.debug("# Path for filetype sorting doesn't exist. Creating...")
                                os.mkdir(s)
                            if not os.path.isfile(s + "/" + item):
                                logger.debug("# File doesn't exists in path.")
                                if(item[0] != '~' and item[0] != '.'):
                                    try:
                                        shutil.move(home + "/" + loc + "/" + item, s + "/" + item)
                                        logger.debug("# Attempting to move..")
                                    except FileNotFoundError as err:
                                        logger.debug("# Problem: {}".format(err))
                                        print(item + " not Found")
                                    except PermissionError as pe:
                                        logger.debug("# Problem: {}".format(pe))
                                        print(item + " can't be moved")
                        #Move everything else where it needs to be
                        else:
                            if(item[0] != '~') and (item[0] != '.') and (not os.path.isfile(home + "/" + key + "/" + item)) and (not os.path.isdir(home + "/" + key + "/" + item)):
                                logger.debug("# File does not begin with '~' or '.'. File does not already exists in new Directory.")
                                try:
                                    # if ("OneDrive/" + key) in oneLocation: #check if it's one of onedrive's folders
                                    #     shutil.move(home + "/" + loc + "/" + item, home + "/OneDrive/" + key + "/" + item)
                                    # else:
                                    shutil.move(home + "/" + loc + "/" + item, home + "/" + key + "/" + item)
                                    logger.debug("# Attempting to move...")
                                except FileNotFoundError as err:
                                    logger.debug("# Problem: {}".format(err))
                                    print(item + " not Found")
                                except PermissionError as pe:
                                    logger.debug("# Problem: {}".format(pe))
                                    print(item + " can't be moved")
                        #Give user clue as to what's going on
                                if fol == 1:
                                    mess1 = "Found {}".format(item) + " and moved to " + key
                                    print(mess1)
                                    logger.debug(mess1)
                            else:
                                if fol == 1:
                                    mess2 = "Found {}".format(item) + " and left alone"
                                    print(mess2)
                                    logger.debug(mess2)

"""
Runs thorough scan of specific folders.
Phase 1: creates a list of all extensions and uses that to create a list of all extensions that appear
more than 3 times.

Phase 2: cycles through items. determines if they are on list of 3 or more. if necessary it cycles
through dictionary of directory names to see if the name for that filetype exists. If name is in dictionary
it creates the folder (if necessary) and moves item to that folder

Phase 3: if name not in folder name dictionary (and file not already moved obviously) it will create (if necessary)
a directory based on the file extension and move the item there.

    Arguments: None, don't even try
"""
def advancedClean():
    logger.info("advancedClean()")
    #Figures out what files need to be grouped together into a folder
    allofthem = []
    moreThan3 = []
    basicClean()
    home = str(Path.home())
    files = os.listdir(home + "/" + loc)
    for item in files:
        t = os.path.splitext(item)
        if os.path.isdir(home + "/" + loc + "/" + item):
            logger.debug(item + " is a folder")
            print("Folder " + item + " detected")
        else:
            allofthem.append(t[1])
            if (allofthem.count(t[1]) > 3) and (moreThan3.count(t[1]) == 0):
                logger.debug("# There are more than 3 {}. Adding to list to sort.".format(t[1]))
                moreThan3.append(t[1])
    #Grabs files and puts them in folders
    for item in files:
        t = os.path.splitext(item)          
        #make folders for files
        if moreThan3:
            #check if in advanced dictionary and moves files to named folders
            for key, value in advancedDictionary.items():
                for z in value:
                    if (t[1][1:].upper() == z) and (t[1] in moreThan3):
                        logger.debug("# {0} in dictionary. {1} has more than 3 instances".format(t[1][1:], t[1]))
                        s = home + "/" + loc + "/" + key
                        if not os.path.exists(s):
                            logger.debug("# Path {0} does not exist. Making entry.".format(s))
                            os.mkdir(s)
                        if not os.path.isfile(s + "/" + item):
                            logger.debug("# File {0} does not exist in path {1}".format(item, s))
                            if(item[0] != '~' and item[0] != '.'):
                                logger.debug("# File does not begin with '~' or '.'")
                                try:
                                    shutil.move(home + "/" + loc + "/" + item, s + "/" + item)
                                    logger.debug("# Attempting to move {0} to {1}".format(item, s))
                                    print("Found " + item + " and moving to " + s)
                                except FileNotFoundError as err:
                                    logger.debug("# Problem: {}".format(err))
                                    print(item + " not Found")
                                except PermissionError as pe:
                                    logger.debug("# Problem: {}".format(pe))
                                    print(item + " can't be moved")
            #If not in dictionary, combine into generic folders
            if os.path.exists(home + "/" + loc + "/" + item):
                nameFolder = home + "/" + loc + "/" + t[1][1:].upper()
                if (not os.path.exists(nameFolder)) and (t[1] in moreThan3) and (item[0] != "~") and (item[0] != '.'):
                    logger.debug("# Generic named folder {0} does not exist\n# {1} has more than 3 instances\n# File name does not begin with '~' or '.'\n# Making folder")
                    os.mkdir(nameFolder)
                if (not os.path.isfile(nameFolder + "/" + item)) and (os.path.exists(nameFolder)) and (not os.path.isdir(nameFolder + "/" + item)):
                    logger.debug("# File {0} does not exist in {1}".format(item, nameFolder))
                    if(item[0] != '~' and item[0] != '.'):
                        try:
                            shutil.move(home + "/" + loc + "/" + item, nameFolder + "/" + item)
                            logger.debug("# Attempting to move {0} to {1}".format(item, loc))
                            print("Found " + item + " and moving to " + nameFolder)
                        except FileNotFoundError as err:
                            logger.debug("# Problem: {}".format(err))
                            print(item + " not Found")
                        except PermissionError as pe:
                            logger.debug("# Problem: {}".format(pe))
                            print(item + " can't be moved")


x = False
#Initial selection screen
while x == False:
    here = input("Select User folder to organize('Desktop', 'Downloads')\n'Full' to organize all, or 'q' to quit\n(For Advanced Clean type 'Advanced')\n:  ")
    if here.upper() == "DESKTOP":
        loc = "Desktop"
        basicClean(1)
        dealwithOneDrive("basic", True)
        x = True
    elif here.upper() == "DOWNLOADS":
        loc = "Downloads"
        basicClean(1)
        dealwithOneDrive("basic", True)
        x = True
    #runs through everything. Most advanced scans done twice to make sure
    elif here.upper() == "FULL":
        loopyfull = False
        runme = False
        while loopyfull == False:
            qfull = input("Would you like to scan OneDrive Folders as well?\n")
            if qfull.upper() in okDictionary:
                runme = True
                loopyfull = True
            elif qfull.upper() in noDictionary:
                loopyfull = True
            else:
                print("Please type 'Yes' or 'No'")
        loc = "Desktop"
        basicClean(1)
        dealwithOneDrive("basic", runme, True)
        loc = "Downloads"
        basicClean(1)
        dealwithOneDrive("basic", runme, True)
        loc = "Documents"
        advancedClean()
        dealwithOneDrive("advanced", runme, True)
        loc = "Pictures"
        advancedClean()
        dealwithOneDrive("advanced", runme, True)
        loc = "Music"
        advancedClean()
        dealwithOneDrive("advanced", runme, True)
        loc = "Videos"
        advancedClean()
        dealwithOneDrive("advanced", runme, True)
        loc = "Music"
        advancedClean()
        dealwithOneDrive("advanced", runme, True)
        loc = "Pictures"
        advancedClean()
        dealwithOneDrive("advanced", runme, True)
        loc = "Documents"
        advancedClean()
        dealwithOneDrive("advanced", runme, True)
        x = True
    #If advanced clean is picked
    elif here.upper() == "ADVANCED":
        print("Advanced Clean")
        y = False
        while y == False:
            selection = input("Perform Advanced Clean on Pictures, Documents, Videos, or Music Folder? ")
            if selection.upper() == "DOCUMENTS":
                loc = "Documents"
                advancedClean()
                dealwithOneDrive("advanced", True)
                y = True
            elif selection.upper() == "PICTURES":
                loc = "Pictures"
                advancedClean()
                dealwithOneDrive("advanced", True)
                y = True
            elif selection.upper() == "VIDEOS":
                loc = "Videos"
                advancedClean()
                dealwithOneDrive("advanced", True)
                y = True
            elif selection.upper() == "MUSIC":
                loc = "Music"
                advancedClean()
                dealwithOneDrive("advanced", True)
                y = True
            elif (selection.upper() == "Q") or (selection.upper() == "QUIT") or (selection.upper() == "EXIT"):
                y = True
            else:
                print("Incorrect Value")
        x = True
    elif (here.upper() == "Q") or (here.upper() == "QUIT") or (here.upper() == "EXIT"):
        break
    else:
        print("incorrect input")
#Completion
end = input("Completed. Press any key to exit.")




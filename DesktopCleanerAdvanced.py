import os
import sys
import shutil
from pathlib import Path

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

#the center of the universe (location)
loc = ''


"""
Making folder for folders and placing folders in folder

Arguments:
    home: home directory
    location: folder item is in
    Item: Item to be moved
"""
def dealWithFolders(h, l, i):
    place = h + "/" + l + "/Folders"
    nname = place + "/" + i
    if not os.path.exists(place):
        os.mkdir(place)
    if (not os.path.exists(nname) and (i not in dontMove)):
        if(i[0] != '~' and i[0] != '.'):
            try:
                shutil.move(h + "/" + loc + "/" + i, place + "/" + i)
                print(i + " moved to Folders")
            except FileNotFoundError as err:
                print(i + " not Found")
            except PermissionError as pe:
                print(i + " can't be moved")
        else:
            print(i + " was left alone")
    else:
        print(i + " was left alone")


"""
Basic Cleaning function. 
Uses dictionary of file extensions to determine where all files within specified folder should go.
Moves files to their designated directories.
Folders within directories other than desktop/downloads are not organized, so fol is 0 by default

Arguments:
    fol: determines if folder organization within directory is enabled(1) or disabled(0)

"""
def basicClean(fol=0):
    #get list of all files and subdirectories on desktop or downloads
    home = str(Path.home())
    files = os.listdir(home + "/" + loc)

    for item in files:
        t = os.path.splitext(item)
        #Test if file is directory, if it is make a 'folders' directory on desktop and place them there
        if os.path.isdir(home + "/" + loc + "/" + item):
            if fol == 1:
                dealWithFolders(home, loc, item)
        #If item is a file
        else:
            #Check file extension against truelocation (list of file extensions)
            for key, value in trueLocation.items():
                for e in value: 
                    if t[1][1:].upper() == e:
                        #Make folders to put Shortcuts and Executables and move those files there
                        if (key == "Shortcut") or (key == "Executables"):
                            s = home + "/" + loc + "/" + key
                            if not os.path.exists(s):
                                os.mkdir(s)
                            if not os.path.isfile(s + "/" + item):
                                if(item[0] != '~' and item[0] != '.'):
                                    try:
                                        shutil.move(home + "/" + loc + "/" + item, s + "/" + item)
                                    except FileNotFoundError as err:
                                        print(item + " not Found")
                                    except PermissionError as pe:
                                        print(item + " can't be moved")
                        #Move everything else where it needs to be
                        else:
                            if(item[0] != '~') and (item[0] != '.') and (not os.path.isfile(home + "/" + key + "/" + item)) and (not os.path.isdir(home + "/" + key + "/" + item)):
                                try:
                                    shutil.move(home + "/" + loc + "/" + item, home + "/" + key + "/" + item)
                                except FileNotFoundError as err:
                                    print(item + " not Found")
                                except PermissionError as pe:
                                    print(item + " can't be moved")
                        #Give user clue as to what's going on
                                if fol == 1:
                                    print("Found {}".format(item) + " and moved to " + key)
                            else:
                                if fol == 1:
                                    print("Found {}".format(item) + " and left alone")

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
    #print("Advanced Clean not yet implemented")
    #Figures out what files need to be grouped together into a folder
    allofthem = []
    moreThan3 = []
    basicClean()
    home = str(Path.home())
    files = os.listdir(home + "/" + loc)
    for item in files:
        t = os.path.splitext(item)
        if os.path.isdir(home + "/" + loc + "/" + item):
            print("Folder " + item + " detected")
        else:
            allofthem.append(t[1])
            if (allofthem.count(t[1]) > 3) and (moreThan3.count(t[1]) == 0):
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
                        s = home + "/" + loc + "/" + key
                        if not os.path.exists(s):
                            os.mkdir(s)
                        if not os.path.isfile(s + "/" + item):
                            if(item[0] != '~' and item[0] != '.'):
                                try:
                                    shutil.move(home + "/" + loc + "/" + item, s + "/" + item)
                                    print("Found " + item + " and moving to " + s)
                                except FileNotFoundError as err:
                                    print(item + " not Found")
                                except PermissionError as pe:
                                    print(item + " can't be moved")
            #If not in dictionary, combine into generic folders
            if os.path.exists(home + "/" + loc + "/" + item):
                nameFolder = home + "/" + loc + "/" + t[1][1:].upper()
                if (not os.path.exists(nameFolder)) and (t[1] in moreThan3) and (item[0] != "~") and (item[0] != '.'):
                    os.mkdir(nameFolder)
                if (not os.path.isfile(nameFolder + "/" + item)) and (os.path.exists(nameFolder)) and (not os.path.isdir(nameFolder + "/" + item)):
                    if(item[0] != '~' and item[0] != '.'):
                        try:
                            shutil.move(home + "/" + loc + "/" + item, nameFolder + "/" + item)
                            print("Found " + item + " and moving to " + nameFolder)
                        except FileNotFoundError as err:
                            print(item + " not Found")
                        except PermissionError as pe:
                            print(item + " can't be moved")



x = False
#Initial selection screen
while x == False:
    here = input("Select User folder to organize('Documents', 'Videos', 'Pictures', 'Music')\n'Full' to organize all, or 'q' to quit\n(For Advanced Clean type 'Advanced')\n:  ")
    if here.upper() == "DESKTOP":
        loc = "Desktop"
        basicClean(1)
        x = True
    elif here.upper() == "DOWNLOADS":
        loc = "Downloads"
        basicClean(1)
        x = True
    #runs through everything. Most advanced scans done twice to make sure
    elif here.upper() == "FULL":
        loc = "Desktop"
        basicClean()
        loc = "Downloads"
        basicClean()
        loc = "Documents"
        advancedClean()
        loc = "Pictures"
        advancedClean()
        loc = "Music"
        advancedClean()
        loc = "Videos"
        advancedClean()
        loc = "Music"
        advancedClean()
        loc = "Pictures"
        advancedClean()
        loc = "Documents"
        advancedClean()
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
                y = True
            elif selection.upper() == "PICTURES":
                loc = "Pictures"
                advancedClean()
                y = True
            elif selection.upper() == "Videos":
                loc = "Videos"
                advancedClean()
                y = True
            elif selection.upper() == "Music":
                loc = "Music"
                advancedClean()
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




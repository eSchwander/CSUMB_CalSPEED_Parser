#!/usr/local/bin/python3
"""
------------------------------------------------------------------------
ARCHIVE.PY

AUTHOR(S):     Peter Walker    pwalker@csumb.edu

PURPOSE-  This script will be called at the end of the week (Sunday, 11:59) to
            archive all of the raw data processed and CSVs created throughout
            the week. If the week number is a multiple of 4 (ie. a month has
            passed), then the data that has been archived over the last 4 weeks
            is archived together, and moved into backups, and emailed to the
            ADMIN.
FUNCTIONS
    _createArchive
    main
------------------------------------------------------------------------
"""

#IMPORTS
import os
import sys
import shutil
import datetime
from _decorators import (__debug, __checkSysArg,
                         logFileLOCATION, ADMIN)
#END IMPORTS

#Checking that this script is being run by at least Python 3
major, *other = sys.version_info
if major<3:
    raise SystemExit("You must be running at least Python 3")



def __moveNO(file, directory, copy=False):
    """
    First determines if the file and directory exist. If they do not, then an
     error is raised. If they do, we find the name that will not conflict with
     any of the other files is the given directory. We then overwrite 'file',
     and pass everything back to the original function.
    """
    file = os.path.abspath(file)
    directory = os.path.abspath(directory)
    if not os.path.isfile(file):
        raise RuntimeError("The given file must be a legitimate file. "+
                           "Was given '{}'.".format(file))
    if not os.path.isdir(directory):
        raise RuntimeError("The given directory must be a legitimate directory. "+
                           "Was given '{}'.".format(directory))
    copyCount = 1
    newName = os.path.basename(file)
    listFiles = os.listdir(directory)
    while True:
        if newName in listFiles:
            listFiles.remove(newName)
            if copyCount > 1:
                newName = os.path.splitext(newName)[0][:-2] + os.path.splitext(newName)[1]
            newName = os.path.splitext(newName)[0] + " {}".format(copyCount) + os.path.splitext(newName)[1]
        else:
            break
    #END WHILE
    #Based on whether the user wanted to copy the file or not, we use shutil's copy2() or move()
    newfile = os.path.join(directory, newName)
    if copy:
        shutil.copy2(file, newfile)
    else:
        shutil.move(file, newfile)
    return True
#END DEF




def __createDataArchive(nowTime, directories, **kwargs):
    #Expanding the directories passed through 'directories'
    (PAR_DIR, __, __, DAT_DIR, __, __) = directories

    #We are going to simply move all files in the parsed directory 'PAR_DIR' into
    # the archival data directory 'DAT_DIR'
    for file in os.listdir(PAR_DIR):
        truePath = os.path.join(PAR_DIR, file)
        __moveNO(truePath, DAT_DIR)
    return True
#END DEF


def __createCSVArchive(nowTime, directories, **kwargs):
    #Expanding the directories passed through 'directories'
    (__, CSV_DIR, __, __, CSA_DIR, __) = directories

    #We are going to simply move all files in the parsed directory 'PAR_DIR' into
    # the archival data directory 'DAT_DIR'
    for file in os.listdir(CSV_DIR):
        if "daily" not in file.lower() and "all" not in file.lower():
            truePath = os.path.join(CSV_DIR, file)
            __moveNO(truePath, CSA_DIR)
    #END FOR
    return True
#END DEF


def __createYearlyArchive(nowTime, directories, **kwargs):
    #Expanding the directories passed through 'directories'
    (__, __, ARC_DIR, DAT_DIR, CSA_DIR, BKP_DIR) = directories

    #Making the file paths of the archives we will be creating
    dataArchive = os.path.join(BKP_DIR, "DATA_{}_backup".format(nowTime.year-1))
    csvsArchive = os.path.join(BKP_DIR, "CSVs_{}_backup".format(nowTime.year-1))

    dir_file_pairs = [(DAT_DIR, dataArchive),
                      (CSA_DIR, csvsArchive) ]

    for org, arc in dir_file_pairs:
        shutil.make_archive(arc, 'zip', root_dir=org)
        shutil.rmtree(org)
    #END FOR
    return True
#END DEF




def _createArchive(nowTime, directories, **kwargs):
    """
    Moves all of the processed data and generated day CSVs to the archive folder.
     If the week is the first of the year, then it zips all of the CSVs and Data,
     and moves it to the backup folder
    ARGS:
        nowTime         datetime object, the current time
          Tuple of directories. Expecting...
            PAR_DIR     String, the location of the archive folder, where all files
                         will be copied to upon successful parsing
            CSV_DIR     String, the directory of the CSVs
            ARC_DIR     String, the location of the folder where files are being archived
            DAT_DIR     String, the directory where processed data will be archived
            CSA_DIR     String, the directory where CSVs will be archived
            BKP_DIR     String, the directory where archives will be archived
    """
    #Expanding the directories passed through 'directories'
    (PAR_DIR, CSV_DIR, __, __, __, __) = directories
    #Setting the location of the daily and weekly CSV
    __, nowWeek, __ = nowTime.isocalendar()


    #This block archives all of the DATA sent to the server throughout the week
    if os.listdir(PAR_DIR):
        print("Moving all Raw Data uploaded over the last week to the archive folder...")
        __createDataArchive(nowTime, directories)
    else:
        print("No new Raw Data to archive...")
    #END IF/ELSE

    #This block archives all of the CSVs created throughout the week
    if os.listdir(CSV_DIR):
        print("Moving all CSVs created over the last week to the archive folder...")
        __createCSVArchive(nowTime, directories)
    else:
        print("No new CSVs to archive...")
    #END IF/ELSE


    #If the week number is 1, then we want to make a "yearly" archive of everything done over
    # the last year
    if nowWeek==1:
        __createYearlyArchive(nowTime, directories)
    else:
        print("No yearly archive to make...")
    #END IF/ELSE
#END DEF


@__debug(logFileLOCATION, ADMIN, fullDebug=True, funcName="Weekly Archiving")
@__checkSysArg
def main(**kwargs):
    """
    Archives data used over the last week, and if the week number is a multiple of 4,
    creates an archive of the last 4 weeks of data
    """
    #This sets the variables holding the paths to the folders we will need
    (BASEDIR, UPL_DIR, PAR_DIR,
     TMP_DIR, ERR_DIR, CSV_DIR,
     ARC_DIR, CSA_DIR, DAT_DIR,
     BKP_DIR) = kwargs['folderPaths']
    os.rmdir(TMP_DIR)

    #Making sure that each folder above is created, and creating it if it is not
    for path in [PAR_DIR, CSV_DIR, ARC_DIR, DAT_DIR, CSA_DIR, BKP_DIR]:
        if not os.path.isdir(path):
            raise ValueError("The path '{}' must exist for this script to run.".format(path))
    #END FOR

    #Setting some paths to CSVs that are common to all files
    nowTime = datetime.datetime.now()

    print("Archiving the last week's worth of data...")
    _createArchive(nowTime, (PAR_DIR, CSV_DIR, ARC_DIR, DAT_DIR, CSA_DIR, BKP_DIR))
    print("Archive functions complete. Now Exitting...")
#END DEF

if __name__=="__main__":
    main()

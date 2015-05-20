#!/usr/local/bin/python3
"""
------------------------------------------------------------------------
SORT_AND_EXTRACT.PY

AUTHOR(S):     Peter Walker    pwalker@csumb.edu

PURPOSE-  This script will be called every hour to check 'UploadData' for new
            text files to process. The files will be parsed, and then the
            necessary CSV values will be calculated and appended to the
            correct CSV files, generally "all_test_results.csv", a daily csv,
            a weekly csv, and the CSV containing all tests conducted on a certain date.
          Once all of the files have been processed, they will be catalogued
            into a folder in raw_data. Files that caused an exception will be
            logged and copied into a separate folder.
FUNCTIONS
    _find
    _makeDateCSVs
    _makeBaseCSVs
    main
------------------------------------------------------------------------
"""

#IMPORTS
import os
import sys
import shutil
import datetime
from _decorators import (__debug, __checkSysArg, logFileLOCATION)
from _sensitiveInfo.emailLogin import ADMIN

projectPath = os.path.join(os.getcwd(),os.path.dirname(__file__))
if projectPath not in sys.path:
    sys.path.append(projectPath)

from PyFiles.csvGeneration.csvGenerator import csvGenerator
from PyFiles.FileParser.FieldTest_File import FieldTest_File
from PyFiles.FileParser.CrowdSource_File import CrowdSource_File
#END IMPORTS

#Checking that this script is being run by at least Python 3
major, *other = sys.version_info
if major<3:
    raise SystemExit("You must be running at least Python 3")


def _find(BASEDIR, UPL_DIR, TMP_DIR, nowTime):
    """Finds files that are ready to process, and moves them to a temp directory"""
    #This will organize each file into a folder based on the modification data of the file, as
    # well as copy the file into the temporary directory
    print("Finding new files to process...")
    #Creating a datetime object that is set to 45 minutes ago
    filesToParse = []
    nowTimeLess = nowTime - datetime.timedelta(minutes=45)
    for file in os.listdir(UPL_DIR):
        truePath = os.path.abspath(os.path.join(UPL_DIR, file))
        #This will get the modification time of the file at 'truePath'. The value returned
        # in the attribute 'st_mtime' is an epoch time (time in seconds since 1/1/1970). That
        # is passed to datetime.fromtimestamp, which creates a datetime object
        lastModTime = datetime.datetime.fromtimestamp(os.stat(truePath).st_mtime)
        #If the modification time of the file is less than the time 45 minutes ago, then
        # we can pass it to the parser
        if lastModTime < nowTimeLess:
            filesToParse.append(truePath)
    #END FOR
    if len(filesToParse) == 0:
        return 0

    print("Found "+str(len(filesToParse))+" files. Processing...")
    #With all of the files found, we will get the file's modification date, copy the file
    # with all of it's metadata into the temp directory and a new directory (named the file's
    # creation data), and then remove the file
    #I may want to do some testing on the raw data. if so, we want to copy the files into
    # the dev folder, but only if the folder exists
    devFolder = os.path.join(BASEDIR, "dev", "UploadData")
    extracopy = False
    if os.path.isdir(devFolder):
        extracopy = True
    for file in filesToParse:
        if extracopy:
            shutil.copy2(file, devFolder)
        #Moving the text file into the temporary directory, preserving any metadata
        shutil.move(file, TMP_DIR)
    #END FOR
    return len(filesToParse)
#END DEF


def _makeDateCSVs(CSV_DIR, csvGener):
    """This will create all of the Date specific CSVs, based on the files in csvGener"""
    #This loop will continue while there are elements in the original csvGenerator
    for DATE in csvGener.fileDates:
        #We first make a new, temporary csvGenerator
        newGen = csvGenerator(sys.argv[1],
                              FileParserPath=os.path.join(os.getcwd(),
                                                          os.path.dirname(__file__),
                                                          "PyFiles"))
        newGen.setOpts( ' '.join([str(item) for item in csvGener.optsChosen]) )
        OBJECTS = csvGener.getAllWithDate(DATE)
        if OBJECTS:
            for obj in OBJECTS:
                newGen._pushObject(obj)
            dateCSV = os.path.join(CSV_DIR, DATE.replace("/","_")+"_results.csv")
            newGen.importCSV(dateCSV, 'date')
            newGen.exportCSV('date', dateCSV)
    #END FOR
    return True
#END DEF


def _makeBaseCSVs(CSV_DIR, csvGener):
    """."""
    #Creating a datetime object
    nowTime = datetime.datetime.now()
    __, nowWeek, __ = nowTime.isocalendar()

    #Setting the location of the -DAILY- CSV file
    dailyCSV = os.path.join(CSV_DIR,"{}_daily_results.csv".format(nowTime.strftime("%m_%d_%Y")))
    #Setting the location of the 'all_test_results' CSV file
    allCSV = os.path.join(CSV_DIR,"all_test_results.csv")

    print("Creating Daily and 'all_test_results' CSVs...")
    csvGener.importCSV(dailyCSV, 'daily')
    csvGener.exportCSV('daily', dailyCSV)
    csvGener.importCSV(allCSV, 'all')
    erroredFiles = csvGener.exportCSV('all', allCSV)
    for file in erroredFiles:
        print(" ERROR when extracting from '{}'".format(file), file=sys.stderr)
    return True
#END DEF






@__debug(logFileLOCATION, ADMIN, fullDebug=True, funcName="Sort And Extract")
@__checkSysArg
def main(**kwargs):
    """Sorts, archives, and parses incoming results files"""
    #This sets the variables holding the paths to the folders we will need
    if sys.argv[1] == 'fieldtest':
        parser = FieldTest_File
    elif sys.argv[1] == 'crowdsource':
        parser = CrowdSource_File
    #END IF/ELIF

    (BASEDIR, UPL_DIR, PAR_DIR,
     TMP_DIR, ERR_DIR, CSV_DIR,
     ARC_DIR, CSA_DIR, DAT_DIR,
     BKP_DIR) = kwargs['folderPaths']

    #Calling the function that sorts and archives new files
    nowTime = datetime.datetime.now()
    numFound = _find(BASEDIR, UPL_DIR, TMP_DIR, nowTime)

    if numFound != 0:
        CSV_GEN = csvGenerator(sys.argv[1],
                               FileParserPath=os.path.join(os.getcwd(),
                                                           os.path.dirname(__file__),
                                                           "PyFiles") )
        (numPar, numErr, ERRORS) = CSV_GEN.pushAllFiles(TMP_DIR,
                                                        ArchiveDirectory=PAR_DIR,
                                                        ErrorDirectory=ERR_DIR)
        if numPar > 0:
            CSV_GEN.setOpts("1 2 3 4 5 6 7 8 10 11")
            _makeBaseCSVs(CSV_DIR, CSV_GEN)
            #_makeDateCSVs(CSV_DIR, CSV_GEN)
            shutil.rmtree(TMP_DIR)
        else:
            print("No files could be processed.")
            shutil.rmtree(TMP_DIR)
    else:
        print("No files found to process.")
        shutil.rmtree(TMP_DIR)
    #END IF/ELSE

    print("Operations completed. Now exitting...")
#END MAIN

if __name__=="__main__":
    main()

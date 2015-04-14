#!/usr/local/bin/python3
"""
------------------------------------------------------------------------
FIND_AND_SCP.PY

AUTHOR(S):     Peter Walker    pwalker@csumb.edu

PURPOSE-    .
FUNCTIONS
    .
------------------------------------------------------------------------
"""

#IMPORTS
import os
import sys
import shutil
import datetime
from _decorators import (__debug, __checkSysArg,
                         logFileLOCATION, ADMIN)
projectPath = os.path.join(os.getcwd(),os.path.dirname(__file__))
if projectPath not in sys.path:
    sys.path.append(projectPath)
from PyFiles.moduleWrappers.scpHACK import (getFile, putFile)
from _sensitiveInfo.scpInfo import (SVR_ADDR, SVR_USER, SVR_PASS,
                                    SVR_localLoc, SVR_hostLoc)
#END IMPORTS

#Checking that this script is being run by at least Python 3
major, *other = sys.version_info
if major<3:
    raise SystemExit("You must be running at least Python 3")




@__debug(logFileLOCATION, ADMIN, funcName="Find CSV and SCP")
@__checkSysArg
def main(**kwargs):
    """Sends either Daily and/or Weekly CSV"""
    #This sets the variables holding the paths to the folders we will need
    (BASEDIR, UPL_DIR, PAR_DIR,
     TMP_DIR, ERR_DIR, CSV_DIR,
     ARC_DIR, CSA_DIR, DAT_DIR,
     BKP_DIR) = kwargs['folderPaths']
    os.rmdir(TMP_DIR)

    #Getting the current time for use in generating CSV paths
    nowTime = datetime.datetime.now()

    #This IF block will run if the day is Sunday. And the only way we are here is
    # if the hour is 11:20 pm
    if nowTime.weekday() == 6:
        print("Copying 'all_test_results' to {}".format(SVR_hostLoc))
        allCSV = os.path.join(CSV_DIR, "all_test_results.csv")
        allCSVcopy = os.path.join(CSV_DIR, "all_test_results_by_{}.csv".format(nowTime.strftime("%m-%d-%y")))
        shutil.copy2(allCSV, allCSVcopy)
        wasSent = putFile(fromPath=allCSVcopy, toPath=SVR_hostLoc,
                          SVR_ADDR=SVR_ADDR, SVR_USER=SVR_USER, SVR_PASS=SVR_PASS)
        if wasSent:
            os.remove(allCSVcopy)
    else:
        print("Copying Daily CSV results to {}".format(SVR_hostLoc))
        dailyCSV = os.path.join(CSV_DIR,"{}_daily_results.csv".format(nowTime.strftime("%m_%d_%Y")))
        wasSent = putFile(fromPath=dailyCSV, toPath=SVR_hostLoc,
                          SVR_ADDR=SVR_ADDR, SVR_USER=SVR_USER, SVR_PASS=SVR_PASS)
        if wasSent:
            os.remove(dailyCSV)
    #END IF/ELSE

    print("Operations completed. Now exitting...")
#END MAIN

if __name__=="__main__":
    main()

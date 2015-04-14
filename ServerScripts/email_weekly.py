#!/usr/local/bin/python3
"""
------------------------------------------------------------------------
EMAIL_WEEKLY.PY

AUTHOR(S):     Peter Walker    pwalker@csumb.edu

PURPOSE-    At 11:20pm, an email is sent with a CSV attached.
            This script will be run every Sunday. It copies the 'all_test_results'
             CSV, and sends it to the CPUC, and CC's the necessary professors
FUNCTIONS
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
projectPath = os.path.join(os.getcwd(),os.path.dirname(__file__))
if projectPath not in sys.path:
    sys.path.append(projectPath)
from PyFiles.moduleWrappers.EmailClient import EmailClient
from _sensitiveInfo.emailLogin import (EMAIL_USER, EMAIL_PASS)
from _sensitiveInfo.emailLogin import (CPUC1, CPUC2,
                                       CHICO1, CHICO2, CHICO3,
                                       BYUN, ANAND)
from _email_base import (setFieldWeeklyOpts, setCrowdWeeklyOpts, setTestingOpts)
#END IMPORTS

#Checking that this script is being run by at least Python 3
major, *other = sys.version_info
if major<3:
    raise SystemExit("You must be running at least Python 3")
#END CHECKING



@__debug(logFileLOCATION, ADMIN, funcName="Weekly Email")
@__checkSysArg
def main(**kwargs):
    """Sends Weekly CSV"""
    #This sets the variables holding the paths to the folders we will need
    (BASEDIR, UPL_DIR, PAR_DIR,
     TMP_DIR, ERR_DIR, CSV_DIR,
     ARC_DIR, CSA_DIR, DAT_DIR,
     BKP_DIR) = kwargs['folderPaths']
    os.rmdir(TMP_DIR)

    #Now set some of the options for our email client
    print("Sending email...")
    emailClient = EmailClient(username=EMAIL_USER, password=EMAIL_PASS, name="CPUC Server")
    if sys.argv[1] == 'fieldtest':
        emailClient.cfg['name'] = "FieldTest Server"
        setFieldWeeklyOpts(emailClient)
    elif sys.argv[1] == 'crowdsource':
        emailClient.cfg['name'] = "CrowdSource Server"
        setCrowdWeeklyOpts(emailClient)
    #If we are testing this, then we want to take all of the emails out of the recipients list
    if "LOCAL" in sys.argv:
        setTestingOpts(emailClient)

    #Getting the current time for use in generating info
    nowTime = datetime.datetime.now()
    #This block will make a copy of the 'all_test_results' CSV, with the day's date
    # appended to the end
    allCSV = os.path.join(CSV_DIR, "all_test_results.csv")
    allCSVcopy = os.path.join(CSV_DIR, "all_test_results_by_{}.csv".format(nowTime.strftime("%m-%d-%y")))
    shutil.copy2(allCSV, allCSVcopy)
    emailClient.addAttachment(allCSVcopy)

    #Sending the emails, and getting the return boolean
    wasSent = emailClient.send()

    #This IF/ELIF block is to remove the CSVs created after they have been emailed.
    #We are assuming that the emailing worked, and that the files now need to be
    # removed if they exist.
    if wasSent:
        print("Removing weekly CSV...")
        os.remove(allCSVcopy)
    #END IF

    print("Operations completed. Now exitting...")
#END MAIN

if __name__=="__main__":
    main()

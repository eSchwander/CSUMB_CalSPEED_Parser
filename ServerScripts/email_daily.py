#!/usr/local/bin/python3
"""
------------------------------------------------------------------------
EMAIL_DAILY.PY

AUTHOR(S):     Peter Walker    pwalker@csumb.edu

PURPOSE-    At 11:20pm every day, an email is sent with a CSV attached. The
             email is only sent to ADMIN and ANAND, and contains the daily CSV.
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
from _email_base import (setFieldDailyOpts, setCrowdDailyOpts, setTestingOpts)
#END IMPORTS

#Checking that this script is being run by at least Python 3
major, *other = sys.version_info
if major<3:
    raise SystemExit("You must be running at least Python 3")
#END CHECKING



@__debug(logFileLOCATION, ADMIN, funcName="Daily Email")
@__checkSysArg
def main(**kwargs):
    """Sends Daily CSV"""
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
        setFieldDailyOpts(emailClient)
    elif sys.argv[1] == 'crowdsource':
        emailClient.cfg['name'] = "CrowdSource Server"
        setCrowdDailyOpts(emailClient)
    #If we are testing this, then we want to take all of the emails out of the recipients list
    if "LOCAL" in sys.argv:
        setTestingOpts(emailClient)

    #Getting the current time for use in generating info
    nowTime = datetime.datetime.now()
    #Getting the location of the daily CSV
    dailyCSV = os.path.join(CSV_DIR,"{}_daily_results.csv".format(nowTime.strftime("%m_%d_%Y")))
    emailClient.addAttachment(dailyCSV)

    #Sending the emails, and getting the return boolean
    wasSent = emailClient.send()

    #This IF block checks that the email was sent. If so, then we can archive the
    # daily results CSV
    if wasSent:
        print("Archiving daily CSV...")
        shutil.move(dailyCSV, CSA_DIR)
    #END IF

    #This bit is a little hardcoded, and is meant only to be run on the Crowd Source server
    if "-gic-cp" in sys.argv:
        location = "/home/gicdata1/DailyUpdate"
        try:
            shutil.copy2(dailyCSV, location)
        except:
            print("Unable to copy daily CSV to location.\n"+
                  "File: {}\n".format(dailyCSV)+
                  "Folder: {}\n".format(location),file=sys.stderr)
    #END IF

    print("Operations completed. Now exitting...")
#END MAIN

if __name__=="__main__":
    main()

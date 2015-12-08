#!/usr/local/bin/python3
"""
------------------------------------------------------------------------
_DECORATORS.PY

AUTHOR(S):     Peter Walker    pwalker@csumb.edu

PURPOSE-  This scripts contains a number of decorator functions that
            will be used by other server scripts.
FUNCTIONS
    __debug
    __checkSysArg
------------------------------------------------------------------------
"""

#IMPORTS
import os
import sys
import datetime
import traceback
from _commonFilePaths import (_generateFieldTestPaths,
                              _generateCrowdSourcePaths,
                              _generateTestingPaths)
projectPath = os.path.join(os.getcwd(),os.path.dirname(__file__))
if projectPath not in sys.path:
    sys.path.append(projectPath)
from PyFiles.moduleWrappers.EmailClient import EmailClient
from _sensitiveInfo.emailLogin import (EMAIL_USER, EMAIL_PASS)
#END IMPORTS

logFileLOCATION = os.path.dirname(os.path.abspath(os.path.join(os.getcwd(),__file__)))

_sendEmail = True
if "NO EMAILS" in sys.argv:
    _sendEmail = False



def __debug(logFileLoc, emailAddress, fullDebug=False, funcName=""):
    """A Wrapper that will call the function and pipe output to a log."""
    logFile = os.path.abspath(os.path.join(logFileLoc, "_ERRORLOG.txt"))
    if len(sys.argv):
        serverName = "{} Server".format(sys.argv[1].upper())
    else:
        serverName = "A Server"
    #END IF/ELSE

    #Instantiating the object that will send the debug email
    ec = EmailClient(username=EMAIL_USER, password=EMAIL_PASS, name="CPUC Server")
    ec.addRecipient(emailAddress)

    def debug_pre_wrap(func):
        """Base function for wrapping"""
        def debug_wrapper(*args, **kwargs):
            """Actual debug wrapper. Puts function in try/except, and puts output into file."""
            #Getting the previous output, for later comparison
            if os.path.isfile(logFile):
                with open(logFile) as fs:
                    oldOut = fs.read()
            else:
                oldOut = ""
            #Setting the time of when the function was run, and redirecting
            # the standard output and standard error output into the log file
            fs = open(logFile,"w")
            sys.stdout = fs
            sys.stderr = fs
            #Running the function in a try/except block
            try:
                #We first try calling the function
                func(*args, **kwargs)
            except:
                #Print out the error to the console and error log
                traceback.print_exc(file=sys.__stdout__)
                traceback.print_exc()
                #Change the standard out and standard error back to the original files
                sys.stdout = sys.__stdout__
                sys.stderr = sys.__stderr__
                fs.close()
                #We then email the log file to the address in 'emailAddress',
                # for debugging, but only if the variable _sendEmail is True
                if _sendEmail:
                    print("Sending {} ERROR file...".format(funcName))
                    timeOfError = datetime.datetime.now().isoformat(' ')
                    ec.addAttachment(logFile)
                    ec.SUBJECT = "ERROR ENCOUNTERED - {}".format(serverName)
                    ec.MESSAGE = ("Error encountered. Error Log file included.\n" +
                                  "TIME=' {} '".format(timeOfError) +
                                  "Log file location: {}\n\n".format(logFile) +
                                  "{}".format(traceback.format_exc())
                                  )
                    ec.send()
                #END IF SEND
                print("Exception Handled...")
            else:
                print(datetime.datetime.now())
                sys.stdout = sys.__stdout__
                sys.stderr = sys.__stderr__
                fs.close()
                #Getting the new output, which we will compare to the old output
                with open(logFile) as fs:
                    newOut = fs.read()
                #If the output is different from the previous hours, email it to the given address
                if newOut != oldOut \
                        and "No files found to process." not in newOut \
                        and fullDebug:
                    #We then email the log file to 'emailAddress', for debugging
                    if _sendEmail:
                        print("Sending {} DEBUG file...".format(funcName))
                        timeOfError = datetime.datetime.now().isoformat(' ')
                        ec.addAttachment(logFile)
                        ec.SUBJECT = "Recent Output - {}".format(serverName)
                        ec.MESSAGE = ("Script complete. Log file included.\n" +
                                      "TIME=' {} '".format(timeOfError)
                                      )
                        ec.send()
                    #END IF SEND
                #END IF
                print("Function completed without error")
            #END TRY/EXCEPT/ELSE
            print("Now exiting debug wrapper...")
        #END DEF
        return debug_wrapper
    return debug_pre_wrap
#END DEF


def __checkSysArg(func):
    """Wrapper function for checking that 'field' or 'crowd' was passed in"""
    def checkSysArgWrapper(*args, **kwargs):
        assert (len(sys.argv)>1
                ),("Too few system arguements. "+
                   "You must pass in another system argument for this script to run.")
        sys.argv[1] = sys.argv[1].lower()
        assert (sys.argv[1] in ['fieldtest', 'crowdsource']
                ),("You must pass in what kind of file will be parsed, 'FieldTest' or 'CrowdSource'.\n"+
                   "Was given '{}'".format(sys.argv[1]))

        #This set some variables that we will be using later, depending on whether we are
        # parsing Field Test files, or Crowd Source files
        if sys.argv[1] == "fieldtest":
            kwargs['folderPaths'] = _generateFieldTestPaths()
        elif sys.argv[1] == "crowdsource":
            kwargs['folderPaths'] = _generateCrowdSourcePaths()
        #END IF/ELSE

        if 'LOCAL' in sys.argv:
            kwargs['folderPaths'] = _generateTestingPaths("/Users/peterwalker/Desktop/rebatch")

        (BASEDIR, UPL_DIR, PAR_DIR,
         TMP_DIR, ERR_DIR, CSV_DIR,
         ARC_DIR, CSA_DIR, DAT_DIR, BKP_DIR) = kwargs['folderPaths']

        #Checking that the UploadData directory exists
        if not os.path.isdir(UPL_DIR):
            raise RuntimeError("The 'UploadData' directory must exist to run this script.\n"+
                               "Currently have '{}'".format(UPL_DIR))

        #Making sure that each folder above is created, and creating it if it is not
        for path in [UPL_DIR, PAR_DIR, TMP_DIR, ERR_DIR,
                     CSV_DIR, ARC_DIR, CSA_DIR, DAT_DIR, BKP_DIR]:
            if not os.path.isdir(path):
                os.makedirs(path)
        #END FOR

        return func(*args, **kwargs)
    #END DEF
    return checkSysArgWrapper
#END DEF

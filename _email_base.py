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
projectPath = os.path.join(os.getcwd(),os.path.dirname(__file__))
if projectPath not in sys.path:
    sys.path.append(projectPath)
from _sensitiveInfo.emailLogin import (ADMIN,
                                       CPUC1, CPUC2,
                                       CHICO1, CHICO2, CHICO3,
                                       BYUN, ANAND)
#END IMPORTS

#Checking that this script is being run by at least Python 3
major, *other = sys.version_info
if major<3:
    raise SystemExit("You must be running at least Python 3")
#END CHECKING


#The functions below provide the message, subject line, and recipients for each
# kind of email, be it from the Crowd Source or Field Test server, a daily or
# weekly email
def setCrowdDailyOpts(eC):
    """."""
    #Getting the current time for use in generating info
    nowTime = datetime.datetime.now()
    #Setting the message content, and sending the message
    eC.SUBJECT = "CPUC Crowd Source Results - {}".format(nowTime.strftime("%b %d, %Y"))
    eC.MESSAGE = ("This is the daily report for the CPUC Crowd Source results.\n"+
                  "Attached are all test results uploaded on {}.\n\n".format(nowTime.strftime("%b %d, %Y"))
                  )
    #eC.addRecipient(ANAND, field='To')
    eC.addRecipient(ADMIN, field='To')
    return True
#END DEF


def setFieldDailyOpts(eC):
    """."""
    #Getting the current time for use in generating info
    nowTime = datetime.datetime.now()
    #Setting the message content, and sending the message
    eC.SUBJECT = "CPUC Field Test Results - {}".format(nowTime.strftime("%b %d, %Y"))
    eC.MESSAGE = ("This is the daily report for the CPUC Field Test results.\n"+
                  "Attached are all test results uploaded on {}.\n\n".format(nowTime.strftime("%b %d, %Y"))+
                  "If you have any questions, please contact Anand Seetharam at aseetharam@csumb.edu.\n"+
                  "Thank you."
                  )
    eC.addRecipient(CPUC1, field='To')
    eC.addRecipient(CPUC2, field='To')
    eC.addRecipient(CHICO1, field='To')
    eC.addRecipient(CHICO2, field='To')
    eC.addRecipient(CHICO3, field='To')
    eC.addRecipient(BYUN, field='Cc')
    eC.addRecipient(ANAND, field='Cc')
    eC.addRecipient(ADMIN, field='Bcc')
    return True
#END DEF


def setCrowdWeeklyOpts(eC):
    """."""
    #Getting the current time for use in generating info
    nowTime = datetime.datetime.now()
    #Setting the message content, and sending the message
    eC.SUBJECT = "CPUC Crowd Source Results - {}".format(nowTime.strftime("%b %d, %Y"))
    eC.MESSAGE = ("Hi Rob,\n\n"+
                  "This is the weekly report for the CPUC Crowd Source results.\n"+
                  "Attached are all test results up until {}.\n\n".format(nowTime.strftime("%b %d, %Y"))+
                  "If you have any questions, please contact Anand Seetharam at aseetharam@csumb.edu.\n"+
                  "Thank you.\n\n"+
                  "Best,\n"+
                  "Anand"
                  )
    eC.addRecipient(CPUC1, field='To')
    eC.addRecipient(ANAND, field='Cc')
    eC.addRecipient(BYUN, field='Cc')
    eC.addRecipient(ADMIN, field='Bcc')
    return True
#END DEF


def setFieldWeeklyOpts(eC):
    """."""
    #Getting the current time for use in generating info
    nowTime = datetime.datetime.now()
    #Setting the message content, and sending the message
    eC.SUBJECT = "CPUC Field Test Results - {}".format(nowTime.strftime("%b %d, %Y"))
    eC.MESSAGE = ("This is the weekly report for the CPUC Field Test results.\n"+
                  "Attached are all test results uploaded on {}".format(nowTime.strftime("%b %d, %Y"))+
                  " since the beginnning of the Field Test.\n\n"+
                  "If you have any questions, please contact Anand Seetharam at aseetharam@csumb.edu.\n"+
                  "Thank you."
                  )
    eC.addRecipient(CPUC1, field='To')
    eC.addRecipient(CPUC2, field='To')
    eC.addRecipient(CHICO1, field='To')
    eC.addRecipient(CHICO2, field='To')
    eC.addRecipient(CHICO3, field='To')
    eC.addRecipient(BYUN, field='Cc')
    eC.addRecipient(ANAND, field='Cc')
    eC.addRecipient(ADMIN, field='Bcc')
    return True
#END DEF


def setTestingOpts(eC):
    """."""
    eC.MESSAGE = (eC.MESSAGE + "\n\n"
                  "Intended TO recipients: " +
                  " ".join( [repr(elem) for elem in eC.recipients['To']] ) + "\n" +
                  "Intended CC recipients: " +
                  " ".join( [repr(elem) for elem in eC.recipients['Cc']] ) + "\n" +
                  "Intended BCC recipients: " +
                  " ".join( [repr(elem) for elem in eC.recipients['Bcc']] ) )
    eC.removeAllRecipients()
    eC.addRecipient(ADMIN, field='To')
    return True
#END DEF

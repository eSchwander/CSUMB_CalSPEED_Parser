#!/bin/bash
##
# A script to automatically generate CSV file every hour.

TMP_HOME=/home/crowduser/
UPLOADS=$TMP_HOME/UploadData
NEW_HOME=/home/crowduser/Byun_Parsing/
NEW_UPLOADS=$NEW_HOME/UploadData

##########################################################################
# Change directory to the home
##########################################################################
cd $TMP_HOME

# ++++++++++++
# ------------------------------------------------------------------------
# Also copy iPerf test results (*.txt) that are older than 45 minutes
# to UploadData directory in Byun_Parsing
# ------------------------------------------------------------------------
find $UPLOADS -type f -name "*.txt"  -mmin +45 | xargs -I files cp -fp files $NEW_UPLOADS
echo ""
echo "Copy test result files (*.txt) to $NEW_UPLOADS"
chown crowduser $NEW_UPLOADS/*
# ++++++++++++



# ++++++++++++ TEMPORARY
# ------------------------------------------------------------------------
# Also copy iPerf test results (*.txt) that are older than 45 minutes
# to UploadData directory in our home folder. This is in case the script
# is having issues, and we don't want files to sit in UploadData
# ------------------------------------------------------------------------
#find $UPLOADS -type f -name "*.txt"  -mmin +45 | xargs -I files mv -f files $TMP_HOME/TEMP/
#echo ""
#echo "MOVE to temp folder"
#chown crowduser $TMP_HOME/TEMP/*
# ++++++++++++

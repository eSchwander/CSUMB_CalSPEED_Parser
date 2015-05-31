#!/bin/bash
##
# A script to automatically generate CSV file every hour.

TMP_HOME=/home/WirelessBBDTester/
UPLOADS=$TMP_HOME/UploadData
RAW_DIR=$TMP_HOME/raw_data
EXTRACT_SH=$TMP_HOME/commands/cpuc_extract.sh
PETER_TESTING=$TMP_HOME/dev_peter/

##########################################################################
# Change directory to the home
##########################################################################
cd $TMP_HOME


##########################################################################
# Creates a temporary WORK_DIR
##########################################################################
hhmm=`date +%H_%M`
WORK_DIR=`echo "$TMP_HOME/work_$hhmm"`
mkdir $WORK_DIR
echo ""
echo "mkdir $WORK_DIR"


##########################################################################
# Copy iPerf test results (*.txt) that are older than one hour
# to "work_hh_mm" subdirectory
##########################################################################
find $UPLOADS -type f -name "*.txt"  -mmin +60 | xargs -I files cp -fp files $WORK_DIR
echo ""
echo "Copy test result files (*.txt) to $WORK_DIR"


# ++++++++++++
# ------------------------------------------------------------------------
# Also copy iPerf test results (*.txt) that are older than one hour
# to UploadData directory in Peter_Field_Testing
# ------------------------------------------------------------------------
find $UPLOADS -type f -name "*.txt"  -mmin +60 | xargs -I files cp -fp files $PETER_TESTING/UploadData
echo ""
echo "Copy test result files (*.txt) to $PETER_TESTING/UploadData"
# ++++++++++++


##########################################################################
# Move all files (including glasnost results (*.log)) that are
# older than one hour to "raw_data" subdirectory
##########################################################################
find $UPLOADS -type f -mmin +60 | xargs -I files mv -f files $RAW_DIR
echo ""
echo "Move all files to $RAW_DIR"


##########################################################################
# Run the extract shell script to generate CSV results for
# the files under WORK_DIR
# If there's no file on the work directory, do not run the extract script.
##########################################################################
num=0
num=`ls -l $WORK_DIR/*.txt 2> /dev/null | wc -l`
if [ $num -ne 0 ]
then
    cd $WORK_DIR
    echo ""
    echo "Run Extract Scripts"
    /bin/bash $EXTRACT_SH 3000 $WORK_DIR/*.txt
    cd $TMP_HOME
else
    echo ""
    echo "No new test result to process at the moment."
fi


##########################################################################
# Delete the "work_hh_mm" directory.
##########################################################################
/bin/rm -f $WORK_DIR/*
/bin/rmdir $WORK_DIR
echo ""
echo "/bin/rm -f $WORK_DIR/*"
echo "/bin/rmdir $WORK_DIR"

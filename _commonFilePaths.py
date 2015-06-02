#!/usr/local/bin/python3
"""
------------------------------------------------------------------------
_COMMON FILE PATHS.PY

AUTHOR(S):     Peter Walker    pwalker@csumb.edu

PURPOSE-  This script simply contains the code that will generate the necessary
            variables that will hold the absolute paths of folder containing
            data, CSV, etc.
------------------------------------------------------------------------
"""

if __name__=="__main__":
    raise SystemExit

#IMPORTS
import os
#END IMPORTS


def _generateFieldTestPaths():
    ## BASEDIR = "/home/WirelessBBDTester/"
    #BASEDIR = "/home/WirelessBBDTester/dev_peter/"
    BASEDIR = os.getcwd()
    return __actualGenerate(BASEDIR)


def _generateCrowdSourcePaths():
    #BASEDIR = "/home/crowduser/"
    ## BASEDIR = "/home/crowduser/dev/"
    BASEDIR = os.getcwd()
    return __actualGenerate(BASEDIR)


def _generateTestingPaths(BASEDIR):
    BASEDIR = BASEDIR
    return __actualGenerate(BASEDIR)


def __actualGenerate(BASEDIR):
    UPL_DIR = os.path.abspath(os.path.join(BASEDIR, "UploadData/other"))
    PAR_DIR = os.path.abspath(os.path.join(BASEDIR, "ProcessedData"))
    TMP_DIR = os.path.abspath(os.path.join(BASEDIR, "TempFiles"))
    ERR_DIR = os.path.abspath(os.path.join(BASEDIR, "ExceptionFiles"))
    CSV_DIR = os.path.abspath(os.path.join(BASEDIR, "csvResults"))
    ARC_DIR = os.path.abspath(os.path.join(BASEDIR, "ARCHIVE"))
    CSA_DIR = os.path.abspath(os.path.join(ARC_DIR, "CSVs_Archive"))
    DAT_DIR = os.path.abspath(os.path.join(ARC_DIR, "DATA_Archive"))
    BKP_DIR = os.path.abspath(os.path.join(BASEDIR, "BACKUPS"))
    return (BASEDIR, UPL_DIR, PAR_DIR,
            TMP_DIR, ERR_DIR, CSV_DIR,
            ARC_DIR, CSA_DIR, DAT_DIR, BKP_DIR)

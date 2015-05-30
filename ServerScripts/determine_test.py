"""
---------------------------------------------------------------------------------------------
determine_test.py

Author:     Evan Schwander  eschwander@csumb.edu

Purpose:    This module is used to determine if an incoming file is a traceroute test or not.
            Depending on what test is found, an apporopriate script is used to parse it.
---------------------------------------------------------------------------------------------
"""


import os
import shutil
import glob

# The following directories need to be created if they don't already exist
if not os.path.exists("./UploadData/other"):
    os.makedirs("./UploadData/other")
if not os.path.exists("./UploadData/tcrt"):
    os.makedirs("./UploadData/tcrt")

# All txt files in UploadData get put into either tcrt or other
for file in glob.glob(os.path.join("./UploadData", '*.txt')):
    fs = open(file, 'r')
    firstline = str(fs.readline())
    fs.close()
    if "traceroute" in firstline.lower():
        shutil.move(file, "./UploadData/tcrt")
    else:
        shutil.move(file, "./UploadData/other")


# Parse tcrt files if there are any
os.system("python parse_all_tcrts.py")

# Parse files in other if there are any
os.system("python sort_and_extract.py fieldtest")

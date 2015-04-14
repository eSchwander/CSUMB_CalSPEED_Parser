#!/usr/local/bin/python3
"""
--------------------------------------------------------------------------------
CSV_UTILS.PY

AUTHOR(S):    Peter Walker    pwalker@csumb.edu

PURPOSE:    Provide a few functions that will be used in multiple modules

FUNCTIONS:
    csvExport
    csvImport
--------------------------------------------------------------------------------
"""
if __name__=="__main__":
    raise SystemExit

from os.path import (abspath, isfile, splitext)


def csvExport(a_2D_Array, fileNameToSave):
    """
    Creates a CSV file from a given 2-dimensional array
    ARGS:
        a_2D_Array:     A 2-dimensional array with each sub array representing a line in the end csv file
        fileNameToSave: The full path of the resulting csv file
    RETURNS:
        A new CSV file saved at given path
    RAISES:
        ValueError - First arg must be a 2-dimensional array. Second arg must be a string
    """
    if not isinstance(a_2D_Array, list) or not isinstance(fileNameToSave, str):
        raise ValueError("You need to pass in a list, and the file name where you would like to save")
    if not fileNameToSave:
        raise ValueError("You need to pass in a legitimate file path through the argument \"fileNameToSave\"")
    if (splitext(fileNameToSave)[-1].lower() != ".csv"):
        fileNameToSave = fileNameToSave+".csv"
    #Open the file into a file write stream
    with open(abspath(fileNameToSave),"w", encoding="utf-8") as fs:
        #For each row of our 2D array, we are going to write the contents of
        # the array, separated by commas
        for row in a_2D_Array:
            rowOfText = ''
            for col in row:
                rowOfText += (str(col).strip() + ',')
            fs.write(rowOfText[:-1]+"\n")
        #END FOR
    #END WITH
    return
#END DEF


def csvImport(fileNameToImport):
    """
    Used to initialize an object of this class
    ARGS:
        fileNameToSave: The full path of the csv file to import
    RETURNS:
        a_2D_Array:     A 2-dimensional array with each sub array representing a line in the csv file
    RAISES:
        ValueError - Arg must be a path ending in .csv
    """
    if not fileNameToImport:
        raise ValueError("You need to pass in a legitimate file path through the argument \"fileNameToImport\"")
    #Making sure that the file is a file
    fileNameToImport = abspath(fileNameToImport)
    if not isfile(fileNameToImport) and (splitext(fileNameToImport)[-1].lower() != ".csv"):
        raise RuntimeError("The argument \"fileNameToImport\" must contain a legitimate CSV file")
    #Initialize an empty array, which will hold the parsed CSV file, and
    # also open the file in a file read stream
    a_2D_Array = []
    with open(fileNameToImport,"r", encoding="utf-8") as fs:
        #We read the first line. If it is a legitimate line (as in, text is read)
        # then we get to continue into the while loop
        line = fs.readline()
        while line:
            a_1D_Array = []
            cols = line.split(",")
            #For each element in our newly read row that has been split by the "," character,
            # we will remove the newline character, the newline+return carriage, and single quotes
            # from the read text. This is the value that will be saved into our new 2D array
            for col in cols:
                a_1D_Array.append(col.replace("\n","").replace("\r","").replace("\"",""))
            #END FOR
            #If the element is a number, then we need to cast it as a number (either int or float)
            for elem in a_1D_Array:
                #We first try a float, because something that is an int cannot be made into
                # a float (like '9'). If that doesn't work, then we try casting the elem as
                # an int. if that doesn't work, then the value must contain characters.
                try:
                    if "." not in elem:
                        a_1D_Array[a_1D_Array.index(elem)] = int(elem)
                    else:
                        a_1D_Array[a_1D_Array.index(elem)] = float(elem)
                except:
                    pass
                #END TRY/EXCEPT
            #END FOR
            a_2D_Array.append(a_1D_Array)
            line = fs.readline()
        #END WHILE
    #END WITH
    return a_2D_Array
#END DEF

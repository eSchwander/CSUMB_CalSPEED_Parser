#!/usr/local/bin/python3
"""
------------------------------------------------------------------------
_CSV APPENDER.PY

AUTHOR(S):     Peter Walker    pwalker@csumb.edu

PURPOSE-  This script will either ask the user for a directory containing
            network test output files (Field Test or Crowd Source), or will
            use the directory provided in the sys.argv array. It will also use
            a CSV file, specified by the user or in sys.argv. It will parse all
            of the files, then add the requested information to the given CSV.

FUNCTIONS:
    appendToCSV
    __main__
------------------------------------------------------------------------
"""

from _csvCommonFuncs_ import parseAllTests


def appendToCSV(folderPath, csvPath, outputFilename="./_result.csv", options="", *args, **kwargs):
    """
    Given the folder that contains the raw data, the CSV to be
    appending to, and a few other options, this function will pass
    every file to the FieldTest_File constructor, store the object,
    and then iterate through every File object, creating a line in
    the CSV from it's values. The user can chose which values should
    be calculated from each File object
    ARGS:
        folderPath      String, the absolute path the folder containing the raw data
        csvPath         String, the absolute path to the original CSV file
        outputFilename  String, the path where the resulting CSV will be saved.
                        Default: ./_result.csv, a CSV in the current directory
        options         String, the option numbers that correspond to which values each
                        line in the CSV should contain.
        NewHeaders      KWARG. Anything. If this is set, then the new CSV headers will be
                        used when finding header/attribute pairs that match
    RETURNS:
        Creates a CSV file at the location in outputFilename
    RAISES:
        ValueError - if folderPath is not a directory, if csvPath is not a CSV file,
                     if PyObject could not be imported
    """
    import os
    import datetime
    import traceback
    #Doing some error checking of the values passed
    #Checking that the folderPath arg contains a value
    if not folderPath or not csvPath:
        raise ValueError("You need to pass in a legitimate folder path through the argument"+
                         "\"folderPath\" or \"csvPath\"")
    #Checking that folderPath is a legitimate directory
    from os.path import (abspath, isdir, isfile)
    folderPath = abspath(folderPath)
    if not isdir(folderPath):
        raise RuntimeError("The argument \"folderPath\" must contain a legitimate directory")
    csvPath = abspath(csvPath)
    if not isfile(csvPath) and (csvPath[-4:].lower() != ".csv"):
        raise RuntimeError("The argument \"csvPath\" must contain a legitimate CSV file")
    #If the file given in outputFilename already exits, warning the user that it will be overwritten.
    # But before that, we need to make sure that the path is the absolute path
    outputFilename = abspath(outputFilename)
    if isfile(outputFilename):
        print("This script will overwrite the contents in \""+
              os.path.basename(outputFilename)+"\".\n"+
              "Do you wish to continue? (y/n)")
        ans = str(input(">>> ")).lower()
        if ans != "y":
            print("Now exiting...")
            raise SystemExit
    #Checking that the arg options is a string
    if not isinstance(options, str):
        raise ValueError("The argument \"options\" must be a string.")
    #Trying to import the fileType object. If unsuccessful, then we exit
    try:
        from FileParser.FieldTest_File import FieldTest_File as outputFile
    except:
        raise RuntimeError("Was unable to import the necessary files for parsing")
    #END TRY/EXCEPT

    #Importing a function from Parser.utils that will let us export the 2 dimensional array
    # that will be created as a CSV file. Also, importing some other statistical functions
    from Parser.utils.basic_utils import csvImport, csvExport
    #Importing our headers based on the type of raw files being used
    from _csvHeaders_ import FieldTestHeaders as headers
    from _csvHeaders_ import FTcsvHeadersOrder as headersOrder

    #Asking the user which kind of values they want in their csv if the script is being
    # run as main, and only the default options are currently chosen.
    if (options == ""):
        print("Please input on one line which values you would like included in the CSV:\n" +
              " example: >>> 13\n\n" +
              " a - All Headers, specified below\n")

        for hdr in headersOrder[5:]:
            print(" "+str(headersOrder.index(hdr)-4)+" - "+hdr[4:])
            if len(headers[hdr])>10:
                half = int(len(headers[hdr])/2)
                print("       "+" ".join(headers[hdr][:half])+"\n"+
                      "       "+" ".join(headers[hdr][half:]))
            else:
                print("       "+" ".join(headers[hdr]))
            #END FOR
        #END FOR
        #Asking for options
        options = str(input(">>> "))
        print()
    #END IF

    #Creating the array that will hold all of the column headers for this CSV
    csvHeaders = []
    #If the user chose all options, then we redeclare options to include all of the option numbers
    if "a" in options:
        options = "".join([str((headersOrder.index(elem)-4)) for elem in headersOrder[5:]])
    #Depending on what numbers the user inputed at the terminal, we will append
    # the headers values to our csvHeader array
    possibleOpts = [(headersOrder.index(elem)-4) for elem in headersOrder[5:]]
    for ind in possibleOpts:
        if str(ind) in options:
            csvHeaders.extend(headers[headersOrder[ind+4]])

    #Now we will parse all of the files in the folder specified in folderPath, and then
    # create the CSV at the location specified in outputFilename
    startTime = datetime.datetime.now()
    parsedFiles = parseAllTests('fieldtest', folderPath, outputFilename, startTime)

    #Importing our csv as an array, which we will be searching through to find
    # the correct row to append values to
    print("Importing CSV from "+csvPath)
    csvAsArray = csvImport(csvPath)
    oldRowLength = len(csvAsArray[0])

    #Now that we've found a path that has not been used, we can print out all of the test
    # into it for error checking
    print("CSV File being created...")
    for file in parsedFiles:
        fileAsArray = []
        #We first split the options chosen into individual elements
        for option in list(options):
            #If the option is a number and is less than 4, then we can use it
            if option.isnumeric() and int(option)<(len(headersOrder)-4):
                #We first get the header of the option chosen
                # eg. 1 => 1+4 => headersOrder[5] => "csv Stat Headers"
                # We then grab just the middle word from the string for use
                hdr = headersOrder[int(option)+4]
                hdrType = hdr.split(" ")[1]

                ## !!!! HACK for old Column Order
                #We are going to get the function that need to be called, call the
                # function, and then re-order the array as necessary
                array = getattr(file, "get_csv"+hdrType+"Values")()
                if hdrType == "Stat" or hdrType == "Qual":
                    array = array[:4] + array[8:12] + array[4:8] + array[12:]
                elif hdrType == "RvMos":
                    array = array[2:] + array[:2]
                #END IF/ELIFs
                fileAsArray.extend(array)
                ## !!!! END HACK

                #getValues = getattr(file, "get_csv"+hdrType+"Values")
                #fileAsArray.extend(getValues())
            #END IF
        #END FOR

        #The CSV headers have recently changed, but if the CSV is using
        # the new headers, set 'NewHeaders' to anything
        try:
            if kwargs["NewHeaders"] is not None:
                pairs=[("Date","Date"), ("Time","Time"),
                       ("LocationID", "LocationID"),
                       ("DeviceID", "DeviceID")]
            else:
                pairs=[("Date","Date"), ("Time","Time"),
                       ("Location_ID", "LocationID"),
                       ("Device ID", "DeviceID")]
            #END IF/ELSE
        except:
            pairs=[("Date","Date"), ("Time","Time"),
                   ("Location_ID", "LocationID"),
                   ("Device ID", "DeviceID")]
        #END TRY/EXCEPT
        #Now we will want to search for the array that matches our file. What we
        # do is get all of the rows that have the right Date and Time. From those,
        # we search for the one with the correct Location ID. If there are still
        # multiple, then we search for the right Device ID.
        matchingRows = findCSVRows(csvAsArray, file, headerAttrbPairs=pairs[:2])
        added = False
        if matchingRows:
            numFields = 3
            while True:
                toSearch = [csvAsArray[0][:]]
                toSearch.extend(matchingRows)
                if len(toSearch)<2 or numFields>len(pairs):
                    break
                elif len(toSearch) == 2:
                    added = True
                    toSearch[1].extend(fileAsArray)
                    break
                else:
                    matchingRows = findCSVRows(csvAsArray, file,
                                               headerAttrbPairs=pairs[:numFields])
                    numFields += 1
                #END IF/ELIF/ELSE
        #If the file was not added, then create a file containing all of the
        # file names that were not added.
        if not added:
            with open(os.path.join(os.path.expanduser("~"), "Desktop", "missingFiles.txt"), "a") as fs:
                fs.write(folderPath.split("/")[-1]+"   "+file.Filename+"\n")
        #END IF

        #Printing out how long the script has been running
        timeDiff = datetime.datetime.now() - startTime
        timeDiff_str = str(timeDiff).split(".")[0]
        print("  Current Run Time: "+timeDiff_str, end='\r')
    #END FOR

    #Now we need to put in placeholders for the rows that did not have a file
    filler = ["File Missing"]*len(csvHeaders)
    for row in csvAsArray[1:]:
        if len(row) == oldRowLength:
            row.extend(filler)
    #END FOR
    #Just before we create our CSV from our massive array, we need to append the new
    # headers (in csvHeaders) to the first element
    csvAsArray[0].extend(csvHeaders)
    #Creating the csv with the csvExport function from Parser.utils.basic_utils
    csvExport(csvAsArray, outputFilename)
    #Printing an empty line after the CSV has been created,
    # so to clear the "Current Run Time:" text
    print(" "*50, end='\r')
    print("CSV File has been created.")
#END DEF


def findCSVRows(csvAsArray, parsedFile, headerAttrbPairs=[], *args, **kwargs):
    """
    This function will take a given CSV, and find the row that
    corresponds to the given parsed file object. The function takes pairs
    of CSV headers and file attributes, and will find all of the rows where
    the CSV columns match all of the file's attributes.
    ARGS:
        csvAsArray      A 2-dimensional array, representing the CSV
        parsedFile      _File object, representing the file whose line we are
                        looking for in the CSV
        headerAttrbPairs
                        KWARGS. Each key represents the column that we will be
                        looking in, while the value associated with that key is
                        the value we are looking for in the column. The row
                        must contain all header/value pairs in order to be
                        returned
    RETURNS:
        List of Arrays, where each array is a row in the CSV where the information
        matched what was given
    """
    if not isinstance(csvAsArray, list) or not isinstance(headerAttrbPairs, list):
        raise ValueError("You need to pass in a list through the arguments"+
                         "\"csvAsArray\" and \"headerAttrbPairs\"")
    #This will loop through all of the pairs in headerAttrbPairs, checking that
    # all of the headers and attributes exist in the CSV and parsed file object
    for header, attr in headerAttrbPairs:
        #This is raising an error if 'header' is not only of the column
        # headers in the CSV
        if header not in csvAsArray[0]:
            raise ValueError(header+" is not a header in the CSV file")
        #This will raise an AttributeError if 'attr' is not an attribute of parsedFile
        __ = getattr(parsedFile, attr)
    #END FOR
    #Making a reference to the CSV headers, and then creating an empty arry (for where
    # the matching rows will go). I am renaming tempHeaders to csvHeaders because I want to
    csvHeaders = csvAsArray[0]
    matchingRows = []
    for row in csvAsArray[1:]:
        matching = True
        #For each row, we want to make sure that all of the headers/attribute pairs
        # match the. Then we will add that row to the array 'matchingRows'
        for header, attr in headerAttrbPairs:
            #We need to use 'in' because, sometimes, there is whitespace in the CSV, and this will
            # get us around that, while still finding the row where the information matches
            if ( str(getattr(parsedFile, attr)) not in str(row[csvHeaders.index(header)])
                 and str(getattr(parsedFile, attr)) != str(row[csvHeaders.index(header)]) ):
                matching = False
        #END FOR
        if matching:
            matchingRows.append(row)
    #END FOR
    return matchingRows
#END DEF



## -----------------------------------------------------------------------------

#MAIN
if __name__ == "__main__":
    """
    This script can be run as __main__ by a user. If they do not give the necessary
    inputs from the comamnd line, then tkinter will ask for the locations of
    files and folder.
    __main__ then calls appendToCSV() with the necessary arguments
    """
    #IMPORTS
    import sys
    import os
    import datetime
    from tkinter.filedialog import (askdirectory, askopenfilename)
    #END IMPORTS
    #Timestamp of the current time
    startingTheScript = datetime.datetime.now()
    #This takes care of the problem of having to run the script from within the
    # folder the contains it. This will dynamically add the project path to Python's
    # sys.path array.
    #We combine the current directory with the path in __file__, get the absolute path
    # of that join, and then remove the script name from the end. That end string is
    # then appended to sys.path
    sys.path.append( os.path.abspath(os.path.join(os.getcwd(), __file__)).rsplit("/",1)[0] )
    #If the number of arguments was less than 2, then we will ask the user where the
    # raw data is, and where they want the file saved.
    if ("-h" in sys.argv) or ("--help" in sys.argv):
        print("This script requires at least one flag, and has a few optional inputs:\n"+
              "  -h/--help    Help menu\n"+
              "  -i [path]    The path to the raw data that will be parsed\n"+
              "  -v [path]    The path to the original CSV file we are appending to\n"+
              "  -o [path]    The path where the file will be saved\n"+
              "  --all        Create the csv with all possible columns\n"+
              "Here some possible ways to run this script:\n" +
              "$ py "+(__file__.split("/")[-1])+"\n" +
              "$ py "+(__file__.split("/")[-1])+" -i /path/to/raw_date -v /path/to/csv\n" +
              "$ py "+(__file__.split("/")[-1])+" -i /path/to/raw_data -o /path/to/result.csv\n")
        raise SystemExit
    #END IF

    #These is where we will determine what information has been provided by the user, and
    # what is missing
    RawDataPath = ""
    OriginalCSVPath = ""
    ResultDataPath = ""
    #If the input path was not specified, then we need to ask the user for it's location
    if "-i" not in sys.argv:
        print("Please select the folder containing the raw data you wish to convert into a CSV...")
        RawDataPath = askdirectory( initialdir=os.path.expanduser("~"),
                                    title="Select the FOLDER containing the raw data",
                                    mustexist=True)
    else:
        path = sys.argv[sys.argv.index("-i")+1]
        RawDataPath = os.path.abspath(path)
    #END IF/ELSE
    #If the CSV path was not specified, then we need to ask the user for it's location
    if "-v" not in sys.argv:
        print("Please select the CSV file that will be appended to...")
        OriginalCSVPath = askopenfilename( initialdir=os.path.expanduser("~"),
                                           title="Select the base CSV to append to",
                                           filetypes=[("CSV files", "*.csv")],
                                           multiple=False)
    else:
        path = sys.argv[sys.argv.index("-v")+1]
        OriginalCSVPath = os.path.abspath(path)
    #END IF/ELSE

    #If the user did not specify where to save the output file, then we will
    # ask them which folder they would like the file saved in.
    if "-o" not in sys.argv:
        print("Please select where you would like to save the output...")
        ResultDir = askdirectory( initialdir=os.path.expanduser("~"),
                                  title="Select the FOLDER to hold the new CSV",
                                  mustexist=True)
        ResultDataPath = ResultDir+"/" + RawDataPath.split("/")[-1]+"_results.csv"
    else:
        path = sys.argv[sys.argv.index("-o")+1]
        if ".csv" not in path[-4:]:
            path += ".csv"
        ResultDataPath = os.path.abspath(path)
    #END IF/ELSE

    #If the user used the "--all" flag, then we will run the CSV creator with the
    # 'a' options, which creates the CSV with all of the possible columns included.
    options = ""
    if "--all" in sys.argv:
        options = "a"

    #Now we actually call the function that creates the CSV
    appendToCSV(folderPath=RawDataPath,
                csvPath=OriginalCSVPath,
                outputFilename=ResultDataPath,
                options=options
                )

    #Doing some calculation of how long the script had to run
    timeToRun = datetime.datetime.now() - startingTheScript
    print("The script has completed with a time of: " + str(timeToRun).split(".")[0])
    print("Now exiting...")
    raise SystemExit
#END IF MAIN

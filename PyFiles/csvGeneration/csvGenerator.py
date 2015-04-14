#!/usr/local/bin/python3
"""
--------------------------------------------------------------------------------
__CSV GENERATOR.PY

AUTHOR(S):     Peter Walker    pwalker@csumb.edu

PURPOSE-  The file contains a number of functions that will take a given
            parsed file, and return an array of values that can be
            exported as a CSV
--------------------------------------------------------------------------------
"""

#IMPORTS
import os
import sys
import shutil
import datetime
import traceback
from platform import system
if system()=="Windows":
    import ntpath as path
else:
    import os.path as path
if path.join(os.getcwd(),path.dirname(__file__)) not in sys.path:
    sys.path.append(path.join(os.getcwd(),path.dirname(__file__)))
from _csvUtils.csv_utils import (csvImport, csvExport)
from csvDataExtractor import csvDataExtractor
#END IMPORTS


class csvGenerator(object):

    """
    The purpose of this class is to store a Python list of objects (of data
     files parsed), and use those object to generate CSVs. The actual value
     generation is done in csvDataExtractor, while the managing of CSVs, file
     objects, and other functions are done with this class.

    Initializing this class will require the type of files being passed to it.
    Once the class has been initialized, you can specify which columns you want
     generated through the use of setOpts().

    You must then import CSV files using importCSV(). You then export the CSV
     (which appends the new values in the process) using exportCSV().
     Both functions will take a path (to the original file OR to the requested
     output path) and an index name (for internal bookkeeping).
     You can get a list of indeces that are present by using listCSVs().
    """

    OPTS = {1: "extractDefaultVals",
            2: "extractExtraVals",
            3: "extractPINGVals",
            4: "extractRValMOSVals",
            5: "extractUDPVals",
            6: "extractTCPVals",
            7: "extractTCPStatVals",
            8: "extractTCPStatSVals",
            9: "extractTCPStatAVals",
            10:"extractTCPQualVals"}
    TOTAL_OPTS = len(OPTS)
    FILETYPES = ['fieldtest','crowdsource']


    # CLASS ATTRIBUTES ----------
    # fileType    = ""
    # parsedCount = 0
    # errorCount  = 0
    #
    # parsedFiles = []
    # CSVs        = {}
    #
    # optsChosen  = []
    # hdrOrder    = []
    # csvHdrs     = {}
    #
    # parser      = PARSER CLASS
    # extractor   = CSV DATA EXTRACTOR CLASS


    def __init__(self, fileType='fieldtest', **kwargs):
        """Initializes the CSV Generator object"""
        #Determining if the 'fileType' passed in is one of the possible options
        fileType = fileType.lower()
        if fileType not in self.FILETYPES:
            print("Given data file type, '{}',".format(fileType) +
                  " is not one of the possible options. Defaulting to 'fieldtest'.")
            fileType = self.FILETYPES[0]
        self.fileType = fileType
        #This will hold the number of files correctly and incorrectly parsed
        self.parsedCount = 0
        self.errorCount  = 0
        #This will be a list of parsed file objects, which will later be passed
        # to the extractor
        self.parsedFiles = []
        #This will be a list of strings that are the dates the tests were conducted on
        self.fileDates = []
        self.CSVs = {}

        #Importing the necessary parser based on the specified data file type. We
        # first check if the user gave us a path to that parser
        if "FileParserPath" in kwargs:
            parserPath = kwargs["FileParserPath"]
        else:
            parserPath = "."

        if self.fileType == self.FILETYPES[0]:
            self.__importField(parserPath)
        elif self.fileType == self.FILETYPES[1]:
            self.__importCrowd(parserPath)
        else:
            self.parser = None
        self.__parserClass = self.parser(empty=True).__class__
        self.extractor = csvDataExtractor(self.fileType)
        self.setOpts("ALL")
    #END DEF


    def __importField(self, FileParserPath="."):
        try:
            from FileParser.FieldTest_File import FieldTest_File as parser
        except ImportError:
            try:
                sys.path.append(FileParserPath)
                from FileParser.FieldTest_File import FieldTest_File as parser
            except:
                raise RuntimeError("Something went wrong when instantiating a CSV Generator.")

        from _csvUtils._csvHeaders_ import (FTcsvHeadersOrder, FieldTestHeaders)
        self.__hdrOrder = FTcsvHeadersOrder
        self.csvHdrs = FieldTestHeaders
        self.parser = parser
    #END DEF

    def __importCrowd(self, FileParserPath="."):
        try:
            from FileParser.CrowdSource_File import CrowdSource_File as parser
        except ImportError:
            try:
                sys.path.append(FileParserPath)
                from FileParser.CrowdSource_File import CrowdSource_File as parser
            except:
                raise RuntimeError("Something went wrong when instantiating a CSV Generator.")

        from _csvUtils._csvHeaders_ import (CScsvHeadersOrder, CrowdSourceHeaders)
        self.__hdrOrder = CScsvHeadersOrder
        self.csvHdrs = CrowdSourceHeaders
        self.parser = parser
    #END DEF



# OPTION SETTING (FOR EXPORT) --------------------------------------------------

    def setOpts(self, opts=''):
        """
        This function takes a given string, and sets an array of "options", which
         will dictate what CSV values are extracted.
        ARGS:
            opts    String, numerical values delimited by spaces
        RETURNS:
            Boolean, whether options were set or not
        """
        if not isinstance(opts, str):
            raise ValueError("The options chosen must be passed in as a string. "+
                             "Was given a {}".format(type(opts)))
        #END IF
        if opts=='':
            print("These are your possible CSV options. Please input multiple with spaces...")
            keys = sorted(self.OPTS.keys())
            for OPT in keys:
                print(" {} -  {}".format(OPT, self.OPTS[OPT]))
            opts = input("---> ")
            if self.__setOptions(opts):
                return True
            return False
        elif opts=="ALL":
            self.optsChosen = sorted(self.OPTS.keys())
            self.hdrOrder = self.__hdrOrder
            return True
        else:
            return self.__setOptions(opts)
        #END IF/ELSE
    #END DEF

    def __setOptions(self, input_):
        """."""
        #Checking that the user has given us the necessary options
        if input_.strip()=="":
            return False

        #This removes any pieces that were a string of spaces, or were not numbers
        input_ = [int(op) for op in input_.split(" ") if (op.strip() and op.isdigit())]
        #Checking that we have at least one result left
        if len(input_)<1:
            return False
        #Checking that all of the numbers are within the range of functions we have available
        for op in input_:
            if op>self.TOTAL_OPTS:
                raise ValueError("The options passed in are not within range.\n"+
                                 "Options chosen can be between 1 and {}.\n".format(self.TOTAL_OPTS)+
                                 "Was given {}".format(op))
        #END FOR
        self.optsChosen = sorted(input_)
        self.hdrOrder = [header for header in self.__hdrOrder
                         if (self.__hdrOrder.index(header)+1) in self.optsChosen]
        return True
    #END DEF

    def printOpts(self, stdout_=False):
        """
        Prints the possible CSV generation options that can be chosen, and
         what is currently chosen
        ARGS:
            stdout_     Boolean, whether to print out what options have been chosen
        RETURNS:
            List of options chosen
        """
        #We only want to print out stuff if the user passed in True
        if stdout_:
            #Printing the possible option choices
            print("These are the current possible options:")
            for opt in self.OPTS:
                print("{}:  {}".format(opt, self.OPTS[opt]))
            #Printing the currently chosen options
            print("\nThese are the current options CHOSEN:")
            for opt in self.optsChosen:
                print("{}:  {}".format(opt, self.OPTS[opt]))
        #END IF
        return self.optsChosen
    #END DEF



# PARSING FUNCTIONS ------------------------------------------------------------

    def _pushObject(self, object, index=-1):
        """This is in case one wants to add a parsed file object to the generator"""
        if not isinstance(object, self.__parserClass):
            print("The object was not the correct kind of class. "+
                  "Was given '{}',\n".format(object.__class__)+
                  " should be '{}'".format(self.__parserClass))
            return False
        if index == -1:
            self.parsedFiles.append(object)
        else:
            self.parsedFiles.insert(index, object)
        self.__addDate(object)
        self.parsedCount += 1
        self.parsedFiles.sort()
        return True
    #END DEF


    def pushFile(self, filePath, **kwargs):
        """
        This take the path to a file, runs it through the parser, adding it to self.parsedFiles
        ARGS:
            filePath        String, the location of the file to be parsed
        KWARGS:
            ErrorDirectory      String, the path to the directory that will hold files that cause an error
            ArchiveDirectory    String, the path to the archival directory
        RETURNS:
            Tuple (Boolean, String), Boolean is whether the file was able to be parsed, and
             the String is the path to the file that's been given
        """
        #The value in filePath must be a string
        if not isinstance(filePath, str):
            return (False, "")
        filePath = os.path.abspath(filePath)
        #Checking that the given file path points to a legitimate file
        if not os.path.isfile(filePath):
            return (False, "")
        #Checking that the given file actually has information to read
        with open(filePath) as quickread:
            try:
                __ = quickread.read()
            except:
                self.errorCount += 1
                traceback.print_exception(*sys.exc_info(), file=sys.stderr)
                print("Errored File: {}\n".format(filePath), file=sys.stderr)
                print(" - UNREADABLE: Processed file '{}'".format(filePath))
                #If we have been given an Error Directory, and the directory exists, then
                # we will make a copy of the file that gave us an error, and move it to
                # the given directory
                if 'ErrorDirectory' in kwargs \
                        and isinstance(kwargs['ErrorDirectory'], str) \
                        and os.path.isdir(kwargs['ErrorDirectory']):
                    shutil.copy2(filePath, kwargs['ErrorDirectory'])
                return (False, filePath)
            #END TRY/EXCEPT
        #END WITH
        #Now that we've tested that the file actually has contents, we are going to
        # pass it to our parser.
        parsedFileObj = self.parser(filePath=filePath)
        if parsedFileObj:
            self.parsedCount += 1
            self.parsedFiles.append(parsedFileObj)
            self.__addDate(parsedFileObj)
            if 'ArchiveDirectory' in kwargs \
                    and isinstance(kwargs['ArchiveDirectory'], str) \
                    and os.path.isdir(kwargs['ArchiveDirectory']):
                shutil.copy2(filePath, kwargs['ArchiveDirectory'])
            return (True,"")
        else:
            self.errorCount += 1
            traceback.print_exception(*sys.exc_info(), file=sys.stderr)
            print("Errored File: {}\n".format(filePath), file=sys.stderr)
            #If we have been given an Error Directory, and the directory exists, then
            # we will make a copy of the file that gave us an error, and move it to
            # the given directory
            if 'ErrorDirectory' in kwargs \
                    and isinstance(kwargs['ErrorDirectory'], str) \
                    and os.path.isdir(kwargs['ErrorDirectory']):
                shutil.copy2(filePath, kwargs['ErrorDirectory'])
            return (False, filePath)
        #END IF/ELSE
    #END DEF


    def pushAllFiles(self, folderPath, **kwargs):
        """
        This takes a given folder path, and parses all files found using the parser
         imported in __init__
        ARGS:
            folderPath      String, the path to the folder containing files to parse
        KWARGS:
            ErrorDirectory      String, the path to the directory that will hold files that cause an error
            ArchiveDirectory    String, the path to the archival directory
        RETURNS:
            Tuple (Int_1, Int_2, List), Int_1 is the number of files that have been parsed,
             Int_2 is the number of files that errored, List is the paths to the files that
             caused an error
        """
        erroredFiles = []
        #This will recursively loop through all of the files and folder in the given folder path.
        for root, dirs, files in os.walk(folderPath):
            for aFile in files:
                #Seeing if the file given is, in fact, a data file
                #If not, the script will exit and display the message below
                thisFile = os.path.join(root, aFile)
                #This calls the class function, and if what is returned is not
                # False, then we have
                return_, filePath = self.pushFile(thisFile, **kwargs)
                if not return_ and filePath:
                    erroredFiles.append(filePath)
            #END FOR files
        #END FOR os.walk
        print("{} files processed without error, {} with error.".format(self.parsedCount, self.errorCount))
        self.parsedFiles.sort()
        return (self.parsedCount, self.errorCount, erroredFiles)
    #END DEF


    def _popObject(self, front=False):
        """Removes the parsed data file object from the end of array of parsed files"""
        if len(self.parsedFiles) < 1:
            return None
        self.parsedCount -= 1
        if front:
            return self.parsedFiles.pop(0)
        return self.parsedFiles.pop()
    #END DEF


    def hasObjects(self):
        """Returns a boolean, whether parsedFiles has items or not"""
        if len(self.parsedFiles) > 0:
            return True
        return False
    #END DEF


    def getAllWithDate(self, date):
        """Returns an array of all parsed file objects that were conducted on date passed in 'date'."""
        if date not in self.fileDates:
            return []
        returns = []
        for OBJ in self.parsedFiles:
            if date == OBJ.Date:
                returns.append(OBJ)
        #END FOR
        return returns
    #END DEF


    def __addDate(self, OBJ):
        if OBJ.Date not in self.fileDates:
            self.fileDates.append(OBJ.Date)
            return True
        return False
    #END DEF


# CSV CREATION FUNCTIONS -------------------------------------------------------

    def __createBlankCSV(self, path):
        """
        This will create an 'empty' CSV, which will contain only the CSV headers
        ARGS:
            path    String, the path where to export the CSV file to
        """
        #If the CSV has not been created, then we will start it, and append
        # the headers, making them the first row.
        csv = []
        allHeaders = []
        for elem in self.hdrOrder:
            allHeaders.extend(self.csvHdrs[elem])
        csv.append(allHeaders)
        csvExport(csv, path)
        return True
    #END DEF


    def importCSV(self, path, indexName):
        """
        Imports the CSV at the given path, and stores it in this object's dictionary
         at the 'indexName' index. If the file does not exist, then a new 2-D array
         is created with the necessary file headers.
        ARGS:
            indexName   The value of the index used to identify this CSV with the object
            path        The path to where the CSV is that needs to be imported
        RETURNS:
            Boolean, True on success, False on failure
        """
        path = os.path.abspath(path)
        try:
            if not os.path.isfile(path):
                self.__createBlankCSV(path)
                print("New CSV created at {}.".format(path))
            self.CSVs[indexName] = csvImport(path)
            return True
        except:
            return False
    #END DEF


    def __appendToCSV(self, indexName):
        """Given an index name, appends all parsed files to the indexed CSV"""
        erroredFiles = []
        #If the index given is in self.CSVs, then we can go ahead and get the
        # values we want
        if indexName in self.CSVs:
            #Sorting the parsed files before we append them to the CSV
            self.parsedFiles.sort()
            for parsedFileObj in self.parsedFiles:
                try:
                    ## print(" Extracting from {}".format(parsedFileObj.FilePath))
                    #This is the block that will make the row of values from the
                    # parsed file object.
                    objAsArray = []
                    #For every option chosen by the user, we will get the values by
                    # calling the necessary function from the EXTRACTOR. We get that
                    # function by using the function name in self.OPTS the corresponds
                    # to the number in 'op'.
                    for op in self.optsChosen:
                        VALUES = getattr(self.extractor, self.OPTS[op])(parsedFileObj)
                        objAsArray.extend(VALUES)
                    #Adding the value to the end of the CSV
                    self.CSVs[indexName].append(objAsArray)
                except:
                    print(traceback.format_exc(), file=sys.__stdout__)
                    erroredFiles.append(parsedFileObj.FilePath)
            return erroredFiles
        else:
            return False
    #END DEF


    def exportCSV(self, indexName, path):
        """
        Exports the CSV currently at the given indexName. The CSV will be
         exported to the given path. If the indexName does not exist, then
         nothing is done.
        ARGS:
            indexName   The value of the index used to identify this CSV with the object
            path        The path to where the CSV will be created
        RETURNS:
            Boolean, True on success, False on failure
        """
        path = os.path.abspath(path)
        if indexName in self.CSVs and len(self.parsedFiles)>0:
            erroredFiles = self.__appendToCSV(indexName)
            self.__cleanCSV(self.CSVs[indexName])
            csvExport(self.CSVs[indexName], path)
            self.CSVs.pop(indexName)
            return erroredFiles

        if len(self.parsedFiles)==0:
            print("Before calling exportCSV(), you should "+
                  "add some files using pushFile() or pushAllFiles().")
        if indexName not in self.CSVs:
            print("'{}' was not one of the possible indeces. ".format(indexName)+
                  "Please choose from this list...\n"+
                  "{}".format(self.listCSVs()))
        return False
    #END DEF


    def listCSVs(self):
        """Returns a list of the CSV index names the user has imported"""
        return list(self.CSVs.keys())



# CSV DATA MANAGEMENT ----------------------------------------------------------

    def __clean(self, value):
        """Given a string (that will be a value in a CSV), returns the 'clean' value."""
        for replacement in [("\"",""), (",","")]:
            value = value.replace(*replacement)
        #END FOR
        if value=="Connectivity Test Failed":
            value = "no effective service"
        elif value=="Test Timeout":
            value = "timeout"
        elif value=="Ping Timeout" or value=="No ACK Received":
            value = "connect_error1"
        elif value=="Write Failure" or value=="Network Unreachable":
            value = "connect_error2"
        elif value=="Output Error" or value=="Bad Exit Value" or value=="Wrong Connection Made":
            value = "bad_output"
        elif value=="Unknown Error":
            value = "unknown_error"
        #END IFs
        return value
    #END DEF

    def __cleanCSV(self, csv):
        """Takes a given csv (as a 2-D array), and cleans all of the values"""
        for ROW in csv:
            for ELEM in ROW:
                if isinstance(ELEM, str):
                    ROW[ROW.index(ELEM)] = self.__clean(ELEM)
        return True
    #END DEF

#END CLASS

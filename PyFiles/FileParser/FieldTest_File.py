﻿"""
------------------------------------------------------------------------
FIELDTEST_FILE.PY

AUTHOR(S):    Peter Walker    pwalker@csumb.edu
              Evan Schwander  eschwander@csumb.edu

PURPOSE-  This object will hold a raw data file's header information (see list of variables)
            and then parses individual tests from the remaining text, storing them as a series of
            objects in the Tests variable.
          In Addition, Video Metrics are calculated here.
------------------------------------------------------------------------
"""
if __name__=="__main__":
    raise SystemExit

# IMPORTS
import os
import sys
from platform import system
if system()=="Windows":
    import ntpath as path
else:
    import os.path as path
if path.dirname(__file__) not in sys.path:
    sys.path.append(path.dirname(__file__))

#Importing necessary basic_utils functions
from _parserUtils.basic_utils import getLinesWith
from _parserUtils.device_tester_table import table
#Importing the necessary sub-classes and base classes
from _File import File
from UDP_Test import UDP_Test
#Importing the senstive information
from PyFiles.FileParser._sensitiveInfo.serverIPs import FieldTest_EastWest
#END IMPORTS


class FieldTest_File(File):

    """
    The starting point for a user's interaction with the parser. This is the
     class that they import and initialize with a text file, containing the
     output of a Field Test test.

    INHERITED ATTRIBUTES
        FilePath            String, the path to the file being parsed
        Filename            String, the name of the file (cut from the FilePath)
        Date                String, the Date when the test was conducted
        Time                String, the Time the test was conducted
        EastWestSrvrIPs     Tuple of Strings, the IP addresses of the East and
                             West server the files were connecting to
        Tests               Dictionary, each test in the file, where each index
                             is the type of test (TCP, UDP, PING, TCRT)
        TestsByNum          Dictionary, each test in the file, where each index
                             is the number of the test (ie. the order run)

     ATTRIBUTES
        Devicetype          String, the type of device (Netbook or Phone)
        DeviceID            String, the ID of the device being used
        AppVersion          String, the version of app being used
        OSName              String, the name of the device's operating system
        OSArchitecture      String, the architecture version of the OS
        OSVersion           String, the version of the OS
        JavaVersion         String, the version of Java being used
        JavaVendor          String, the vender of Java being used
        Tester              The ID of the Tester using this device
        Server              String, the name of the server connected to
        Host                String, the host being used
        NetworkProvider     String, the cellular provider of the connection
        NetworkOperator     String, the name of the network operator (generally same as Provider)
        NetworkCarrier      String, the normalized name of the carrier used during this test
        ConnectionType      String, technology used in connection
        LocationID          String, the source of location data (GPS or Network)
        Latitude            Float, Latitude of device during testing
        Longitude           Float, Longitude of device during testing
        AllCoordPairs       List of Tuples
    """

    def __new__(cls, *args, **kwargs):
        """
        Before creating an instance of the given file as a parsed object, we want to check
         that the file is indeed a test file. This will see if the necessary text
         is in the first few lines. If not, then we return None, and the object is not created
        """
        if 'empty' in kwargs and kwargs['empty']:
            return File.__new__(cls)
        #Getting the file path that was passed in to the constructor
        if "filePath" in kwargs:
            fileLoc = kwargs["filePath"]
        else:
            fileLoc = args[0]
        #Removing any backslashes that may have been included in the file path by
        # converting the string into a representation of it (which will escape the
        # backslashes), removing the backslashes, and then the single quotes. We
        # then save the result back into fileLoc
        if system()!="Windows":
            fileLoc = path.abspath(fileLoc).replace("\\","").strip()
        #Checking that the file is indeed a FieldTest File. If not, return None
        try:
            with open(fileLoc) as checkingFile:
                allText = checkingFile.read()
            #END WITH FILE
            if all( [(string not in allText.split("\n\n")[0]) for string in ["CPUC Tester","CPUC Traceroute"]] ):
                if "DEBUG" in kwargs and kwargs["DEBUG"]:
                    print("{} is not a Field Test output file. ".format(os.path.basename(fileLoc))+
                          "It did not have the necessary header.", file=sys.stderr)
                return None
        except:
            print(fileLoc+" is a file that could not be read.", file=sys.stderr)
            return None
        inst = File.__new__(cls)
        return inst
    #END DEF

    def __init__(self, filePath="", **kwargs):
        """
        Initializes the object by parsing the data in the given file path. Calls parent's __init__
        ARGS:
            filePath    String, containing absolute path to raw data file
        """
        if 'empty' in kwargs and kwargs['empty']:
            return
        #Quick little bit of formatting
        if system()!="Windows":
            filePath = path.abspath(filePath).replace("\\","").strip()

        #Call the parent class' __init__
        eastAndWestServerIP = FieldTest_EastWest
        File.__init__(self, filePath=filePath, eastWestIP=eastAndWestServerIP)
        self.loadFieldTestInfo()

        #Actually parsing the tests in the file
        self.findAndParseTCPTests()
        self.findAndParsePINGTests()
        self.findAndParseUDPTests()

        for eastwest in ['East','West']:
            try:
                self.RValue[eastwest] = self.calcRval(eastwest)
                self.MOS[eastwest] = self.calcMOS(eastwest)   
            except:
                self.RValue[eastwest] = 'NA'
                self.MOS[eastwest] = 'NA'

        #This is one final check, to make sure that we have all 14 tests. If not, then
        # there was an unknown test of some kind, and we set our _contains_Errors to True
        #The 14 Tests are:
        #   2 PING TESTS (1 East, 1 West)
        #   4 TCP TESTS (2 East, 2 West)
        #   6 UDP 1 second TESTS (3 East, 3 West)
        #   2 UDP 5 second TESTS (1 East, 1 West)
        if (len(self.TestsByNum) != 14) and not self.ContainsErrors:
            specialMessage = ("There was an unknown error of some kind, and the 14 necessary" +
                              " tests were not performed. There are "+str(14-len(self.TestsByNum))+
                              " tests missing.")
            self._ErrorHandling__setErrorCode(404, specialMessage)
        #END IF

        #Video Metric Stuff
        try:
            self.WestVideoMetrics = VideoMetrics(self, 'West').getValues()
        except Exception as e:
            print(e)
            self.WestVideoMetrics = []
        try:
            self.EastVideoMetrics = VideoMetrics(self, 'East').getValues()
        except:
            self.EastVideoMetrics = []
        #self.EastVideoMetrics = VideoMetrics(self, 'east').getValues()

    #END INIT



# INITIALIZATION FUNCTIONS -----------------------------------------------------

    def loadFieldTestInfo(self):
        """
        Parses data and info in given file (location is filePath) and stores
         it in the object's attributes
        ARGS:
            None
        RETURNS:
            None
        """
        #This opens the file, and stores the file stream into the variabe fs
        with open(self.FilePath,'r') as fs:
            #Read in Operating System Header Information
            self.parseLineAndSetAttr(fileStream=fs, delimiter=["Name =", "Architecture =", ", Version ="],
                                     attribute=["OSName", "OSArchitecture", "OSVersion"],
                                     hasParts=True)
            #Read in Java Header Information
            self.parseLineAndSetAttr(fileStream=fs, delimiter=[": Version =", "Vendor ="],
                                     attribute=["JavaVersion", "JavaVendor"],
                                     hasParts=True)
            #Looping through pairs of delimiter and attribute pairs
            for pair in [("Server: ","Server"),("Host: ","Host"),("NetworkProvider: ","NetworkProvider"),
                         ("Network Provider: ","NetworkProvider"), ("NetworkOperator: ","NetworkOperator"),
                         ("Device ID: ","DeviceID"),("Host name: ","DeviceID"),
                         ("ConnectionType: ","ConnectionType"),("Location ID: ","LocationID"),
                         ("Location: ","LocationID")]:
                self.parseLineAndSetAttr(fileStream=fs, delimiter=pair[0], attribute=pair[1])
            #END FOR

            #Defining self.NetworkCarrier, based on the data in NetworkProvider and NetworkOperator
            if self.NetworkProvider in self.ConfirmedCarriers:
                self.NetworkCarrier = self.NetworkProvider
            elif self.NetworkOperator in self.ConfirmedCarriers:
                self.NetworkCarrier = self.NetworkOperator
            #These ELIFs are for the special cases when the Provider is 'sprint' or 'Verizon Wireless'
            elif self.NetworkProvider == "sprint":
                self.NetworkCarrier = "Sprint"
            elif self.NetworkOperator == "Verizon Wireless":
                self.NetworkCarrier = "Verizon"
            else:
                self.NetworkCarrier = "NA"
            #END IF/ELIF/ELSE

            #Setting the Device Type based on the Date/Time line, and the file name
            if getLinesWith(fs,"Testing started at") and "WBBD" not in self.Filename:
                if "tablet" in getLinesWith(fs,"CPUC Tester")[0].lower():
                    self.DeviceType = "Tablet"
                else:
                    self.DeviceType = "Phone"
                    #checks if the Phone is an iPhone
                    if getLinesWith(fs,"iPhone"):
                        self.DeviceType = "iPhone"
            else:
                self.DeviceType = "Netbook"
            #END IF

            #This is for the rare case when the Device ID was not recorded in the test for some reason
            if not self.DeviceID:
                self.DeviceID = "NA"

            #Determining which Tester used the device that conducted this test
            self.Tester = "NA"
            if self.DeviceID != "NA":
                #First we much check wether or not the device is on iOS
                # iOS devices use a different tester scheme than android
                if self.DeviceType == "iPhone":
                    self.Tester = self.parseiPhoneTester(self.DeviceID)
                #This converts the multiline string into a 2-D list, where the first
                # element is the device ID, and the second is the tester number
                else:
                    dttable = [elem.split(",") for elem in table.strip().split("\n")]
                    for pair in dttable:
                        if self.DeviceID in pair[0]:
                            self.Tester = pair[1].strip()
                            break
                #END FOR
            #END IF

            #Getting all of the Latitude and Longitude pairs from the file, and
            # then searching through them for the most accurate (ie. first pair,
            # starting from the end, to have non-zero values)
            self.AllCoordPairs = self.__getAllCoordinates(fileStream=fs)
            for pair in reversed(self.AllCoordPairs):
                if all([elem!=0 for elem in pair]):
                    self.Latitude = pair[0]
                    self.Longitude = pair[1]
                    break
            #END FOR
            if "Latitude" not in self.__dict__:
                self.Latitude = 0
                self.Longitude = 0
        #END WITH FILE

        #Creating an array of the variables that we want to set to "NA" if they are empty
        emptiesToSet = ["OSName", "OSArchitecture", "OSVersion", "JavaVersion",
                        "JavaVendor", "Server", "Host", "NetworkProvider",
                        "NetworkOperator", "NetworkCarrier", "ConnectionType" ]
        self.setEmptysToDefault(attributes=emptiesToSet)
    #END DEF

    def __getAllCoordinates(self, fileStream):
        """
        A function used by loadFieldTestInfo to parse all of the Location pairs
         (i.e. Latitude and Longitude), and save in self.AllCoordPairs
        """
        #Getting all lines with the Latitude info
        latitudes = getLinesWith(fileStream, "Latitude:")
        #Now that we have all of the latitudes, we need to go back to those locations
        # in the file and get the following lines, which contain the Longitudes
        longitudes = []
        oldLoc = fileStream.tell()
        for goodLat in latitudes:
            line = "__"
            while line:
                if goodLat in line:
                    line = fileStream.readline()
                    longitudes.append(line)
                    break
                line = fileStream.readline()
            #END WHILE
            if latitudes.index(goodLat) != (len(longitudes)-1):
                longitudes.append("Longitude: 0.0")
        #END FOR
        fileStream.seek(oldLoc)

        pairs = []
        #Now we are going to go through our three arrays, grabbing each value
        # and making a 2-element array out of the latitude and longitude.
        #We will only go along the array up to the shortest array so that we don't try to
        # index beyond the array
        for i in range( len(latitudes) ):
            pairs.append( [latitudes[i].split("Latitude:")[1].strip(),
                           longitudes[i].split("Longitude:")[1].strip()] )
        #END FOR
        #Going through each 'pair' (of three elements) and casting them to a float if they
        # are numeric. Otherwise, we assume that they are 0
        for pair in pairs:
            newPair = []
            for elem in pair:
                try:
                    elem = float(elem)
                    newPair.append(elem)
                except:
                    newPair.append(0)
            #END FOR
            pairs[pairs.index(pair)] = newPair
        #END FOR
        #Making all of our 3-element pairs into tuples
        pairs = [tuple(pair) for pair in pairs]
        return pairs
    #END DEF

    def findAndParseUDPTests(self):
        """
        This takes the contents of the file being parsed, splits the content by "Staring Test"
         (to included any error messages in the tests) using the readAllTestsFromFile function,
         and the creates the specified Test objects. Assumes that self._fileContentsByTest
         contains all of the tests.
        """
        #First we run the readAllTestsFromFile function, to make sure that self._fileContentsByTest
        # is set, and contains all of the test output
        self.readAllTestsFromFile()
        #If the function above ran and did not hit any major errors, then we can run the code
        # inside of the IF block
        if not self.ContainsErrors:
            for chunk in self._fileContentsByTest:
                if "1 second Test" in chunk:
                    #This block gets the test number from the beginning of this chunk of
                    # characters. Each 1 second test has a different test number, as 3 are
                    # run in sequence. The number stored in tempTestNum applies to all 3
                    allStartingLine = ""
                    tempTestNum = 0
                    for line in chunk.split("\n"):
                        #If "Starting Test" is in the line, and we have not set our overall
                        # test number yet, we are going to parse it out. We also save the
                        # line with the number in it so that we can concatenate it to
                        # the beginning of each chunk
                        if ("Starting Test" in line) and (tempTestNum == 0):
                            allStartingLine = line+"\n"
                            rightChunk = line.split("Starting Test ")[1].strip()
                            tempTestNum = rightChunk.split(":")[0].split("..")[0]
                            break
                    #END FOR
                    subTests = chunk.split("Starting UDP 1")[1:]
                    subTests = [(allStartingLine+"Starting UDP 1"+text) for text in subTests]
                    #Now we go through each 1 second test, parse it into a UDP_Test object,
                    # and appended it to the array parsedSubTests. This array will then be
                    # added to self.Tests in the UDP and NUM category
                    for test in subTests:
                        #The if statement is one last check to make sure that the test actually contains
                        # some basic information
                        if "Iperf command line" in test:
                            parsedTest = UDP_Test(dataString=test, eastWestIP=self.EastWestSrvrIPs)
                            tempSubTestNum = test.split("Test #")[1].split("\n")[0].strip()
                            parsedTest.TestNumber = int(tempTestNum)
                            parsedTest.SubTestNumber = int(tempSubTestNum)
                            self.Tests[parsedTest.ConnectionType].append(parsedTest)
                            #Determining the index for this "sub" test
                            byNum = float(str(parsedTest.TestNumber)+"."+str(parsedTest.SubTestNumber))
                            self.TestsByNum[byNum] = parsedTest
                        #END IF
                    #END FOR
                else:
                    parsedTest = UDP_Test(dataString=chunk, eastWestIP=self.EastWestSrvrIPs)
                    #If the line above returned an object (and not None), then we have correctly
                    # parsed a Test, and can add it to our list.
                    if parsedTest:
                        self.Tests[parsedTest.ConnectionType].append(parsedTest)
                        self.TestsByNum[int(parsedTest.TestNumber)] = parsedTest
                    else:
                        pass #If we are passing, then the test was not a TCP test
                    #END IF/ELSE
                #END IF/ELSE
            #END FOR
        #END IF
    #END DEF

    def parseiPhoneTester(self, id):
        """
        iPhones use a different device id system than Android.
        This function parses out the Tester number from device id.
        """
        tester = ""
        for x in id:
            if x.isdigit():
                tester = tester + x
        bool = True
        while bool:
            if tester[0] == "0":
                tester = tester[1:]
            else:
                bool = False
        tester = "Tester " + tester
        return tester

# STRING PRINTOUT --------------------------------------------------------------

    # DESC: Returns a string representation of the object
    def __str__(self):
        """Returns a string represenation of the object"""
        return (self.StringPadding +
                "Filename: {}\n".format(self.Filename) +
                self.StringPadding +
                "Location ID: {}\n".format(self.LocationID) +
                self.StringPadding +
                "DateTime of Speed Test: {} {}\n".format(self.Date,self.Time) +
                self.StringPadding +
                "Device ID: {}\n".format(self.DeviceID) +
                self.StringPadding +
                "Device Type: {}\n".format(self.DeviceType) +
                self.StringPadding +
                "Network Carrier: {}\n".format(self.NetworkCarrier) +
                self.StringPadding +
                "Network: Provider = {}".format(self.NetworkProvider) +
                ", Operator = {}\n".format(self.NetworkOperator) +
                self.StringPadding +
                "Connection Type: {}\n".format(self.ConnectionType) +
                self.StringPadding +
                "OS: {}, {}, {}\n".format(self.OSName,self.OSArchitecture,self.OSVersion) +
                self.StringPadding +
                "Java: {}, {}\n".format(self.JavaVersion,self.JavaVendor) +
                self.StringPadding +
                "Connection: Server = {}, ".format(self.Server) + "Host = {}\n".format(self.Host) +
                self.StringPadding +
                "Location: ({},{})\n".format(self.Latitude,self.Longitude) +
                self.StringPadding +
                "Contain Major Errors: {}\n".format(repr(self.ContainsErrors)) +
                ((self.StringPadding + " Error Type: {}\n".format(self.ErrorType))
                 if self.ContainsErrors else ""
                 ) +
                ((self.StringPadding + " Error Message: {}\n".format(self.ErrorMessage))
                 if self.ContainsErrors else ""
                 ) +
                self.printTests()
                )
    #END DEF

    def _str_short(self):
        return (self.StringPadding +
                "Filename: {}\n".format(self.Filename) +
                self.StringPadding +
                "Location ID: {}\n".format(self.LocationID) +
                self.StringPadding +
                "DateTime of Speed Test: {} {}\n".format(self.Date,self.Time) +
                self.StringPadding +
                "Device ID: {}\n".format(self.DeviceID) +
                self.StringPadding +
                "Device Type: {}\n".format(self.DeviceType) +
                self.StringPadding +
                "Network Carrier: {}\n".format(self.NetworkCarrier) +
                self.StringPadding +
                "Network: Provider = {}".format(self.NetworkProvider) +
                ", Operator = {}\n".format(self.NetworkOperator) +
                self.StringPadding +
                "Connection Type: {}\n".format(self.ConnectionType) +
                self.StringPadding +
                "OS: {}, {}, {}\n".format(self.OSName,self.OSArchitecture,self.OSVersion) +
                self.StringPadding +
                "Java: {}, {}\n".format(self.JavaVersion,self.JavaVendor) +
                self.StringPadding +
                "Connection: Server = {}, ".format(self.Server) + "Host = {}\n".format(self.Host) +
                self.StringPadding +
                "Location: ({},{})\n".format(self.Latitude,self.Longitude) +
                self.StringPadding +
                "Contain Major Errors: {}\n".format(repr(self.ContainsErrors)) +
                ((self.StringPadding + " Error Type: {}\n".format(self.ErrorType))
                 if self.ContainsErrors else ""
                 ) +
                ((self.StringPadding + " Error Message: {}\n".format(self.ErrorMessage))
                 if self.ContainsErrors else ""
                 )
                )
    #END DEF

    '''
    def __repr__(self):
        """Returns a string of all of the attributes in this object"""
        string = ""
        for elem in self.__dict__:
            string += elem+":   "+str(self.__dict__[elem])+"\n"
        return string
    #END DEF
    '''
#END CLASS


class VideoMetrics:
    """
    This class calculates and stores video metric information.
    """
    def __init__(self, object, eastwest):
        #East or West MOS calculation
        MOS = object.MOS[eastwest]
        if eastwest == 'West':
            testnums = [0,2]
        elif eastwest == 'East':
            testnums = [1,3]
        else:
            print('Need east or west as an input')          
  
        #These lists are used to hold speed information from TCP tests
        upSum = []
        dnSum = []
        for i in range(0,4):
            upSum.append([])
            dnSum.append([])
 
        #These loops interate through all the speed measurements in a TCP test and put them into lists
        for test in testnums:
            for updown in ['UP','DOWN']:
                for thread in object.Tests['TCP'][test].Threads[updown]:
                    intervalCount = 0
                    for interval in thread.Measurements:
                        try:
                            if updown == 'UP':
                                upSum[test][intervalCount] += interval.Speed
                            else:
                                dnSum[test][intervalCount] += interval.Speed
                        except:
                            if updown == 'UP':
                                upSum[test].append(interval.Speed)
                            else:
                                dnSum[test].append(interval.Speed)
                        intervalCount+=1
                        if intervalCount == 10: #we only want the first 10 measurements
                            break
         
        # Putting down measurements into one list
        dnTotal = []
        upTotal = []
        for x in testnums:
            dnTotal.extend(dnSum[x])
            upTotal.extend(upSum[x])

        # The following variables are put into the csv
        self.DnVideo = self.streamQuality(dnTotal)
        self.UpVideo = self.streamQuality(upTotal)
        self.Conference = self.conferenceQuality(self.streamQuality(upTotal), self.streamQuality(dnTotal), MOS)
        self.Dn = self.streamQuality(dnTotal, 'quantity')
        self.Up = self.streamQuality(upTotal, 'quantity')

    def streamQuality(self, connection, toReturn = 'quality'):
        '''
        This function calculates the amount of each quality in a given connection.
        It then returns the overall quality of the connection or the quantity of each quality type in the connection.
        
        If toReturn equals 'quality' the function returns the overall quality. This is the default.
        or
        If toReturn equals 'quantity' the function returns the quantity of each quality type. 
        '''
        qualities = {'HD':0,'SD':0,'LD':0}
        for x in connection:
            if x >= 2500.0:
                qualities['HD'] += 1
            elif x >= 700.0:
                qualities['SD'] += 1
            else:
                qualities['LD'] += 1

        if toReturn == 'quality':
            if qualities['HD'] / len(connection) >= 0.95:
                return 'HD'
            elif (qualities['SD'] + qualities['HD']) / len(connection) >= 0.95:
                return 'SD'
            else:
                return 'LD'
        
        if toReturn == 'quantity':
            return qualities

    def conferenceQuality(self, up, dn, mos):
        if mos < 4:
            return 'LD'
        else:
            if up == 'LD' or dn == 'LD':
                return 'LD'
            elif up == 'SD' or dn == 'SD':
                return 'SD'
            else:
                return 'HD'

    def getValues(self):
        '''
        getValues returns all the values stored in the VideoMetrics class.
        '''
        values = []
        values.append(self.Dn['LD'])
        values.append(self.Dn['SD'])
        values.append(self.Dn['HD'])
        values.append(self.DnVideo)
        values.append(self.Up['LD'])
        values.append(self.Up['SD'])
        values.append(self.Up['HD'])
        values.append(self.UpVideo)
        values.append(self.Conference)
        return values
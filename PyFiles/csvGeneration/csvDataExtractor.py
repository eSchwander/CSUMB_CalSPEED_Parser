#!/usr/local/bin/python3
"""
------------------------------------------------------------------------
__CSV DATA EXTRACTOR.PY

AUTHOR(S):     Peter Walker    pwalker@csumb.edu
               Evan Schwander  eschwander@csumb.edu

PURPOSE-  The file contains a number of functions that will take a given
            parsed file, and return an array of values that can be
            exported as a CSV
------------------------------------------------------------------------
"""

#IMPORTS
#import os
import sys
#import datetime
#import traceback
from statistics import (pstdev, median, mean)
from platform import system
if system()=="Windows":
    import ntpath as path
else:
    import os.path as path
if path.dirname(__file__) not in sys.path:
    sys.path.append(path.dirname(__file__))
from _csvUtils._csvHeaders_ import (FieldTestHeaders, CrowdSourceHeaders)
#END IMPORTS


class csvDataExtractor(object):

    """
    The purpose of the this class is to specialize in data extraction.

    The intialization function will take a file type, which is a string that is
     either 'fieldtest' or 'crowdsource' (for the moment). This attribute will
     dictate which hidden function is called when the public extraction function
     is executed.
    Each extraction function will take a given object, and extract the requested
     data from the necessary sub-objects. The data will then be ordered into an
     array, and returned to the user.
    """

    FILETYPES = ['fieldtest',
                 'crowdsource']

    def __init__(self, fileType='fieldtest', **kwargs):
        """Initializes the CSV Generator object"""
        #Determining if the 'fileType' passed in is one of the possible options
        if fileType.lower() not in self.FILETYPES:
            print("Given data file type, '{}',".format(fileType) +
                  " is not one of the possible options. Defaulting to 'fieldtest'.")
            fileType = self.FILETYPES[0]
        self.fileType = fileType.lower()
    #END DEF



# DATA EXTRACTOR DECORATORS ----------------------------------------------------

    def __POST_returnChecker(headers, headerIndex='csv Default Headers'):
        """
        A wrapper that takes the index of an item in the dictionary 'headers', which
         will likely be a reference to the headers imported at the beginning of this file
        """
        assert (isinstance(headers, dict)
                ),(
                "You must pass in a dictionary of header strings. "+
                "Was given a {}".format(type(headers)))
        assert (headerIndex in headers
                ),(
                "The header index given must exist in the 'headers' dictionary. "+
                "'{}' is not in this dictionary".format(headerIndex))
        #Now that our error checks are done, we can actually call our wrapper
        def __POST_preWrap(func):
            def _POST_returnChecker(*args, **kwargs):
                potentialReturns = func(*args, **kwargs)
                if len(potentialReturns) != len(headers[headerIndex]):
                    raise ValueError("Not enough values were generated for the "+
                                     "'{}' field.\n".format(headerIndex)+
                                     "Was given {}".format(len(potentialReturns))+
                                     ", expected {}".format( len(headers[headerIndex]) ))
                else:
                    return potentialReturns
            #END DEF
            return _POST_returnChecker
        return __POST_preWrap
    #END DEF

    def __PRE_objectChecker(func):
        def _PRE_objectChecker(*args, **kwargs):
            """This checks that the given objects (index 1) is of the correct type"""
            if args[0].fileType not in str(args[1].__class__).lower():
                return None
            return func(*args, **kwargs)
        #END DEF
        return _PRE_objectChecker
    #END DEF



# DEFAULT VALUES EXTRACTORS ----------------------------------------------------

    @__POST_returnChecker(FieldTestHeaders, "csv Default Headers")
    def __extractFT_DefaultVals(self, OBJECT):
        VALUES = []
        VALUES.append( OBJECT.Tester )
        VALUES.append( OBJECT.LocationID )
        VALUES.append( OBJECT.Date )
        VALUES.append( OBJECT.Time )
        VALUES.append( OBJECT.NetworkProvider )
        VALUES.append( OBJECT.NetworkOperator )
        VALUES.append( OBJECT.ConnectionType )
        VALUES.append( OBJECT.Latitude )
        VALUES.append( OBJECT.Longitude )
        VALUES.append( OBJECT.DeviceID )
        VALUES.append( OBJECT.DeviceType )
        return VALUES
    #END DEF

    @__POST_returnChecker(CrowdSourceHeaders, "csv Default Headers")
    def __extractCS_DefaultVals(self, OBJECT):
        VALUES = []
        VALUES.append( OBJECT.Date )
        VALUES.append( OBJECT.Time )
        VALUES.append( OBJECT.AppVersion )
        VALUES.append( OBJECT.Environment )
        VALUES.append( OBJECT.PhoneModel )
        VALUES.append( OBJECT.PhoneManufac )
        VALUES.append( OBJECT.PhoneAPIVer )
        VALUES.append( OBJECT.PhoneSDKVer )
        VALUES.append( OBJECT.NetworkProvider )
        VALUES.append( OBJECT.NetworkOperator )
        #If the device was a desktop, then we want the Network
        # column in the CSV to hold all of the connection types the
        # device had
        if OBJECT.Devicetype == "Desktop":
            connTypes = ", ".join(OBJECT.ConnectionType)[:-2]
            VALUES.append( connTypes )
        else:
            if OBJECT.NetworkType.lower() == "wifi":
                VALUES.append( OBJECT.NetworkType )
            else:
                VALUES.append( OBJECT.ConnectionType )
            #END IF/ELSE
        #END IF/ELSE
        VALUES.append( repr(OBJECT.Roaming) )
        #VALUES.append( OBJECT.WiFiBSSID )
        VALUES.append( OBJECT.WiFiSSID )
        VALUES.append( OBJECT.LocationSource )
        VALUES.append( OBJECT.Latitude )
        VALUES.append( OBJECT.Longitude )
        VALUES.append( OBJECT.DistanceMoved )
        VALUES.append( OBJECT.Devicetype )
        return VALUES
    #END DEF

    @__PRE_objectChecker
    def extractDefaultVals(self, OBJECT, **kwargs):
        """
        Based on the object's fileType attribute, calls the correct
         default value extractor on the given file object.
        """
        if self.fileType == self.FILETYPES[0]:
            return self.__extractFT_DefaultVals(OBJECT)
        elif self.fileType == self.FILETYPES[1]:
            return self.__extractCS_DefaultVals(OBJECT)
        else:
            return []
    #END DEF



# EXTRA VALUES EXTRACTORS ------------------------------------------------------

    @__POST_returnChecker(FieldTestHeaders, "csv Extra Headers")
    def __extractFT_ExtraVals(self, OBJECT):
        #csvExtraHeaders = ["Census2010", "R5Coverage", "NormalLAT", "NormalLONG" ]
        extraVals = ["NA","NA"]
        extraVals.append( "" )#self.AvgLatitude )
        extraVals.append( "" )#self.AvgLongitude )
        return extraVals
    #END DEF

    @__POST_returnChecker(CrowdSourceHeaders, "csv Extra Headers")
    def __extractCS_ExtraVals(self, OBJECT):
        return []

    @__PRE_objectChecker
    def extractExtraVals(self, OBJECT, **kwargs):
        """
        Based on the object's fileType attribute, calls the correct
         extra value extractor on the given file object. Currently, neither type
         of files actually return any useful values.
        """
        if self.fileType == self.FILETYPES[0]:
            return self.__extractFT_ExtraVals(OBJECT)
        elif self.fileType == self.FILETYPES[1]:
            return self.__extractCS_ExtraVals(OBJECT)
        else:
            return []
    #END DEF

# VIDEO METRICS VALUES EXTRACTORS ------------------------------------------------------
    '''
    @__POST_returnChecker(FieldTestHeaders, "csv Video Metrics Headers")
    def __extractFT_VideoMetrics(self, OBJECT):
        VALUES = []
        if len(OBJECT.VideoMetrics) == 18:
            for values in OBJECT.VideoMetrics:
                VALUES.append(values)
        else:
            for _ in range(0,18):
                VALUES.append( 'Error' )
        return VALUES
    
    @__PRE_objectChecker
    def extractVMVals(self, OBJECT, **kwargs):
        """
        Based on the object's fileType attribute, calls the correct
         Video Metric value extractor on the given file object
        """
        if self.fileType == self.FILETYPES[0]:
            return self.__extractFT_VideoMetrics(OBJECT)
        else:
            return []
    '''
##### PING VALUES ##############################################################

# PING VALUES EXTRACTORS -------------------------------------------------------

    def __getPINGVals(self, pingTest):
        csvVals = []
        if not pingTest.ContainsErrors:
            csvVals.append(pingTest.RTTMin)
            csvVals.append(pingTest.RTTMax)
            csvVals.append(pingTest.RTTAverage)
            csvVals.append(pingTest.LossPercent)
        else:
            csvVals = [pingTest.ErrorType]*4
        return csvVals
    #END DEF

    def __extractPINGVals(self, OBJECT):
        """Getting the West, then East, RTT Min, Max, Average, and loss percent as an array"""
        #This array will hold all of the Ping values that will be in the csv
        pingVals = []
        #Get the RTT Min, Max, Average, and calculate the percent loss of packets in the PING test
        for connLoc in ["West", "East"]:
            pingTest = OBJECT.getTest("PING", ConnectionLoc=connLoc)
            if pingTest:
                pingVals.extend(self.__getPINGVals(pingTest[0]))
            else:
                pingVals.extend([OBJECT.ErrorType]*4)
        #END FOR
        return pingVals
    #END DEF

    @__POST_returnChecker(FieldTestHeaders, "csv PING Headers")
    def __extractFT_PINGVals(self, OBJECT):
        VALS = self.__extractPINGVals(OBJECT)
        #This is to re-order the values according to the csv Headers
        VALS = VALS[4:8] + VALS[0:4]
        return VALS

    @__POST_returnChecker(CrowdSourceHeaders, "csv PING Headers")
    def __extractCS_PINGVals(self, OBJECT):
        return self.__extractPINGVals(OBJECT)

    @__PRE_objectChecker
    def extractPINGVals(self, OBJECT, **kwargs):
        """
        Based on the object's fileType attribute, calls the correct
         PING value extractor on the given file object
        """
        if self.fileType == self.FILETYPES[0]:
            return self.__extractFT_PINGVals(OBJECT)
        elif self.fileType == self.FILETYPES[1]:
            return self.__extractCS_PINGVals(OBJECT)
        else:
            return []
    #END DEF



# RVALUE/MOS VALUES EXTRACTORS -------------------------------------------------

    def __extract_RValMOSVals(self, OBJECT):
        """Get the R-Value and MOS for West and East"""
        rValMOSVals = []
        for connLoc in ['West', 'East']:
            # Check for any errors in. If there are any, use the appropriate error message
            if OBJECT.RValue[connLoc] == 'NA' or OBJECT.RValue[connLoc] == '': 
                try:
                    rValMOSVals.extend(self.findErrors(OBJECT))
                except:
                    rValMOSVals.extend([OBJECT.ErrorType]*2)
            else:
                rValMOSVals.append(OBJECT.RValue[connLoc])
                rValMOSVals.append(OBJECT.MOS[connLoc])
        return rValMOSVals

    def findErrors(self, OBJECT):
        #if not [OBJECT.ErrorType] == '':          
        #    return [OBJECT.ErrorType]*2 
        #else:
        for tests in [OBJECT.Tests['PING'],OBJECT.Tests['UDP'], OBJECT.Tests['TCP']]:
            for test in tests:
                if test.ContainsErrors:
                    return [test.ErrorType]*2 
        

    @__POST_returnChecker(FieldTestHeaders, "csv RvMos Headers")
    def __extractFT_RValMOSVals(self, OBJECT):
        #The returns are saved into a variable so that we can swap the order
        VALS = self.__extract_RValMOSVals(OBJECT)
        #This is to re-order the values according to the csv Headers
        VALS = VALS[2:4] + VALS[0:2]
        return VALS

    @__POST_returnChecker(CrowdSourceHeaders, "csv RvMos Headers")
    def __extractCS_RValMOSVals(self, OBJECT):
        return self.__extract_RValMOSVals(OBJECT)

    @__PRE_objectChecker
    def extractRValMOSVals(self, OBJECT, **kwargs):
        """
        Based on the object's fileType attribute, calls the correct
         PING R-Value and MOS value extractor on the given file object
        """
        if self.fileType == self.FILETYPES[0]:
            return self.__extractFT_RValMOSVals(OBJECT)
        elif self.fileType == self.FILETYPES[1]:
            return self.__extractCS_RValMOSVals(OBJECT)
        else:
            return []
    #END DEF




##### UDP VALUES ###############################################################

# UDP VALUES EXTRACTORS --------------------------------------------------------

    def __getUDPVals(self, udpTest):
        """Defining a short function to be used to get the necessary values from a UDP test"""
        csvVals = []
        if not udpTest.ContainsErrors:
            csvVals.append(udpTest.Threads[0].ServerReport.Jitter)
            csvVals.append(udpTest.Threads[0].ServerReport.Dtgrams_Perc)
            csvVals.append(udpTest.TestInterval)
        else:
            csvVals = [udpTest.ErrorType]*3
        #END IF/ELSE
        return csvVals
    #END DEF


    @__POST_returnChecker(FieldTestHeaders, "csv UDP Headers")
    def __extractFT_UDPVals(self, OBJECT):
        udpVals = []
        #We are going loop through all of the sub test numbers in order, and with each sub test number,
        # we get the East test, and then the West test, getting the default CSV values from each test
        for connLoc in ["West", "East"]:
            for subTestNum in [1, 2, 3]:
                udpTest = OBJECT.getTest("UDP", TestInterval=1,
                                         SubTestNumber=subTestNum,
                                         ConnectionLoc=connLoc)
                if udpTest:
                    udpVals.extend(self.__getUDPVals(udpTest[0]))
                else:
                    udpVals.extend([OBJECT.ErrorType]*3)
            #END FOR
        #END FOR
        for connLoc in ["West", "East"]:
            #Now we get the 5 second interval East test, and get it's default CSV values, which are
            # appended to the array that we will return
            udpTest = OBJECT.getTest("UDP", TestInterval=5,
                                     ConnectionLoc=connLoc)
            if udpTest:
                udpVals.extend(self.__getUDPVals(udpTest[0]))
            else:
                udpVals.extend([OBJECT.ErrorType]*3)
        #END FOR
        return udpVals
    #END DEF

    @__POST_returnChecker(CrowdSourceHeaders, "csv UDP Headers")
    def __extractCS_UDPVals(self, OBJECT):
        udpVals = []
        #We are going loop through all of the sub test numbers in order, and with each sub test number,
        # we get the East test, and then the West test, getting the default CSV values from each test
        for connLoc in ["West", "East"]:
            #Now we get the 5 second interval East test, and get it's default CSV values, which are
            # appended to the array that we will return
            udpTest = OBJECT.getTest("UDP", ConnectionLoc=connLoc)
            if udpTest:
                udpVals.extend(self.__getUDPVals(udpTest[0]))
            else:
                udpVals.extend([OBJECT.ErrorType]*3)
        #END FOR
        return udpVals
    #END DEF

    @__PRE_objectChecker
    def extractUDPVals(self, OBJECT, **kwargs):
        """
        Based on the object's fileType attribute, calls the correct
         UDP value extractor on the given file object
        """
        if self.fileType == self.FILETYPES[0]:
            return self.__extractFT_UDPVals(OBJECT)
        elif self.fileType == self.FILETYPES[1]:
            return self.__extractCS_UDPVals(OBJECT)
        else:
            return []
    #END DEF




##### TCP VALUES ###############################################################

# TCP VALUES EXTRACTORS --------------------------------------------------------

    def __getTCPVals(self, tcpTest):
        """Returns a List of the default CSV values needed for the creation of a CSV"""
        csvVals = []
        #If there was no error, there are values to calculate
        # Otherwise, we return an array of "self._error_Type"
        if not tcpTest.ContainsErrors:
            upSum = 0
            dnSum = 0
            for thread in tcpTest.Threads["UP"]:
                upSum += thread.FinalMsmt.Speed
            for thread in tcpTest.Threads["DOWN"]:
                dnSum += thread.FinalMsmt.Speed
            csvVals = [upSum, dnSum]
        else:
            csvVals = [tcpTest.ErrorType]*2
        return csvVals
    #END DEF

    @__POST_returnChecker(FieldTestHeaders, "csv TCP Headers")
    def __extractFT_TCPVals(self, OBJECT):
        """Getting the default TCP values (averge Upload and Download for all tests)"""
        tcpVals = []
        #Getting the values need for the TCP tests. If a test does not exist, then
        # it's placeholder is "No Test"
        for connLoc in ["West", "East"]:
            tcpTests = OBJECT.getTest("TCP", ConnectionLoc=connLoc)
            #If there are tests, then we calculate the necessary values
            if tcpTests:
                #This is just a quick test to see if the TCP tests are in order by number.
                # If they aren't then we swap them
                if (len(tcpTests) == 2) and (tcpTests[0].TestNumber > tcpTests[1].TestNumber):
                    #This is a quick swap
                    tcpTests[0], tcpTests[1] = tcpTests[1], tcpTests[0]
                #END IF

                _partial_tcpVals = []
                for test in tcpTests:
                    _partial_tcpVals.extend( self.__getTCPVals(test) )
                #END FOR
                if len(tcpTests) == 1:
                    _partial_tcpVals.extend( [OBJECT.ErrorType]*2 )

                #Now we append the values for this direction to the array that
                # we are returning
                tcpVals.extend( _partial_tcpVals )
            else:
                tcpVals.extend( [OBJECT.ErrorType]*4 )
            #END IF/ELSE
        #END FOR
        #This list addition is because of the order of values above versus what is
        # the expected order based on the csv Headers
        tcpVals = tcpVals[0:2] + tcpVals[4:6] + tcpVals[2:4] + tcpVals[6:8]
        return tcpVals
    #END DEF

    @__POST_returnChecker(CrowdSourceHeaders, "csv TCP Headers")
    def __extractCS_TCPVals(self, OBJECT):
        """Getting the default TCP values (averge Upload and Download for all tests)"""
        tcpVals = []
        #Getting the values need for the TCP tests. If a test does not exist, then
        # it's placeholder is "No Test"
        for connLoc in ["West", "East"]:
            tcpTest = OBJECT.getTest("TCP", ConnectionLoc=connLoc)
            if tcpTest:
                tcpVals.extend( self.__getTCPVals(tcpTest[0]) )
            else:
                tcpVals.extend( [OBJECT.ErrorType]*2 )
            #END IF/ELSE
        #END FOR
        return tcpVals
    #END DEF

    @__PRE_objectChecker
    def extractTCPVals(self, OBJECT, **kwargs):
        """
        Based on the object's fileType attribute, calls the correct
         TCP default value extractor on the given file object
        """
        if self.fileType == self.FILETYPES[0]:
            return self.__extractFT_TCPVals(OBJECT)
        elif self.fileType == self.FILETYPES[1]:
            return self.__extractCS_TCPVals(OBJECT)
        else:
            return []
    #END DEF



# STAT VALUES EXTRACTORS -------------------------------------------------------

    def __getTCPStatValues(self, tcpTest):
        """
        This creates an array of 4 values that will be appended to the Results CSV
         provided by CPUC. If there was an error in the test, the 4 values returned are the error type.
         Otherwise, the 4 values are the StDev and Median for both thread directions for this test
        """
        csvVals = []
        #If there was no error, there are values to StDev and Median
        # Otherwise, we return an array of "None"
        if not tcpTest.ContainsErrors:
            #Calculating the stDev's and medians of the Up and Down threads
            upThread = tcpTest.get_ThreadSumValues(direction="UP", attribute="Speed")
            downThread = tcpTest.get_ThreadSumValues(direction="DOWN", attribute="Speed")
            csvVals.append( pstdev(upThread) )
            csvVals.append( median(upThread) )
            csvVals.append( pstdev(downThread) )
            csvVals.append( median(downThread) )
        else:
            csvVals = [tcpTest.ErrorType]*4
        return csvVals
    #END DEF

    @__POST_returnChecker(FieldTestHeaders, "csv Stat Headers")
    def __extractFT_TCPStatVals(self, OBJECT):
        tcpVals = []
        #This will get all of the West values, and then the East values
        for connLoc in ["West", "East"]:
            tcpTests = OBJECT.getTest("TCP", ConnectionLoc=connLoc)
            #If there are tests, then we calculate the necessary values
            if tcpTests:
                #This is just a quick test to see if the TCP tests are in order by number.
                # If they aren't then we swap them
                if (len(tcpTests) == 2) and (tcpTests[0].TestNumber > tcpTests[1].TestNumber):
                    #This is a quick swap
                    tcpTests[0], tcpTests[1] = tcpTests[1], tcpTests[0]
                #END IF
                _partial_tcpVals = []
                for test in tcpTests:
                    _partial_tcpVals.extend(self.__getTCPStatValues(test))
                if len(tcpTests) == 1:
                    _partial_tcpVals.extend( [OBJECT.ErrorType]*4 )
                #Finally appending the values to the array that we are returning
                tcpVals.extend(_partial_tcpVals)
            else:
                tcpVals.extend( [OBJECT.ErrorType]*8)
            #END IF/ELSE
        #END FOR
        #This is necessary to correctly align values with their headers. In the
        # Field Test CSV, we print the first West test, then the first East test
        # (and this pattern repeats for the second test for each direction). This
        # contrasts with both West tests, then both East
        tcpVals = tcpVals[:4] + tcpVals[8:12] + tcpVals[4:8] + tcpVals[12:16]
        return tcpVals
    #END DEF

    @__POST_returnChecker(CrowdSourceHeaders, "csv Stat Headers")
    def __extractCS_TCPStatVals(self, OBJECT):
        tcpVals = []
        #This will get all of the West values, and then the East values
        for connLoc in ["West", "East"]:
            tcpTest = OBJECT.getTest("TCP", ConnectionLoc=connLoc)
            if tcpTest:
                tcpVals.extend(self.__getTCPStatValues(tcpTest[0]))
            else:
                tcpVals.extend( [OBJECT.ErrorType]*4 )
            #END IF/ELSE
        #END FOR
        return tcpVals
    #END DEF

    @__PRE_objectChecker
    def extractTCPStatVals(self, OBJECT, **kwargs):
        """
        Based on the object's fileType attribute, calls the correct
         TCP Statistics value extractor on the given file object.
        """
        if self.fileType == self.FILETYPES[0]:
            return self.__extractFT_TCPStatVals(OBJECT, **kwargs)
        elif self.fileType == self.FILETYPES[1]:
            return self.__extractCS_TCPStatVals(OBJECT)
        else:
            return []
    #END DEF



# COMBINED STAT VALUES EXTRACTORS ----------------------------------------------

    def __calcTCPStatVals(self, UP, DN):
        if UP:
            upMean = mean(UP)
            upStDev = pstdev(UP)
            upMean_1 = upMean-upStDev
            upMean_2 = upMean_1-upStDev
        else:
            upMean = "bad_output"
            upStDev = "bad_output"
            upMean_1 = "bad_output"
            upMean_2 = "bad_output"
        if DN:
            dnMean = mean(DN)
            dnStDev = pstdev(DN)
            dnMean_1 = dnMean-dnStDev
            dnMean_2 = dnMean_1-dnStDev
        else:
            dnMean = "bad_output"
            dnStDev = "bad_output"
            dnMean_1 = "bad_output"
            dnMean_2 = "bad_output"
        #END IF/ELSEs
        return [upMean, upStDev, upMean_1, upMean_2,
                dnMean, dnStDev, dnMean_1, dnMean_2]
    #END DEF

    def __extract_TCPStatSVals(self, OBJECT):
        """Combining TCP values using Sathya's method"""
        allTCPs = OBJECT.getTest("TCP")
        upMsrments = []
        dnMsrments = []
        #We will only perform these functions and math if allTCPs actually
        # returned tests for us to use
        if allTCPs:
            for test in allTCPs:
                if not test.ContainsErrors:
                    upMsrments.extend(test.get_ThreadSumValues(direction="UP"))
                    dnMsrments.extend(test.get_ThreadSumValues(direction="DOWN"))
            return self.__calcTCPStatVals(upMsrments, dnMsrments)
        else:
            return [OBJECT.ErrorType]*8
    #END DEF

    @__POST_returnChecker(FieldTestHeaders, "csv Stat-S Headers")
    def __extractFT_TCPStatSVals(self, OBJECT):
        return self.__extract_TCPStatSVals(OBJECT)

    @__POST_returnChecker(CrowdSourceHeaders, "csv Stat-S Headers")
    def __extractCS_TCPStatSVals(self, OBJECT):
        return self.__extract_TCPStatSVals(OBJECT)

    @__PRE_objectChecker
    def extractTCPStatSVals(self, OBJECT, **kwargs):
        """
        Based on the object's fileType attribute, calls the correct
         TCP Stat-S value extractor on the given file object.
        """
        if self.fileType == self.FILETYPES[0]:
            return self.__extractFT_TCPStatSVals(OBJECT)
        elif self.fileType == self.FILETYPES[1]:
            return self.__extractCS_TCPStatSVals(OBJECT)
        else:
            return []
    #END DEF


# OVERALL STAT VALUES EXTRACTORS -------------------------------------------

    def __extract_TCPStatAVals(self, OBJECT):
        """
        This will conglomerate all upload speed from every TCP test into one
        list. The same will also be done with the download speeds.
        Once our lists have all 4 TCP test's speeds, we will then take the mean,
        the population standard deviation, and then calculate the mean minus
        one standard deviation.
        RETURNS:
            NBNValues   List of 6 values, the mean, population standard deviation,
                        and (mean - (1*pstdev)) of a combination of all threads from every
                        test in each direction.
        """
        allTCPs = OBJECT.getTest("TCP")
        upMeans = []
        dnMeans = []
        #We will only perform these functions and math if allTCPs actually
        # returned tests for us to use
        if allTCPs:
            for test in allTCPs:
                if not test.ContainsErrors:
                    upMeans.append( mean(test.get_ThreadSumValues(direction="UP")) )
                    dnMeans.append( mean(test.get_ThreadSumValues(direction="DOWN")) )
            return self.__calcTCPStatVals(upMeans, dnMeans)
        else:
            return [OBJECT.ErrorType]*6
    #END DEF

    @__POST_returnChecker(FieldTestHeaders, "csv Stat-A Headers")
    def __extractFT_TCPStatAVals(self, OBJECT):
        return self.__extract_TCPStatAVals(OBJECT)

    @__POST_returnChecker(CrowdSourceHeaders, "csv Stat-A Headers")
    def __extractCS_TCPStatAVals(self, OBJECT):
        return self.__extract_TCPStatAVals(OBJECT)

    @__PRE_objectChecker
    def extractTCPStatAVals(self, OBJECT, **kwargs):
        """
        Based on the object's fileType attribute, calls the correct
         TCP Stat-A value extractor on the given file object.
        """
        if self.fileType == self.FILETYPES[0]:
            return self.__extractFT_TCPStatAVals(OBJECT)
        elif self.fileType == self.FILETYPES[1]:
            return self.__extractCS_TCPStatAVals(OBJECT)
        else:
            return []
    #END DEF


# TCP QUALITY VALUES EXTRACTORS ------------------------------------------------

    def __TCPPeriod(self, tcpTest):
        if not tcpTest.ContainsErrors:
            PERIOD = {"UP": [], "DOWN": [] }
            for direction in PERIOD:
                #This block calculates the TCP Quality based on the total time
                # it took the thread to complete their downloads
                #For each thread, get the total time (final measurement timeEnd)
                for thread in tcpTest.Threads[direction]:
                    PERIOD[direction].append(thread.FinalMsmt.TimeEnd)
                #END FOR
            #This creates an array of average upload times (the average PERIOD)
            qualVals = [mean(PERIOD["UP"]), mean(PERIOD["DOWN"])]
        else:
            qualVals = [tcpTest.ErrorType]*2
        return qualVals
    #END DEF

    def __TCPRating(self, tcpTest):
        if not tcpTest.ContainsErrors:
            RATING = {"UP": [], "DOWN": []}
            for direction in RATING:
                #This block calculates the TCP Quality based on the data score,
                # a value between 1 and 0 based on how many intervals in the threads were
                # either downloading or uploading data
                allSpeeds = tcpTest.get_ThreadsValues(direction=direction)
                for thread in allSpeeds:
                    for elem in thread:
                        if elem>0:
                            RATING[direction].append(1)
                        else:
                            RATING[direction].append(0)
                #END FOR
            #END FOR
            qualVals = [mean(RATING["UP"]), mean(RATING["DOWN"])]
        else:
            qualVals = [tcpTest.ErrorType]*2
        return qualVals
    #END DEF

    @__POST_returnChecker(FieldTestHeaders, "csv Qual Headers")
    def __extractFT_TCPQualVals(self, OBJECT):
        """
        This function extracts the quality of the TCP connection.
        Quality is determined by either Time or Data. Time is the average total time it took for
        the TCP threads to complete transfer. Data is a score between 1 and 0, where
        a time interval is given a 1 if it is transmitting data, and a 0 if it is not. The 1's
        and 0's are totaled up and averaged.
        """
        tcpVals = []
        #This will get all of the West values, and then the East values
        for connLoc in ["West", "East"]:
            tcpTests = OBJECT.getTest("TCP", ConnectionLoc=connLoc)
            #If there are tests, then we calculate the necessary values
            if tcpTests:
                #This is just a quick test to see if the TCP tests are in order by number.
                # If they aren't then we swap them
                if (len(tcpTests) == 2) and (tcpTests[0].TestNumber > tcpTests[1].TestNumber):
                    #This is a quick swap
                    tcpTests[0], tcpTests[1] = tcpTests[1], tcpTests[0]
                #END IF
                _partial_tcpVals = []
                for test in tcpTests:
                    PERIOD = self.__TCPPeriod(test)
                    RATING = self.__TCPRating(test)
                    _partial_tcpVals.extend( [PERIOD[0], RATING[0], PERIOD[1], RATING[1]] )
                if len(tcpTests) == 1:
                    _partial_tcpVals.extend( [OBJECT.ErrorType]*4 )
                #Finally appending the values to the array that we are returning
                tcpVals.extend(_partial_tcpVals)
            else:
                tcpVals.extend( [OBJECT.ErrorType]*8)
            #END IF/ELSE
        #END FOR
        if len(OBJECT.WestVideoMetrics) == 9:
            for values in OBJECT.WestVideoMetrics:
                tcpVals.append(values)
        else:
            for _ in range(9):
                tcpVals.append( 'Error' )
        if len(OBJECT.EastVideoMetrics) == 9:
            for values in OBJECT.EastVideoMetrics:
                tcpVals.append(values)
        else:
            for _ in range(9):
                tcpVals.append( 'Error' )
        return tcpVals # The placement of this return might be a huge issue
        #This is necessary to correctly align values with their headers. In the
        # Field Test CSV, we print the first West test, then the first East test
        # (and this pattern repeats for the second test for each direction). This
        # contrasts with both West tests, then both East
        tcpVals = tcpVals[:4] + tcpVals[8:12] + tcpVals[4:8] + tcpVals[12:16]
        return tcpVals
    #END DEF

    @__POST_returnChecker(CrowdSourceHeaders, "csv Qual Headers")
    def __extractCS_TCPQualVals(self, OBJECT):
        tcpVals = []
        #This will get all of the West values, and then the East values
        for connLoc in ["West", "East"]:
            tcpTest = OBJECT.getTest("TCP", ConnectionLoc=connLoc)
            if tcpTest:
                PERIOD = self.__TCPPeriod(tcpTest[0])
                RATING = self.__TCPRating(tcpTest[0])
                tcpVals.extend( [PERIOD[0], RATING[0], PERIOD[1], RATING[1]] )
            else:
                tcpVals.extend( [OBJECT.ErrorType]*4 )
            #END IF/ELSE
        #END FOR
        if len(OBJECT.WestVideoMetrics) == 9:
            for values in OBJECT.WestVideoMetrics:
                tcpVals.append(values)
        else:
            for _ in range(9):
                tcpVals.append( 'NA' )
        if len(OBJECT.EastVideoMetrics) == 9:
            for values in OBJECT.EastVideoMetrics:
                tcpVals.append(values)
        else:
            for _ in range(9):
                tcpVals.append( 'NA' )
        return tcpVals
    #END DEF

    @__PRE_objectChecker
    def extractTCPQualVals(self, OBJECT, **kwargs):
        """
        Based on the object's fileType attribute, calls the correct
         TCP Quality value extractor on the given file object.
        """
        if self.fileType == self.FILETYPES[0]:
            return self.__extractFT_TCPQualVals(OBJECT)
        elif self.fileType == self.FILETYPES[1]:
            return self.__extractCS_TCPQualVals(OBJECT)
        else:
            return []
    #END DEF

#END CLASS

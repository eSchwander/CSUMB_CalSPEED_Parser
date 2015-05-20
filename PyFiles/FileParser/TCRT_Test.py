"""
------------------------------------------------------------------------
Evan_Test.PY

AUTHOR(S):    Evan Schwander		eschwander@csumb.edu

PURPOSE-  This class will hold an individual TraceRoute test.

VALUES TO CARE ABOUT (For the CSV): 
    HopCount - The amount of hops in a test.
    Hops[] - Holds Hop objects. Hops past HopCount hold 'NA' values
        Each Hop object holds its own number, name(Nm), IP(IP), and speed(D).
            
------------------------------------------------------------------------
"""
if __name__=="__main__":
    raise SystemExit

# IMPORTS
import sys
from _parserUtils.basic_utils import calc_rVal_MOS
from _Test import Test
from __Base import Formatting
from _sensitiveInfo.tcrtIPs import *
#END IMPORTS



class Hop(Formatting):

    """A simple class for holding the information from a single hop"""

    '''
    # ------------------------------
    # ---- CLASS VARIABLES ----
    Number = ""
    Name = ""
    IP = ""
    Speed = ""
    # ------------------------------
    '''
    
    def __init__(self, dataString):
        dataString = dataString.split(" ")
        temp = [x for x in dataString if x]
        self.Number = temp.pop(0)
        self.Name = temp.pop(0)
        self.IP = temp.pop(0)[1:-1]
        self.Speed = temp.pop(0)
        if self.IP == "":
            self.IP = "*"
        if self.Name == "*":
            self.Name = "NA" 
        if self.IP == "*":
            self.IP = "NA" 
        if self.Speed == "*":
            self.Speed = "NA" 


    
    def __str__(self):
        return("Hop number: {}\nDestination: {}\nDestination IP: {}\nSpeed: {} ms".format(self.Number, self.Name, self.IP, self.Speed))
    #END DEF


class TCRT_Test(Test):
    
    """A TRCRT test, containing parsed information about TCRT hops"""

    '''
    # ------------------------------
    # ---- INHERITED ATTRIBUTES ----
    ConnectionType  = ""
    ConnectionLoc   = ""
    TestNumber      = 0
    ReceiverIP      = ""
    StartingLine    = ""
    _text           = ""

    # ---- CLASS ATTRIBUTES ----
    Hops = []
    HopCount = 0
    HopMin = -1
    HopMax = -1
    HopAvg = -1
    is_outputType1  = True
    # ------------------------------
    '''

    def __init__(self, dataString="", eastWestIP=("0.0.0.0", "0.0.0.0")):
        '''
        Used to initialize an object of this class
        ARGS:
            self:       reference to the object calling this method (i.e. Java's THIS)
            dataString: String, the text that is going to be parsed
            eastWestIP: Tuple of two Strings, first String is the IP address of the East server, second the West
        '''
        # If we are at this point, then the dataString contained "traceroute", and we can
        # set the ConnectionType to "TCRT"
        self.ConnectionType = "TCRT"
        
        # Call the parent class' __init__
        Test.__init__(self, dataString=dataString, eastWestIP=eastWestIP)
        
        # Some variable initialization
        self.Hops = []
        self.Destination = ''
        self.HopMax = 40
        #Construct Hops array
        self.Hops.append(self.__parseHops(dataString))
    #END DEF

# INITIALIZATION FUNCTIONS -----------------------------------------------------

    def __parseHops(self, dataString):
        """ 
        Parses all the hops in a test and prepares them to be parsed individually 
        """
        # We start our function be splitting the data string into individual chunks,
        # which we will then parse individually
        dataChunks = [elem.strip() for elem in dataString.split("\n\n") if elem]
        for chunk in dataChunks:
            if "traceroute" in chunk:
                chunk = chunk.splitlines()
                # We pop off the frist line of the chunk as it has some special properties
                firstLine = chunk.pop(0)
                # Parse the first line to find HopMax and Destination
                self.__parseFirstLine(firstLine)
                # We finally parse the hops
                self.__parseIndividualHops(chunk)
        #END FOR
    #END DEF

    def __parseIndividualHops(self, dataString):
        """ 
        Creates Hop objects that are parsed upon creation 
        These objects are then stored into an array 
        Additionally, this function will fill the Hops array up to the 40 hop max 
        """
        # This is where we creat Hop objects and store them into an array
        self.Hops = []
        while(dataString):
            self.Hops.append(Hop(dataString.pop(0)))
        #Here we determine the number of hops before completion
        self.HopCount = len(self.Hops)
        # This loop fills the Hops array with fake Hop objects up to HopMax
        while(len(self.Hops) < self.HopMax):
            emptyHop = str(len(self.Hops)) + " NA (NA) NA"
            self.Hops.append(Hop(emptyHop))
    #END DEF

    def __parseFirstLine(self, dataString):
        """ 
        Finds destination IP and HopMax 
        """
        dataString = dataString.split(" ") 
        
        # The following loop finds the hop max and destination IP in the first line
        flag = False
        for x in dataString:
            if flag:
                self.HopMax = int(x)
                break
            if '.' in x:
                self.Destination = x[0:-1]
                flag = True

        if(self.Destination == CaliforniaIP):
            self.ConnectionLoc = "California"
        elif(self.Destination == OregonIP):
            self.ConnectionLoc = "Oregon"
        elif(self.Destination == EastCoastIP):
            self.ConnectionLoc = "East"

    #END DEF

    def __str__(self):
        # converts test into csv
        csv = str(self.HopCount) + ","
        for hop in self.Hops:
            csv += hop.Name + ","
            csv += hop.IP + ","
            csv += hop.Speed + ","
        return(csv)


"""
------------------------------------------------------------------------
UDP_TEST.PY

AUTHOR(S):    Peter Walker    pwalker@csumb.edu

PURPOSE-  This class will hold just an individual UDP speed test.
            This takes a chunk of text (as a string), and parses out all of the
            header information, like the server connected to, measuring format, etc.
            It then splits the test measurements into their individual threads,
            and passing the resulting strings to the Thread object.
------------------------------------------------------------------------
"""
if __name__=="__main__":
    raise SystemExit

# IMPORTS
import sys
from _Test import Test
#END IMPORTS


class UDP_Test(Test):

    """A UDP Test, which is a single upload thread, sending datagrams"""

    '''
    # ------------------------------
    # ---- INHERITED ATTRIBUTES ----
    ConnectionType  = ""
    ConnectionLoc   = ""
    Threads         = None
    TestNumber      = 0
    ReceiverIP      = ""
    Port            = 0000
    TestInterval    = 0
    MeasuringFmt    = None  #[kmKM] (Kbits, Mbits, KBytes, MBytes)
    _mform_short    = None
    _text           = ""
    iPerfCommand    = ""
    StartingLine    = ""

    # ---- CLASS ATTRIBUTES ----
    DatagramSize    = 0
    SubTestNumber   = 0
    TargetBandwidth = None  #n[KM]
    # ------------------------------
    '''



    def __new__(cls, *args, **kwargs):
        """
        Before creating an instance of the given file as a parsed object, we want to check
        that the file is indeed a test file. This will see if the necessary text
        is in the first few lines. If not, then we return None, and the object is not created
        """
        #Getting the Data String passed to this constructor that was passed in to the constructor
        if "dataString" in kwargs:
            dataString = kwargs["dataString"]
        else:
            dataString = args[0]
        #END IF/ELSe
        if "udp" not in dataString.lower():
            if "DEBUG" in kwargs and kwargs["DEBUG"]:
                print("The raw data passed to this constructor (UDP_Test) did not contain "+
                      "the necessary identifiers.",
                      file=sys.stderr)
            return None
        #END IF
        inst = Test.__new__(cls, *args, **kwargs)
        return inst
    #END DEF

    def __init__(self, dataString="", eastWestIP=("0.0.0.0", "0.0.0.0")):
        """
        Used to initialize an object of this class
        ARGS:
            self:       reference to the object calling this method (i.e. Java's THIS)
            dataString: String, the raw text that will be parsed
            eastWestIP: Tuple of two Strings, first String is the IP address of the East server, second the West
        """
        #If we are at this point, then the dataString contained "TCP", and we can
        # set the ConnectionType to "TCP"
        self.ConnectionType = "UDP"
        #Call the parent class' __init__
        Test.__init__(self, dataString=dataString, eastWestIP=eastWestIP)

        #If we were unable to parse out the iPerfCommand line from the text, then
        # we assume that there was an error of some kind that was not caught, and exit
        if not self.iPerfCommand:
            self._ErrorHandling__setErrorCode(101, "Iperf Command Line not Found")
            #raise RuntimeError("For some reason, the Iperf command line was not parsed.")
        else:
            #Getting the datagram size
            self.DatagramSize = self.iPerfCommand[self.iPerfCommand.find("-l"):].split(" ")[1].strip()
            #Getting the datagram size
            self.TargetBandwidth = self.iPerfCommand[self.iPerfCommand.find("-b"):].split(" ")[1].strip()
            self.SubTestNumber = 0
            if not self.ContainsErrors:
                #Declaring and creating the UDP Thread for this test
                self.Threads = []
                dataArray = [line for line in self._text if ("[ " in line)]
                threadNum = int(dataArray[0].split("]")[0].split("[")[1].strip())
                self.Threads.append( UDP_Thread(dataArr=dataArray,
                                                threadNum=threadNum,
                                                direction="UP",
                                                units=self.MeasuringFmt) )
            #END IF
        #END IF/ELSE
    #END DEF


# STRING OUTPUT ----------------------------------------------------------------

    def __str__(self):
        """Returns a string represenation of the object"""
        string = (  self.StringPadding[:-1] + "-" +
                    "Test Number: {}\n".format(self.TestNumber) +
                    ((self.StringPadding +
                      "Sub Test Number: {}\n".format(self.SubTestNumber))
                     if (self.SubTestNumber != 0) else ""
                     ) +
                    self.StringPadding +
                    "Connection Type: {}\n".format(self.ConnectionType) +
                    self.StringPadding +
                    "Connection Location: {}\n".format(self.ConnectionLoc) +
                    self.StringPadding +
                    "Receiver IP: {}:{}\n".format(self.ReceiverIP,self.Port) +
                    self.StringPadding +
                    "Test Interval: {}".format(self.TestInterval) +
                    "  Datagram Size: {}\n".format(self.DatagramSize) +
                    self.StringPadding +
                    "Target Bandwidth: {}".format(self.TargetBandwidth) +
                    "  Measurement Format: {}, {}\n".format(self.MeasuringFmt[0],
                                                            self.MeasuringFmt[1]) +
                    self.StringPadding +
                    "Contain Errors: {}\n".format(repr(self.ContainsErrors)) +
                    ((self.StringPadding + "Error Type: " +self.ErrorType+ "\n")
                     if self.ContainsErrors else ""
                     ) +
                    ((self.StringPadding + "Error Message: " +self.ErrorMessage+ "\n")
                     if self.ContainsErrors else ""
                     )
                    )
        if not self.ContainsErrors:
            for thread in self.Threads:
                string += str(thread)
        #END IF
        return string
    #END DEF
#END CLASS









"""
------------------------------------------------------------------------
UDP_THREAD.PY

AUTHOR(S):    Peter Walker    pwalker@csumb.edu

PURPOSE-  This object will represent a single thread, or pipe, in a network
            speed test. It will hold an array of Measurement objects, and has
            some basic object information
------------------------------------------------------------------------
"""
# IMPORTS
from _Thread import Thread
from _Measurement import UDP_ServerReport as ServerReport
#END IMPORTS


class UDP_Thread(Thread):

    """A Thread in a UDP test."""

    '''
    # ---- INHERITED ATTRIBUTES ----
    ThreadNumber    = 0
    DataDirection   = ""
    LocalIP         = ""
    LocalPort       = 0000
    ServerIP        = ""
    ServerPort      = 0000
    Measurements    = []
    FinalMsmt       = None

    # ---- CLASS ATTRIBUTES ----
    DatagramzSent = 0
    ServerReport = None
    # ----------------------------------
    '''


    def __init__(self, dataArr=None, threadNum=0, direction="UP", units=("KBytes", "Kbits/sec")):
        """
        Used to initialize an object of this class
        ARGS:
            self:   reference to the object calling this method (i.e. Java's THIS)
            dataArr:    List of Strings, each String is a measurement that will be parsed and stored in this object
            ThreadNum:  Integer, the number that this thread is (generally between 3 and 6)
            direction:  String, the direction of the data in this thread (UP or DOWN)
            units:      Tuple of two Strings, the units being used by the measurements
        """
        #Call the parent class' __init__
        Thread.__init__(self, dataArr=dataArr, threadNum=threadNum, direction=direction, units=units)
        #Parsing out the datagrams sent, and the server report (which is passed to the UDP_ServerReport object)
        for line in dataArr:
            #These two lines below check that the correct line is gotten.
            # First initialize an array of strings (which will be used as reference).
            # Next, for each elem in the array, check if it is in the line we are checking.
            #   (this is everything in the parenthesis)
            # Then, use all() on the returned array. The code in the parenthesis returns an array of
            #  booleans, and all() makes sure that they are all True.
            # If the conditions are met, this line is the line we are looking for.
            # If one of the strings was not found, then sadly, it means
            #  that these are not the droids we are looking for...
            # This was implemented because datagrams is in a few other lines, but not the ones we want
            strCheck = ["datagrams", "Sent"]
            if all([text in line for text in strCheck]):
                self.DatagramzSent = int(line.split("Sent ")[1].split(" ")[0])
            # If "Server Report" is in the line, we need the next line
            if "Server Report" in line:
                #The actual server report is the line below the current line, so we need to get
                # this current line's index, and add 1 to it
                tempIndex = dataArr.index(line) + 1
                #This uses list comprehension to get all of the lines pertaining to the Server Report.
                # Sometimes, there is more than one line in the Server Report
                serverReportLines = [line for line in dataArr[tempIndex:] if ("[ " in line)]
                #Passing the necessary lines to the Server Report constructor
                self.ServerReport = ServerReport(data=serverReportLines, units=units)
            #END IF/ELIF
        #END FOR
    #END DEF


# STRING PRINTOUT --------------------------------------------------------------

    def __str__(self):
        """Returns a String representation of the object"""
        string = (self.StringPadding +
                  "Thread Number: {}".format(self.ThreadNumber) + "\n" +
                  self.StringPadding +
                  "Data Direction: {}".format(self.DataDirection) + "\n" +
                  self.StringPadding +
                  "Local: {}:{}".format(self.LocalIP,self.LocalPort) + "\n" +
                  self.StringPadding +
                  "Server: {}:{}".format(self.ServerIP,self.ServerPort) + "\n" +
                  self.StringPadding +
                  "Datagrams Sent: {}".format(self.DatagramzSent) + "\n"
                  )
        for msmt in self.Measurements:
            string += str(msmt) +"\n"
        string += ( str(self.FinalMsmt) +"\n"+ str(self.ServerReport) +"\n" )
        return string
    #END DEF
#END CLASS

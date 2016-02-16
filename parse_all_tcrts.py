"""
----------------------------------------------------------------------------
parse_all_tcrts.py

Author:     Evan Schwander  eschwander@csumb.edu

Purpose:    This module parses trace route tests and outputs a csv
----------------------------------------------------------------------------
"""

import os
import sys
import shutil
import calendar
import glob
from PyFiles.FileParser._parserUtils.device_tester_table import table
from PyFiles.FileParser.TCRT_Test import TCRT_Test
from PyFiles.csvGeneration._csvUtils._csvHeaders_ import FieldTestHeaders as headers
import datetime


def main():

    #open csvs
    #file creation/opening happens here
    #daily file
    currentDate = currDate()
    dailyFile = open("./csvResults/" + currentDate + "_daily_tcrt_results.csv", 'a')
    if os.path.getsize("./csvResults/" + currentDate + "_daily_tcrt_results.csv") == 0:
        headers = str(getHeaders()).replace("'","").replace(" ","")[1:-1]
        dailyFile.write(headers + "\n")
    #all file
    allFile = open("./csvResults/all_tcrt_test_results.csv", 'a')
    if os.path.getsize("./csvResults/all_tcrt_test_results.csv") == 0:
        headers = str(getHeaders()).replace("'","").replace(" ","")[1:-1]
        allFile.write(headers + "\n")

    #parsing all tcrts
    for file in glob.glob(os.path.join("./UploadData/tcrt", '*.txt')):
        tocsv = Test()
        fs = open(file, 'rt')
        allLines = fs.readlines()
        fs.close()
        #shutil.move(file, "./ProcessedData")
        firstLine = str(allLines.pop(0))
        if "tablet" in firstLine.lower():
            tocsv.DeviceType = "Tablet"
        else:
            tocsv.DeviceType = "Phone"
        # This loop parses basic info
        while "Checking Connectivity" not in allLines[0]:
            tocsv.findBasicInfo(str(allLines.pop(0)))

        #Variable initialization for the following loop
        recording = False
        hops = ''
        tcrtTests = []
        destination = ''
        #The following loop records once it finds a certain delimiter
        #It then creates a TCRT_Test object once it reaches a different delimiter
        while "Saving" not in allLines[0]:
            if ": Traceroute" in allLines[0]: #delimiter 1
                #begin recording and set the destination
                recording = True
                destinationLine = allLines[0]
                if "Oregon" in destinationLine:
                    destination = "oregon"
                elif "West" in destinationLine:
                    destination = "california"
                elif "East" in destinationLine:
                    destination = "east"
                allLines.pop(0)
                allLines.pop(0)
            elif allLines[0] == "\n" and recording == True: #delimiter 2
                recording = False
                tcrtTests.append(TCRT_Test(hops, destination))
                hops = ''
            if recording:
                hops += allLines.pop(0)
            else:
                allLines.pop(0)

        #Here we build the "finalString" to write to the csv
        finalString = str(tocsv)
        # If there were no traceroutes, the network was unreachable
        if tcrtTests == []:
            finalString += "error: Network unreachable"
            #The following range is based off of the remaining spots in csv,
            #which is 362 = 40(max hops) *3(info in hops) *3(numberof tests) +3-1(hop count in each test minus 1)
            for i in range(0,362):
                if i == 120 or i == 241: # 120 and 241 are where the error messages should go
                    finalString += ",error: Network unreachable"
                else:
                    finalString += ",NA"
        else:
            #If for some reason there are less than 3 trace routes,
            # display the error that appeared in the last test
            if len(tcrtTests) < 3:
                for i in range(len(tcrtTests), 3):
                    tcrtTests.append(TCRT_Test("\nQuitting\n"))
            for x in tcrtTests:
                finalString += str(x)
            
        print(finalString)
    
        #write to appropriate csvs
        dailyFile.write(finalString + "\n")
        allFile.write(finalString + "\n")

        #move file to ProcessedData
        shutil.move(file, "./ProcessedData")

    #close csvs
    dailyFile.close()
    allFile.close()

def currDate():
        #Everything is finally written to a daily csv and an all tcrt results csv
        #But first we need to get the current date in the proper format
        currentDate = str(datetime.date.today())
        currentDate = currentDate.replace('-','_')
        currentDate += "_"
        convertDate = list(currentDate)
        convertDate.extend(currentDate[0:4])
        convertDate = convertDate[5:]
        currentDate = ''
        for x in convertDate:
            currentDate += x
        return currentDate

class Test:
    
    def __init__(self):
        self.Tester = 'NA'
        self.LocationID = 'NA'
        self.Date = 'NA'
        self.Time = 'NA'
        self.Provider = 'NA'
        self.Operator = 'NA'
        self.Network = 'NA'
        self.Latitude = 'NA'
        self.Longitude = 'NA'
        self.DeviceID = 'NA'
        self.DeviceType = 'NA'
 
    def findBasicInfo(self, dataString):
        if "Test started" in dataString:
            self.parseDateTime(dataString)
        elif "NetworkProvider:" in dataString:
            self.Provider = str(dataString.split(" ").pop())
        elif "NetworkOperator:" in dataString:
            self.Operator = str(dataString.split(" ").pop())
        elif "Device ID:" in dataString:
            self.DeviceID = str(dataString.split(" ").pop())
            self.determineTester(self.DeviceID)
        elif "Latitude:" in dataString:
            self.Latitude = str(dataString.split(":").pop())
        elif "Longitude:" in dataString:
            self.Longitude = str(dataString.split(":").pop())
        elif "ConnectionType:" in dataString:
            self.Network = str(dataString.split(" ").pop())
        elif "Location ID:" in dataString:
            self.LocationID = str(dataString.split(" ").pop())
        elif "Testing started" in dataString:
            self.parseDateTime(dataString)

    def parseDateTime(self, dataString):
        dataString = dataString.split(" ")
        year = dataString.pop()
        timezone = dataString.pop()
        time = dataString.pop() 
        day = dataString.pop()
        monthAbbr = dataString.pop()
        month = list(calendar.month_abbr).index(monthAbbr)
        self.Date = str(month) + "/" + str(day) + "/" + str(year)
        self.Time = time

    def determineTester(self, id):
        pairs = table.rsplit()
        id = str(id.rsplit()[0])
        flag = False
        for pair in pairs:
            if id in str(pair):
                flag = True
            elif flag:
                self.Tester = "Tester " + str(pair)
                break

    def __str__(self):
        ''' returns string in the form of a csv '''
        csv = ''
        csv += self.Tester + "," + self.LocationID + "," + self.Date + "," + self.Time + "," + self.Provider + "," 
        csv += self.Operator + "," + self.Network + "," + self.Latitude + "," + self.Longitude + ","
        csv += self.DeviceID + "," + self.DeviceType + ","
        csv = csv.replace('\n','')
        return csv



#def parseTCRT(self, dataString):
    

'''
The following mess is the headers for csv files created by this script.
These headers also exist in PyFiles/csvGeneration/_csvUtils/_csvHeaders_.py,
    but importing them is a pain
'''
def getHeaders():
    FieldTestHeaders = []
    FieldTestHeaders.extend(headers["csv Default Headers"])
    FieldTestHeaders.extend(headers["csv TCRT Headers"])
    return FieldTestHeaders


main()
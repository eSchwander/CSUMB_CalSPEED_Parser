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
import datetime


def main():

    for file in glob.glob(os.path.join("./UploadData/tcrt", '*.txt')):
        tocsv = Test()
        fs = open(file, 'r')
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
        #The following loop records once it finds a certain delimiter
        #It then creates a TCRT_Test object once it reaches a different delimiter
        while "Saving" not in allLines[0]:
            if "traceroute to" in allLines[0]: #delimiter 1
                recording = True
            elif allLines[0] == "\n" and recording == True: #delimiter 2
                recording = False
                tcrtTests.append(TCRT_Test(hops))
                hops = ''
            if recording:
                hops += allLines.pop(0)
            else:
                allLines.pop(0)

        #Here we build the "finalString" to write to the csv
        finalString = str(tocsv)
        if tcrtTests == []:
            finalString += "error: network unreachable"
            #This range is based off of the remaining spots in csv
            #which is 362 = 40(max hops) *3(info in hops) *3(numberof tests) +3-1(hop count in each test minus 1)
            for i in range(0,362):
                finalString += ",NA"
        else:
            for x in tcrtTests:
                finalString += str(x)
        
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
        #file creation and writing happens here
        #daily file
        dailyFile = open("./csvResults/" + currentDate + "_daily_tcrt_results.csv", 'a')
        if os.path.getsize("./csvResults/" + currentDate + "_daily_tcrt_results.csv") == 0:
            headers = str(getHeaders()).replace("'","").replace(" ","")[2:-2]
            dailyFile.write(headers + "\n")
        dailyFile.write(finalString + "\n")
        dailyFile.close()
        #all tcrts file
        allFile = open("./csvResults/all_tcrt_test_results.csv", 'a')
        if os.path.getsize("./csvResults/all_tcrt_test_results.csv") == 0:
            headers = str(getHeaders()).replace("'","").replace(" ","")[2:-2]
            allFile.write(headers + "\n")
        allFile.write(finalString + "\n")
        allFile.close()

        #move file to ProcessedData
        shutil.move(file, "./ProcessedData")


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
                self.Tester = pair
                break

    def __str__(self):
        ''' returns string in the form of a csv '''
        csv = ''
        csv += self.Tester + "," + self.LocationID + "," + self.Date + "," + self.Time + "," + self.Provider + "," 
        csv += self.Operator + "," + self.Network + "," + self.Latitude + "," + self.Longitude + ","
        csv += self.DeviceID + "," + self.DeviceType + ","
        return csv.replace('\n','')



#def parseTCRT(self, dataString):
    

'''
The following mess is the headers for csv files created by this script.
These headers also exist in PyFiles/csvGeneration/_csvUtils/_csvHeaders_.py,
    but importing them is a pain
'''
def getHeaders():
    FieldTestHeaders = []
    FieldTestHeaders.append(["Tester", "LocationID", "Date", "Time", "Provider", "Operator",
             "Network", "Latitude", "Longitude", "DeviceID", "DeviceType",
             "cwTr_hops",
             "cwTrH1Nm", "cwTrH1IP", "cwTrH1D",
             "cwTrH2Nm", "cwTrH2IP", "cwTrH2D",
             "cwTrH3Nm", "cwTrH3IP", "cwTrH3D",
             "cwTrH4Nm", "cwTrH4IP", "cwTrH4D",
             "cwTrH5Nm", "cwTrH5IP", "cwTrH5D",
             "cwTrH6Nm", "cwTrH6IP", "cwTrH6D",
             "cwTrH7Nm", "cwTrH7IP", "cwTrH7D",
             "cwTrH8Nm", "cwTrH8IP", "cwTrH8D",
             "cwTrH9Nm", "cwTrH9IP", "cwTrH9D",
             "cwTrH10Nm", "cwTrH10IP", "cwTrH10D",
             "cwTrH11Nm", "cwTrH11IP", "cwTrH11D",
             "cwTrH12Nm", "cwTrH12IP", "cwTrH12D",
             "cwTrH13Nm", "cwTrH13IP", "cwTrH13D", 
             "cwTrH14Nm", "cwTrH14IP", "cwTrH14D", 
             "cwTrH15Nm", "cwTrH15IP", "cwTrH15D", 
             "cwTrH16Nm", "cwTrH16IP", "cwTrH16D", 
             "cwTrH17Nm", "cwTrH17IP", "cwTrH17D", 
             "cwTrH18Nm", "cwTrH18IP", "cwTrH18D", 
             "cwTrH19Nm", "cwTrH19IP", "cwTrH19D", 
             "cwTrH20Nm", "cwTrH20IP", "cwTrH20D", 
             "cwTrH21Nm", "cwTrH21IP", "cwTrH21D",
             "cwTrH22Nm", "cwTrH22IP", "cwTrH22D",
             "cwTrH23Nm", "cwTrH23IP", "cwTrH23D", 
             "cwTrH24Nm", "cwTrH24IP", "cwTrH24D", 
             "cwTrH25Nm", "cwTrH25IP", "cwTrH25D", 
             "cwTrH26Nm", "cwTrH26IP", "cwTrH26D", 
             "cwTrH27Nm", "cwTrH27IP", "cwTrH27D", 
             "cwTrH28Nm", "cwTrH28IP", "cwTrH28D", 
             "cwTrH29Nm", "cwTrH29IP", "cwTrH29D", 
             "cwTrH30Nm", "cwTrH30IP", "cwTrH30D", 
             "cwTrH31Nm", "cwTrH31IP", "cwTrH31D", 
             "cwTrH32Nm", "cwTrH32IP", "cwTrH32D", 
             "cwTrH33Nm", "cwTrH33IP", "cwTrH33D", 
             "cwTrH34Nm", "cwTrH34IP", "cwTrH34D", 
             "cwTrH35Nm", "cwTrH35IP", "cwTrH35D", 
             "cwTrH36Nm", "cwTrH36IP", "cwTrH36D", 
             "cwTrH37Nm", "cwTrH37IP", "cwTrH37D",
             "cwTrH38Nm", "cwTrH38IP", "cwTrH38D",
             "cwTrH39Nm", "cwTrH39IP", "cwTrH39D",
             "cwTrH40Nm", "cwTrH40IP", "cwTrH40D",
             "eTr_hops",
             "eTrH1Nm", "eTrH1IP", "eTrH1D",
             "eTrH2Nm", "eTrH2IP", "eTrH2D",
             "eTrH3Nm", "eTrH3IP", "eTrH3D",
             "eTrH4Nm", "eTrH4IP", "eTrH4D",
             "eTrH5Nm", "eTrH5IP", "eTrH5D",
             "eTrH6Nm", "eTrH6IP", "eTrH6D",
             "eTrH7Nm", "eTrH7IP", "eTrH7D",
             "eTrH8Nm", "eTrH8IP", "eTrH8D",
             "eTrH9Nm", "eTrH9IP", "eTrH9D",
             "eTrH10Nm", "eTrH10IP", "eTrH10D",
             "eTrH11Nm", "eTrH11IP", "eTrH11D",
             "eTrH12Nm", "eTrH12IP", "eTrH12D",
             "eTrH13Nm", "eTrH13IP", "eTrH13D", 
             "eTrH14Nm", "eTrH14IP", "eTrH14D", 
             "eTrH15Nm", "eTrH15IP", "eTrH15D", 
             "eTrH16Nm", "eTrH16IP", "eTrH16D", 
             "eTrH17Nm", "eTrH17IP", "eTrH17D", 
             "eTrH18Nm", "eTrH18IP", "eTrH18D", 
             "eTrH19Nm", "eTrH19IP", "eTrH19D", 
             "eTrH20Nm", "eTrH20IP", "eTrH20D", 
             "eTrH21Nm", "eTrH21IP", "eTrH21D",
             "eTrH22Nm", "eTrH22IP", "eTrH22D",
             "eTrH23Nm", "eTrH23IP", "eTrH23D", 
             "eTrH24Nm", "eTrH24IP", "eTrH24D", 
             "eTrH25Nm", "eTrH25IP", "eTrH25D", 
             "eTrH26Nm", "eTrH26IP", "eTrH26D", 
             "eTrH27Nm", "eTrH27IP", "eTrH27D", 
             "eTrH28Nm", "eTrH28IP", "eTrH28D", 
             "eTrH29Nm", "eTrH29IP", "eTrH29D", 
             "eTrH30Nm", "eTrH30IP", "eTrH30D", 
             "eTrH31Nm", "eTrH31IP", "eTrH31D", 
             "eTrH32Nm", "eTrH32IP", "eTrH32D", 
             "eTrH33Nm", "eTrH33IP", "eTrH33D", 
             "eTrH34Nm", "eTrH34IP", "eTrH34D", 
             "eTrH35Nm", "eTrH35IP", "eTrH35D", 
             "eTrH36Nm", "eTrH36IP", "eTrH36D", 
             "eTrH37Nm", "eTrH37IP", "eTrH37D",
             "eTrH38Nm", "eTrH38IP", "eTrH38D",
             "eTrH39Nm", "eTrH39IP", "eTrH39D",
             "eTrH40Nm", "eTrH40IP", "eTrH40D",
             "owTr_hops",
             "owTrH1Nm", "owTrH1IP", "owTrH1D",
             "owTrH2Nm", "owTrH2IP", "owTrH2D",
             "owTrH3Nm", "owTrH3IP", "owTrH3D",
             "owTrH4Nm", "owTrH4IP", "owTrH4D",
             "owTrH5Nm", "owTrH5IP", "owTrH5D",
             "owTrH6Nm", "owTrH6IP", "owTrH6D",
             "owTrH7Nm", "owTrH7IP", "owTrH7D",
             "owTrH8Nm", "owTrH8IP", "owTrH8D",
             "owTrH9Nm", "owTrH9IP", "owTrH9D",
             "owTrH10Nm", "owTrH10IP", "owTrH10D",
             "owTrH11Nm", "owTrH11IP", "owTrH11D",
             "owTrH12Nm", "owTrH12IP", "owTrH12D",
             "owTrH13Nm", "owTrH13IP", "owTrH13D", 
             "owTrH14Nm", "owTrH14IP", "owTrH14D", 
             "owTrH15Nm", "owTrH15IP", "owTrH15D", 
             "owTrH16Nm", "owTrH16IP", "owTrH16D", 
             "owTrH17Nm", "owTrH17IP", "owTrH17D", 
             "owTrH18Nm", "owTrH18IP", "owTrH18D", 
             "owTrH19Nm", "owTrH19IP", "owTrH19D", 
             "owTrH20Nm", "owTrH20IP", "owTrH20D", 
             "owTrH21Nm", "owTrH21IP", "owTrH21D",
             "owTrH22Nm", "owTrH22IP", "owTrH22D",
             "owTrH23Nm", "owTrH23IP", "owTrH23D", 
             "owTrH24Nm", "owTrH24IP", "owTrH24D", 
             "owTrH25Nm", "owTrH25IP", "owTrH25D", 
             "owTrH26Nm", "owTrH26IP", "owTrH26D", 
             "owTrH27Nm", "owTrH27IP", "owTrH27D", 
             "owTrH28Nm", "owTrH28IP", "owTrH28D", 
             "owTrH29Nm", "owTrH29IP", "owTrH29D", 
             "owTrH30Nm", "owTrH30IP", "owTrH30D", 
             "owTrH31Nm", "owTrH31IP", "owTrH31D", 
             "owTrH32Nm", "owTrH32IP", "owTrH32D", 
             "owTrH33Nm", "owTrH33IP", "owTrH33D", 
             "owTrH34Nm", "owTrH34IP", "owTrH34D", 
             "owTrH35Nm", "owTrH35IP", "owTrH35D", 
             "owTrH36Nm", "owTrH36IP", "owTrH36D", 
             "owTrH37Nm", "owTrH37IP", "owTrH37D",
             "owTrH38Nm", "owTrH38IP", "owTrH38D",
             "owTrH39Nm", "owTrH39IP", "owTrH39D",
             "owTrH40Nm", "owTrH40IP", "owTrH40D"])
    return FieldTestHeaders


main()
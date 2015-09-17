#!/usr/local/bin/python3
"""
------------------------------------------------------------------------
_CSV HEADERS.PY

AUTHOR(S):     Peter Walker    pwalker@csumb.edu
                Evan Schwander  eschwander@csumb.edu

PURPOSE-  This file holds a number of variables that will be used
            by the csvDataExtractor ad csvGenerator
------------------------------------------------------------------------
"""
if __name__=="__main__":
    raise SystemExit

'''
Headers for the CSV file creation
 1  csv Default Headers     The basic file information always included in the csv
 2  csv Extra Headers       Other extra information not usually calculated
 3  csv PING Headers        PING test statistics at end of test
 4  csv RvMos Headers       R-value and MOS score based on PING test values
 5  csv UDP Headers         Jitter and Loss from server report, Time is test interval time
 6  csv TCP Headers         Sum of final measurement's speed from all threads
 7  csv Stat Headers        StDev and Median information from TCP tests
 8  csv Stat-C Headers      StDev and Median information from
                              TCP tests combined into one dataset
 9  csv Stat-A Headers      The average, standard deviation and (mean - 1 pstdev) for all
                              TCP tests combined, separated by data direction
10  csv Qual Headers        TCP Quality. PR is average total download time. Pct is a value from
                              0-1 representing number of measurements that had non-zero values
'''
FTcsvHeadersOrder = ["csv Default Headers",
                     "csv Extra Headers",
                     "csv PING Headers",
                     "csv RvMos Headers",
                     "csv UDP Headers",
                     "csv TCP Headers",
                     "csv Stat Headers",
                     "csv Stat-S Headers",
                     "csv Stat-A Headers",
                     "csv Qual Headers" ]
CScsvHeadersOrder = FTcsvHeadersOrder[:]
# CScsvHeadersOrder = ["csv Default Headers",
#                      "csv Extra Headers",
#                      "csv PING Headers",
#                      "csv RvMos Headers",
#                      "csv UDP Headers",
#                      "csv TCP Headers",
#                      "csv Stat Headers",
#                      "csv Stat-S Headers",
#                      "csv Stat-A Headers",
#                      "csv Qual Headers" ]

"""
Adding new types of analyses requires modifying three files.
In this file, add a new list element to FTcsvHeadersOrder or CScsvHeadersOrder. Then,
  in the appropriate dictionary below (or both), add your new list of column headers.

In the csvDataExtractor.py file, add a new function to the csvDataExtractor class,
  using the algorithm you wish to generate and return the necessary values.
In the csvGenerator.py file, add the name of the function created in csvDataExtractor
  to the dictionary OPTS, giving it the appropriate index number. The order of functions should
  match the numbers in the docstring at the beginning of this file.

CURRENT FUNCTIONS:
    extractDefaultVals
    extractExtraVals
    extractPINGVals
    extractRValMOSVals
    extractUDPVals
    extractTCPVals
    extractTCPStatVals
    extractTCPStatSVals
    extractTCPStatAVals
    extractTCPQualVals
"""








# The Field Test CSV Headers
#'''
#-------------- The OLD Column Order --------------#
FieldTestHeaders = {}
FieldTestHeaders["csv Default Headers"] = \
        ["Tester", "LocationID", "Date", "Time", "Provider", "Operator",
         "Network", "Latitude", "Longitude", "DeviceID", "DeviceType",
         "wDownNS", "wDownSD", "wDownHD",
         "wUpNS", "wUpSD", "wUpHD",
         "eDownNS", "eDownSD", "eDownHD",
         "eUpNS", "eUpSD", "eUpHD",
         "wVideo", "eVideo", "wConference", "eConference"]
FieldTestHeaders["csv Extra Headers"] = \
        ["Census2010", "R5Coverage", "NormalLAT", "NormalLONG"]
FieldTestHeaders["csv PING Headers"] = \
        ["eRttMin", "eRttMax", "eRttAvg", "eRttLoss",
         "wRttMin", "wRttMax", "wRttAvg", "wRttLoss" ]
FieldTestHeaders["csv RvMos Headers"] = \
        ["eRVal", "eMOS", "wRVal", "wMOS" ]
FieldTestHeaders["csv UDP Headers"] = \
        ["wUDPJit1", "wUDPLoss1", "wUDPTime1", "wUDPJit2", "wUDPLoss2", "wUDPTime2",
         "wUDPJit3", "wUDPLoss3", "wUDPTime3",
         "eUDPJit1", "eUDPLoss1", "eUDPTime1", "eUDPJit2", "eUDPLoss2", "eUDPTime2",
         "eUDPJit3", "eUDPLoss3", "eUDPTime3",
         "wUDPJit4", "wUDPLoss4", "wUDPTime4", "eUDPJit4", "eUDPLoss4", "eUDPTime4" ]
FieldTestHeaders["csv TCP Headers"] = \
        ["wTCPUp1", "wTCPDown1", "eTCPUp1", "eTCPDown1",
         "wTCPUp2", "wTCPDown2", "eTCPUp2", "eTCPDown2" ]
FieldTestHeaders["csv Stat Headers"] = \
        ["wUpStdDev1", "wUpMedian1", "wDnStdDev1", "wDnMedian1",
         "eUpStdDev1", "eUpMedian1", "eDnStdDev1", "eDnMedian1",
         "wUpStdDev2", "wUpMedian2", "wDnStdDev2", "wDnMedian2",
         "eUpStdDev2", "eUpMedian2", "eDnStdDev2", "eDnMedian2" ]
FieldTestHeaders["csv Stat-S Headers"] = \
        ["sUpMean", "sUpStdDev", "sUpMean_1",
         "sDnMean", "sDnStdDev", "sDnMean_1" ]
FieldTestHeaders["csv Stat-A Headers"] = \
        ["aUpMean", "aUpStdDev", "aUpMean_1",
         "aDnMean", "aDnStdDev", "aDnMean_1" ]

# This overrides the headers in Stat-S, as we are going to, in general, use the
# algorithm specified in the corresponding function in csvDataExtractor
FieldTestHeaders["csv Stat-S Headers"] = \
        ["cUpMean", "cUpStdDev", "cUpMean_1",
         "cDnMean", "cDnStdDev", "cDnMean_1" ]
#

FieldTestHeaders["csv Qual Headers"] = \
        ["wTCPUpPR1", "wTCPUpPct1", "wTCPDnPR1", "wTCPDnPct1",
         "eTCPUpPR1", "eTCPUpPct1", "eTCPDnPR1", "eTCPDnPct1",
         "wTCPUpPR2", "wTCPUpPct2", "wTCPDnPR2", "wTCPDnPct2",
         "eTCPUpPR2", "eTCPUpPct2", "eTCPDnPR2", "eTCPDnPct2" ]

# Traceroute headers. Includes California, Oregon, and East Coast tests.
FieldTestHeaders["csv TCRT Headers"] = \
        ["cwTr_hops",
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
         "owTrH40Nm", "owTrH40IP", "owTrH40D"]







'''
#-------------- The Better Column Order --------------#
#This column order is currently not being used. As we are using the older column
# order, the csvDataExtractor functions need to shuffle the order of values to
# reflect the column header order above. If the new column order below is used,
# then those hacks can be removed.

FieldTestHeaders = {}
FieldTestHeaders["csv Default Headers"] = \
        ["Tester", "LocationID", "Date", "Time", "Provider", "Operator",
         "Network", "Latitude", "Longitude", "DeviceID", "DeviceType"]
FieldTestHeaders["csv Extra Headers"] = \
        ["Census2010", "R5Coverage", "NormalLAT", "NormalLONG" ]
FieldTestHeaders["csv PING Headers"] = \
        ["wRttMin", "wRttMax", "wRttAvg", "wRttLoss",
         "eRttMin", "eRttMax", "eRttAvg", "eRttLoss" ]
FieldTestHeaders["csv RvMos Headers"] = \
        ["wRVal", "wMOS", "eRVal", "eMOS" ]
FieldTestHeaders["csv UDP Headers"] = \
        ["wUDPJit1", "wUDPLoss1", "wUDPTime1", "wUDPJit2", "wUDPLoss2", "wUDPTime2",
         "wUDPJit3", "wUDPLoss3", "wUDPTime3",
         "eUDPJit1", "eUDPLoss1", "eUDPTime1", "eUDPJit2", "eUDPLoss2", "eUDPTime2",
         "eUDPJit3", "eUDPLoss3", "eUDPTime3",
         "wUDPJit4", "wUDPLoss4", "wUDPTime4", "eUDPJit4", "eUDPLoss4", "eUDPTime4" ]
FieldTestHeaders["csv TCP Headers"] = \
        ["wTCPUp1", "wTCPDown1", "wTCPUp2", "wTCPDown2",
         "eTCPUp1", "eTCPDown1", "eTCPUp2", "eTCPDown2" ]
FieldTestHeaders["csv Stat Headers"] = \
        ["wUpStdDev1", "wUpMedian1", "wDnStdDev1", "wDnMedian1",
         "wUpStdDev2", "wUpMedian2", "wDnStdDev2", "wDnMedian2",
         "eUpStdDev1", "eUpMedian1", "eDnStdDev1", "eDnMedian1",
         "eUpStdDev2", "eUpMedian2", "eDnStdDev2", "eDnMedian2" ]
FieldTestHeaders["csv Stat-S Headers"] = \
        ["cUpMean", "cUpStdDev", "cUpMean_1",
         "cDnMean", "cDnStdDev", "cDnMean_1" ]
FieldTestHeaders["csv Stat-A Headers"] = \
        ["aUpMean", "aUpStdDev", "aUpMean_1",
         "aDnMean", "aDnStdDev", "aDnMean_1" ]
FieldTestHeaders["csv Qual Headers"] = \
        ["wTCPUpPR1", "wTCPUpPct1", "wTCPDnPR1", "wTCPDnPct1",
         "wTCPUpPR2", "wTCPUpPct2", "wTCPDnPR2", "wTCPDnPct2",
         "eTCPUpPR1", "eTCPUpPct1", "eTCPDnPR1", "eTCPDnPct1",
         "eTCPUpPR2", "eTCPUpPct2", "eTCPDnPR2", "eTCPDnPct2" ]
#'''








# The Crowd Source CSV Headers. The groups of headers, however, follow the same
# basic structure as in the FieldTest headers.
CrowdSourceHeaders = {}
CrowdSourceHeaders["csv Default Headers"] = \
        ["Date", "Time", "AppVersion", "Environ", "Ph_Model", "Ph_Manufac",
         "Ph_API", "Ph_SDK", "Provider", "Operator", "Network", "Roaming",
         #"Wifi_BSSID",
         "Wifi_SSID", "LocSource", "Latitude", "Longitude",
         "MovingDist", "DeviceType"]
CrowdSourceHeaders["csv Extra Headers"] = []
CrowdSourceHeaders["csv PING Headers"] = \
        ["wRttMin", "wRttMax", "wRttAvg", "wRttLoss",
         "eRttMin", "eRttMax", "eRttAvg", "eRttLoss" ]
CrowdSourceHeaders["csv RvMos Headers"] = \
        ["wRVal", "wMOS", "eRVal", "eMOS" ]
CrowdSourceHeaders["csv UDP Headers"] = \
        ["wUDPJit", "wUDPLoss", "wUDPTime", "eUDPJit", "eUDPLoss", "eUDPTime" ]
CrowdSourceHeaders["csv TCP Headers"] = \
        ["wTCPUp", "wTCPDown", "eTCPUp", "eTCPDown" ]
CrowdSourceHeaders["csv Stat Headers"] = \
        ["wUpStdDev", "wUpMedian", "wDnStdDev", "wDnMedian",
         "eUpStdDev", "eUpMedian", "eDnStdDev", "eDnMedian" ]
CrowdSourceHeaders["csv Stat-S Headers"] = \
        ["cUpMean", "cUpStdDev", "cUpMean_1",
         "cDnMean", "cDnStdDev", "cDnMean_1" ]
CrowdSourceHeaders["csv Stat-A Headers"] = \
        ["aUpMean", "aUpStdDev", "aUpMean_1",
         "aDnMean", "aDnStdDev", "aDnMean_1" ]
CrowdSourceHeaders["csv Qual Headers"] = \
        ["wTCPUpPR", "wTCPUpPct", "wTCPDnPR", "wTCPDnPct",
         "eTCPUpPR", "eTCPUpPct", "eTCPDnPR", "eTCPDnPct" ]

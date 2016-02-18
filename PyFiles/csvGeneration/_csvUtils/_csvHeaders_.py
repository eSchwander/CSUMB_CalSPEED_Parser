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
                     "csv Qual Headers"]
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
         "Network", "Latitude", "Longitude", "DeviceID", "DeviceType"]
FieldTestHeaders["csv Video Metrics Headers"] = \
        ["wDownNS", "wDownSD", "wDownHD", "wDownVideo",
         "wUpNS", "wUpSD", "wUpHD", "wUpVideo",
         "wConference",
         "eDownNS", "eDownSD", "eDownHD", "eDownVideo",
         "eUpNS", "eUpSD", "eUpHD", "eUpVideo",
         "eConference"]
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
#FieldTestHeaders["csv Stat-S Headers"] = \
#        ["sUpMean", "sUpStdDev", "sUpMean_1",
#         "sDnMean", "sDnStdDev", "sDnMean_1" ]
FieldTestHeaders["csv Stat-A Headers"] = \
        ["aUpMean", "aUpStdDev", "aUpMean_1",
         "aDnMean", "aDnStdDev", "aDnMean_1" ]

# This overrides the headers in Stat-S, as we are going to, in general, use the
# algorithm specified in the corresponding function in csvDataExtractor
FieldTestHeaders["csv Stat-S Headers"] = \
        ["cUpMean", "cUpStdDev", "cUpMean_1", "cUpMean_2",
         "cDnMean", "cDnStdDev", "cDnMean_1", "cDnMean_2" ]
#

FieldTestHeaders["csv Qual Headers"] = \
        ["wTCPUpPR1", "wTCPUpPct1", "wTCPDnPR1", "wTCPDnPct1",
         "eTCPUpPR1", "eTCPUpPct1", "eTCPDnPR1", "eTCPDnPct1",
         "wTCPUpPR2", "wTCPUpPct2", "wTCPDnPR2", "wTCPDnPct2",
         "eTCPUpPR2", "eTCPUpPct2", "eTCPDnPR2", "eTCPDnPct2",
         "wDownNS", "wDownSD", "wDownHD", "wDownVideo",
         "wUpNS", "wUpSD", "wUpHD", "wUpVideo",
         "wConference",
         "eDownNS", "eDownSD", "eDownHD", "eDownVideo",
         "eUpNS", "eUpSD", "eUpHD", "eUpVideo",
         "eConference" ]


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

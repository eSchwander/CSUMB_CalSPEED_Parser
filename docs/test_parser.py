#!/usr/local/bin/python3
"""
----------------------------------------------------------------
This file is for testing batches of file, to see if the parser is
working correctly. This is mainly to check if a file causes an exception
or problem, and not if the data is fully parsed in.

AUTHOR:     Peter Walker
DATE:       Nov 23, 2014
----------------------------------------------------------------
"""


def main():
    """
    This script can be run as __main__ by a user. If they do not give the necessary
    inputs from the comamnd line, then the script will not run.
    """
    import sys
    import os
    if ("-h" in sys.argv) or \
            ("--help" in sys.argv) or \
            len(sys.argv) > 2 or \
            len(sys.argv) < 2:
        print("Call this script with a folder path as the second argument.")
        raise SystemExit
    #END IF

    #This takes care of the problem of having to run the script from within the
    # folder the contains it. This will dynamically add the project path to Python's
    # sys.path array.
    #Overwrite this variable with the correct path for your system
    projectPath = "/Users/peterwalker/Documents/GitHub/CSUMB_CalSPEED_Parser/PyFiles/"
    sys.path.append(projectPath)

    #Now we import the _File objects
    from FileParser.FieldTest_File import FieldTest_File
    from FileParser.CrowdSource_File import CrowdSource_File
    #END IF/ELSE


    #Now, we start actually determining the path that the user has given us, and from there
    # which files we need to import
    fullPath = os.path.realpath(sys.argv[-1])
    if not os.path.isdir(fullPath):
        fullPath = os.path.dirname(fullPath)
    print("Using files in : {}\n".format(fullPath))

    #Parsing all of the files, and putting them into an array
    parsedFiles = {"FieldTest":   []
                   "CrowdSource": [] }
    for file in os.listdir(fullPath):
        truePath = os.path.join(fullPath, file)
        #We try parsing the file with both kinds, and if there is an error, then
        # we simply pass it.
        file = FieldTest_File(filePath=truePath)
        if file:
            parsedFiles["FieldTest"].append( file )
        else:
            file = CrowdSource_File(filePath=truePath)
            if file:
                parsedFiles["CrowdSource"].append( file )
        #END IF/ELSE
    #END FOR

    #os.path.expanduser takes the "~" as a placeholder for my home directoy, and
    # returns the absolute path. This is then appended with /Desktop/output.txt, which
    # is where the output will be saved
    num = 1
    outputPath = os.path.expanduser("~") + "/Desktop/output_"+str(num)+".txt"
    while os.path.isfile(outputPath):
        num += 1
        outputPath = os.path.expanduser("~") + "/Desktop/output_"+str(num)+".txt"
    #Now that we've found a path that has not been used, we can print out all of the test
    # into it for error checking
    with open(outputPath,"w") as newfile:
        newfile.write("Used files located in: "+fullPath+"\n")
        newfile.write(str(len(parsedFiles))+" files were read and parsed without error.\n\n")
        for type_ in ["FieldTest", "CrowdSource"]:
            for file in parsedFiles[type_]:
                if file:
                    output = (file.Filename+"\n"+
                              "----------------------------------------\n")
                    output += file._str_short()
                    output += ( ("="*100) + "\n" +
                                ("="*100) + "\n\n\n" )
                    newfile.write(output)
                #END IF
            #END FOR
        #END FOR
    #END WITH FILE
    print("Output File has been made at "+outputPath)

    print("Now exiting....")
    return True
#END MAIN

if __name__ == "__main__":
    main()

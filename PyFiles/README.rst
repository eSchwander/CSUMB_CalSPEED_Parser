CSUMB's CPUC Project - Raw Text File Parser
============================================

This project consists of a parser object, located in PyFiles/FileParser.
Based on the type of raw data that one needs to parse, import FieldTest_File or
CrowdSource_File.

Each object takes a string, the path to the file you would like parsed.


--------------------------------------------
SAMPLE USE:

from FileParser.FieldTest_File import FieldTest_File
parsedFile = FieldTest_File("/path/to/raw/file")


--------------------------------------------
Please refer to Github Pages webpage for more information.
http://pwalker91.github.io/CSUMB_CalSPEED_Parser/

CSUMB's CPUC Project - Raw Text File Parser
============================================

This project consists of a parser object, located in PyObjects.
Based on the type of raw data that one needs to parse, import FieldTest_File or
CrowdSource_File.

Each object takes a string, the path to the file you would like parsed.


--------------------------------------------
SAMPLE USE:

from FileParser.FieldTest_File import FieldTest_File
parsedFile = FieldTest_File("/path/to/raw/file")


--------------------------------------------
This code was "forked" from my previous project at
https://github.com/pwalker91/CPUC--iPerfParser_with_DB_Storage. This was forked
after the November 1st, 2014 Commit.

Please refer to Github Pages webpage for more information.
http://pwalker91.github.io/CSUMB_CPUC-Test-Parser/

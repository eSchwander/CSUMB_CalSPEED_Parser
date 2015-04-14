Hello, and welcome to the docs folder!
SECTIONS:
	My Setup
	Project Repo Setup
	Simple Usage
	Parser Setup
	CSV Generation Setup (and other extraneous classes)
	Server Script Setup



--------------------------------------------------------------------------------

MY SETUP:
	  As I work on this project, my work station is as follows…
		Atom (text editor)
		Mac OSX Terminal (Command Line)
		Cyberduck (SFTP GUI Client)
		Sourcetree (Version Control)
	  I prefer to keep my code writing and testing areas separate, hence the use
	Atom and Terminal, rather than a complete IDE like Eclipse
	  When I am testing new code, I prefer to copy the edited files into a
	separate directory on my desktop. This is mainly for convenience, as I don't
	like having a number of pycache folders in the project folder.



PROJECT REPO SETUP:
	  The repository setup is meant to group similar files together. To that
	effect, the Python scripts are in the folder ServerScripts. These scripts
	are meant to be run on the live servers for the Field Test area of the CPUC
	project, or for the Crowd Source area of the CPUC project.
		  I define a Python script as something that runs from start to finish
		without asking for user input (or much, at least), and has a specific
		purpose that it fills.
	  The other folder in this repository is the PyFiles folder. This is where
	all of the class files live.
		 Class files are ones that define Python classes, which are structures
		designed to hold data in a specific way, and have interfaces for getting
		the data it holds.
	  TLDR; Two folders (PyFiles and ServerScripts), one holds Python classes,
	the other holds Python scripts



SIMPLE USAGE:
	  The file parser can be used by importing either the FieldTest_File class
	from FieldTest_File.py, or the CrowdSource_File class.
	ex.  from FieldTestFile import FieldTest_File
	  The reason for the funny repetition is that the first "FieldTest_File" is
	the name of the file, and the second "FieldTest_File" is the name of the
	class.
	  Once you import the required class, you then instantiate the object with
	the path to a file.
	ex.  newFile = FieldTest_File("/my/path/to/some/file.txt")
	  If the file is an actual Field Test file (or Crowd Source file, depending
	on the class you used), then an object will be returned. Otherwise, a None
	type object is returned.

	  The CSV generator can be used by importing the necessary class.
	ex.  from csvGenerator import csvGenerator
	You then instantiate an instance, passing in the type of files that will be
	given to the generator. Currently, the accepted types are 'fieldtest' and
	'crowdsource'. An optional argument is the path to the FileParser folder
	(which contains the file parser classes), which needs to be passed in via
	the keyword 'FileParserPath'.
		  Once you've created a CSV generator, you can pass it individual files,
		or a folder containing files. The function names are pushFile(), and
		pushAllFiles(). Some optional keyword arguments are 'ArchiveDirectory'
		and 'ErrorDirectory', which are the paths to a directory where parsed
		files are copied, or where files that cause an error are copied.
		  To actually create a CSV (or append to it), use the function
		importCSV(), which takes the path to a CSV file, and the index name you
		wish it to be stored as in the object. The CSV file can be created
		beforehand. If it is not, it will be created during processing.
		  Now that you have a CSV generator with files imported and a CSV
		imported, you simply need to call exportCSV(), with the index value you
		gave the CSV during importCSV() and the path to save the file at.
		While exporting the CSV, the generator object will extract the necessary
		values from the parsed files stored in the object, add the values to
		the CSV, and write the CSV file.
		TLDR; 1-Create a CSV Generator. 2-Add parsed files with pushFile or
		pushAllFiles. 3-Import a CSV file with importCSV(). 4-Create the CSV
		file with exportCSV()



PARSER SETUP:
	  .



CSV GENERATOR SETUP (and other extraneous classes):
	  .



SERVER SCRIPT SETUP:
	  .

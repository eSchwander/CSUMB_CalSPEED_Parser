Hi, this is Evan. 
If you are searching for Peter's documentation, scroll down a little.

HOW TO USE:
	  After downloading, put some files you want parsed in the /UploadData
	folder. Next run determine_test.py from the terminal. The parser then parses
	all the files in UploadData and puts a csv in /csvGeneration. It probably 
	will not work on your first try because there are some files you will need 
	to put in the _sensitiveInfo files scattered through this project. This is a
	problem that I will attempt to address. If this works on the first try, 
	chances are I have fixed it and have not updated this.
	  Something to keep in mind. The trace route and speed test portions of this
	projects were handled by two different people. What determine_test.py 
	actually does is run parse_all_tcrts.py on trace route files and
	sort_and_extract.py on all speed test files. sort_and_extract.py likes to 
	send out emails so if you want to just want to test out the speed test 
	portion of this project you can run test_parser.py in this folder.
	
  If you are looking for some good documentation of what the speed test parser
take a look over here: 
http://pwalker91.github.io/CSUMB_CalSPEED_Parser/ProjectDocumentation.html

(The following is Peter's documentation)
--------------------------------------------------------------------------------
Hello, and welcome to the docs folder!
SECTIONS:
	My Setup
	Project Repo Setup
	Simple Usage
	Parser Setup
	CSV Generation Setup (and other extraneous classes)
	Server Script Setup
	Server File System Setup



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
	ex.  from FieldTest_File import FieldTest_File
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
	  As described above, the general usage of the files in the FileParser
	directory is to import FieldTest_File or CrowdSource_File. However, there
	are a number of other files in the directory, which support this class.
	  Each _File object (and by _File, I'm referring to FieldTest_File and
	CrowdSource_File) is going to be made up of _Test objects. These _Test
	objects can be TCP_Tests, UDP_Tests, etc.
	  If you look at a raw data file, you will notice that each file contains
	a number of tests, and each test contains a number of threads, and each
	thread a number of measurements. The object architecture is much the same,
	with each object holding a list of other, smaller entities.

	  Also in the FileParser directory are a number of files that start with
	'_'. These are the base classes. '_Test' is the base class for 'UDP_Test'
	and 'TCP_Test' and others. The '_' files are not meant to be used in code,
	as they are just an abstract version of the others.
	  Also, every class, in some way, inherits from '__Base'. This class holds
	some formatting information (in the Formatting class), and Error info (in
	the ErrorHandling class). Be careful with those classes.



CSV GENERATOR SETUP (and other extraneous classes):
	  Initially, the FileParser classes had internal functions that returned
	values one would require for a CSV. However, this meant that scripts that
	would create CSVs also needed to know those functions, and then put the
	values in the order they required.
	  Now, there is a CSV Generator class, which specializes in putting values
	for a CSV in the correct order. It uses the CSV Data Extractor class to get
	values from _File and _Test objects. If you need to get new value, you need
	to modify the 'csvDataExtractor' class.
	  Also, be aware that the column headers for CSVs are stored in the
	'_csvHeaders_' file. Any changes here can affect the function of the
	generator.

	  This class (and the dependent subclasses) are quite complicated. I have
	not yet found a better way to do this, as well as implement error checking.
	For instance, in the CSV Data Extractor class, there is a POST-condition
	function that checks the number of values extracted against the number of
	columns associated with those values. If they do not match up, then an error
	is raised. Maybe there is a better way to do this, but I haven't thought of
	it yet.



SERVER SCRIPT SETUP:
	  Much like everything else in this project, underscore mean 'semi-private'.
	Files that start with an underscore are generally not run directly, but are
	used by the other scripts in this system.
	  The main scripts you will want to pay attention to are 'sort_and_extract',
	'email_daily', 'email_weekly', and 'archive'.
	  'sort_and_extract' is run every hour (at xx:10), 'email_daily' is run
	every day at 11:20pm, 'email_weekly' is run every Sunday at 11:22pm, and
	'archive' is run every Sunday at 11:59pm.

	  'sort_and_extract' looks for new raw data files in the UploadData
	directory. If new files are found, they are parsed, and the necessary
	values extracted and added to the correct CSV.
	  'email_*' sends an email with the most recent CSV changes to specified
	recipients. Some of the emails are for error checking only, while others
	are more official emails. Functionality that is common to both 'email_daily'
	and 'email_weekly' is stored in 'email_base'.
	  'archive' will move any files in ProcessedData and csvResults to the
	correct folders in ARCHIVE at 11:59pm on Sunday. If there are copies of a
	CSV file in CSVs_Archive and csvResults, then a duplicate of one is made,
	and both are maintained.



SERVER FILE SYSTEM SETUP:
	  Here I'll talk about how the folders are all set up on the server, what
	each one holds, and other such things.
	  This is a broad overview of the server setup, starting from the home
	folder of the user we have access to.

	USER
		crontab_config.txt
		ARCHIVE
			CSVs_Archive
			DATA_Archive
		BACKUPS
		commands
			sort_and_extract.py
			archive.py
			...
			_sensitiveInfo				(1)
			PyFiles
				FileParser
					FieldTest_File.py
					TCP_Test.py
					...
					_sensitiveInfo		(2)
				csvGeneration
				moduleWrappers
		csvResults
		dev
		ExceptionFiles
		ProcessedData
		UploadData


	- crontab_config: This holds the cron job commands that should be used. To
			add them to your user's crontab,
			execute 'crontab crontab-config.txt'
	- ARCHIVE: This folder will hold an archive of all of the 'daily results'
			CSVs, as well as the processed data
	- BACKUPS: This folder will hold yearly backups of the data uploaded, which
			have been zipped into a smaller file format
	- commands: This folder holds all of the script and class files to be used
		- *.py: Python scripts that will be used during cronjob execution
		- PyFiles: This folder holds all of the Python class files, necessary
				for parsing raw text files, and performing special functions,
				like generating a CSV
			- FileParser: This is the folder that holds all of the Python class
					files for the main work of the server, parsing raw data
					files. Inside of this directory, there are a number of
					Python files, as well as a "sensitive info" folder. The
					sensitive info folder holds a Python file (that is not on
					Github) which contains the IP addresses of the East and
					West server
	- csvResults: This folder holds the daily CSVs, as well as the
			'all_test_results' CSV. Once the CSVs are no longer going to be
			appended to (i.e. end of the day), they are moved to
			ARCHIVE/CSVs_Archive
	- dev: This folder will contain Python files that I am testing
	- ExceptionFiles: This folder will hold raw data files that caused an error
			during parsing, and should be examined later
	- ProcessedData: This folder will hold all raw data files that have been
			successfully parsed, and their values added to the necessary CSVs
	- UploadData: This folder is where new raw data files are uploaded

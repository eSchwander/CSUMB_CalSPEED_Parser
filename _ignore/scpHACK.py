#!/usr/local/bin/python3
"""
------------------------------------------------------------------------
SCP HACK.PY

AUTHOR(S):     Peter Walker    pwalker@csumb.edu

PURPOSE-  This is a horrible file, but is a way to execute an SCP command,
            without needing a third-party module.
          DON'T EVER MAKE A SCRIPT LIKE THIS!!!
------------------------------------------------------------------------
"""
if __name__=="__main__":
    raise SystemExit

#IMPORTS
import os
import sys
import tempfile
import subprocess
import traceback
#END IMPORTS



def _executeTempScript(script):
    openFileDesc, ABSPATH = tempfile.mkstemp(text=True)
    try:
        openFile = os.fdopen(openFileDesc, "w")
        openFile.write(script)
        openFile.close()
        #Executing the EXPECT script we just wrote to the temp file.
        subprocess.check_call(["/usr/bin/expect", ABSPATH])
        os.remove(ABSPATH)
    except:
        traceback.print_exc()
        try:
            openFile.close()
            os.close(openFileDesc)
        except:
            pass
        os.remove(ABSPATH)
        return False
    #END TRY/EXCEPT
    return True
#END DEF


def putFile(fromPath="", toPath="",
            SVR_ADDR="localhost", SVR_USER="", SVR_PASS=""):
    """Copying a file from 'fromPath' to 'toPath'"""
    if not os.path.isfile(os.path.abspath(fromPath)):
        raise ValueError("The given file does not exists.\n"+
                         "Was given {}".format(os.path.abspath(fromPath)))

    expectScript = """
        #!/usr/bin/expect
        spawn scp {3} {1}@{0}:{4}
        expect "password:"
        send "{2}\r"
        expect eof
        """.format(SVR_ADDR,SVR_USER,SVR_PASS, fromPath, toPath)
    return _executeTempScript(expectScript)
#END DEF


def getFile(fromPath="", toPath="",
            SVR_ADDR="localhost", SVR_USER="", SVR_PASS=""):
    """Getting a given file at the specified location 'fromPath', putting it in 'toPath'"""
    expectScript = """
        #!/usr/bin/expect
        spawn scp {1}@{0}:{3} {4}
        expect "password:"
        send "{2}\r"
        expect eof
        """.format(SVR_ADDR,SVR_USER,SVR_PASS, fromPath, toPath)
    currentNumFiles = len(os.listdir(toPath))
    return _executeTempScript(expectScript)
#END DEF

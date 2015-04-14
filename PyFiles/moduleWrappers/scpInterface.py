#!/usr/local/bin/python3
"""
------------------------------------------------------------------------
SCP INTERFACE.PY

AUTHOR(S):     Peter Walker    pwalker@csumb.edu

PURPOSE-  This script will contain a number of functions that can be
            used to execute some 'scp' commands. The general idea is that
            each function will create a Popen object from Python's subprocess
            module. This object will execute an 'scp' command, and input the
            necessary keyfile location/password to authenticate the connection.
            The functions will also handle some of the error handling, in terms
            of files already existing on the server or local side.
          The functions in the script are expected to only transfer one file at
            a time, and will simply fail gracefully when an error occurs.
------------------------------------------------------------------------
"""
if __name__=="__main__":
    raise SystemExit

#IMPORTS
import os
import sys
import pty
import time
import subprocess
import traceback
#END IMPORTS



class SCPInterface(object):

    """
    ..
    ..
    """

    def __init__(self, **kwargs):
        """Basic class initialization"""
        self.remoteDir = ""
        self.localDir = os.getcwd()
        self.config = {"host":     "",
                       "username": "",
                       "keyfile":  ""
                       }
        self.config.update(kwargs)
    #END DEF


# Decorators -------------------------------------------------------------------

    def __POST_fileTransferred(func):
        def fileWasTransferred(*args, **kwargs):
            output = func(*args, **kwargs)
            if "No such file or directory" in output:
                return False
            else:
                return True
        #END DEF
        return fileWasTransferred
    #END DEF

    def __PRE_fileExists(func):
        def fileExists(*args, **kwargs):
            if not os.path.isfile(args[1]):
                raise RuntimeError("Given file does not exist on this system."+
                                   "Was given: {}".format(args[1]))
            return func(*args, **kwargs)
        return fileExists
    #END DEF

    def __PRE_configSet(func):
        def configIsSet(*args, **kwargs):
            if "username" not in args[0].config:
                raise ValueError("The username has not been set. Please set self.config['username'].")
            if "host" not in args[0].config:
                raise ValueError("The host address has not been set. Please set self.config['host'].")
            if args[0].remoteDir == "":
                raise ValueError("The remote directory has not been set. Please set self.remoteDir.")
            return func(*args, **kwargs)
        return configIsSet
    #END DEF


# Functions called to GET or PUT files on the server ---------------------------

    @__POST_fileTransferred
    @__PRE_configSet
    def getFile(self, filename):
        """Based on the options set in self.config, gets a file from a remote server"""
        if "password" in self.config and \
                self.config["password"]!="" and \
                not self.config["keyfile"]:
            return self.__getFile_pwd(filename)
        elif "keyfile" in self.config:
            return self.__getFile_key(filename)
        else:
            return None
    #END DEF

    @__POST_fileTransferred
    @__PRE_configSet
    @__PRE_fileExists
    def putFile(self, filename):
        """Based on the options set in self.config, put a file on a remote server"""
        if "password" in self.config and \
                self.config["password"] and \
                not self.config["keyfile"]:
            return self.__putFile_pwd(filename)
        elif "keyfile" in self.config:
            return self.__putFile_key(filename)
        else:
            return None
    #END DEF


# Get and Put using a keyfile --------------------------------------------------

    def __getFile_key(self, filename):
        getOptions = ["/usr/bin/scp",
                      "-i", self.config["keyfile"],
                      "{}@{}:{}".format(self.config['username'],
                                        self.config['host'],
                                        os.path.abspath(
                                           os.path.join(self.remoteDir, filename)
                                           )
                                        ),
                      os.path.abspath(self.localDir)
                      ]
        return self.__executeSP(getOptions)
    #END DEF

    def __putFile_key(self, filename):
        putOptions = ["/usr/bin/scp",
                      "-i", self.config["keyfile"],
                      os.path.abspath(os.path.join(self.localDir, filename)),
                      "{}@{}:{}".format(self.config['username'],
                                        self.config['host'],
                                        os.path.abspath(self.remoteDir)
                                        )
                      ]
        return self.__executeSP(putOptions)
    #END DEF

    def __executeSP(self, opts):
        #After checking that opts is a list, we
        if not isinstance(opts, list):
            raise RuntimeError("The options passed were not in a list. Was given "+
                               "a {}".format(type(opts)))
        #END IF
        subP = subprocess.Popen(opts,
                                shell=False,
                                stdin=subprocess.PIPE,
                                stdout=subprocess.PIPE,
                                stderr=subprocess.PIPE
                                )
        response = subP.communicate()[0]
        return response
    #END DEF


# Get and Put using a password -------------------------------------------------

    def __getFile_pwd(self, filename):
        #Between a GET and PUT call, the only difference is where the filename goes.
        # As such, we only need to set the paths for local and remote
        remotePath = ("{}@{}:".format(self.config['username'], self.config['host'])+
                      "{}".format(os.path.abspath(os.path.join(self.remoteDir, filename))) )
        localPath = os.path.abspath(self.localDir)
        return self.__executeCP(remotePath, localPath)
    #END DEF

    def __putFile_pwd(self, filename):
        remotePath = ("{}@{}:".format(self.config['username'], self.config['host'])+
                      "{}".format(os.path.abspath(self.remoteDir)) )
        localPath = os.path.abspath(os.path.join(self.localDir, filename))
        return self.__executeCP(localPath, remotePath)
    #END DEF

    def __executeCP(self, pathFrom, pathTo):
        #Setting the process name, and the sequence of arguments
        allOutput = ""
        processName = "/usr/bin/scp"
        command_args = [processName, pathFrom, pathTo]

        #We now use fork() to create two processes of the same function. However,
        # the child process will replace itself with the execution of the above commands,
        # and the parent process will send data to the child process.
        #PID = 0 for child, and the PID of the child for the parent
        pid, child_fd = pty.fork()
        if not pid: # Child process
            # Replace child process with our SCP process
            os.execv(processName, command_args)

        #Back in our parent process, we send the necessary information (like a
        # password) to our child process
        while True:
            output = os.read(child_fd, 1024).decode()
            if not output:
                break

            #Removing return carriages from ouput
            output = output.replace("\r","")\
                           .replace("\n\n","\n")

            # Write the password, if the child process is waiting
            if 'password:' in output.lower():
                os.write(child_fd, ("{}\n".format(self.config['password'])).encode())
                #Sleep for just a tiny bit so that our input can be read
                time.sleep(0.001)
            elif "are you sure you want to continue connecting" in output.lower():
                # Adding key to known_hosts
                os.write(child_fd, ("yes\n").encode())
                time.sleep(0.001)
            #Adding the current output to the variable that will hold everything
            allOutput += output
        #END WHILE
        return allOutput
    #END DEF


# Simple attribute getters -----------------------------------------------------

    def printCurrentInfo(self):
        """Prints the current connection information"""
        print("Connected to '{}' as '{}'".format(self.config["host"], self.config["username"]))
        print("Current LOCAL directory: {}".format(self.localDir))
        print("Current REMOTE directory: {}".format(self.remoteDir))
        print("Has PASSWORD: {}".format( repr('password' in self.config and
                                              self.config['password']!="") ))
        print("Has KEYFILE: {}".format( repr('keyfile' in self.config and
                                             self.config['keyfile']!="") ))
        return False
    #END DEF

    def getCurrentInfo(self):
        """Returns a list of the current connection information"""
        return ["{}@{}".format(self.config["username"], self.config["host"]),
                self,localDir,
                self.remoteDir]
    #END DEF
#END CLASS

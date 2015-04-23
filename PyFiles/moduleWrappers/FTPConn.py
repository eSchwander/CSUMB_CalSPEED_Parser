#!/usr/local/bin/python3
"""
------------------------------------------------------------------------
FTP CONN.PY

AUTHOR(S):     Peter Walker    pwalker@csumb.edu

PURPOSE-    This module provides a class that manages and facilitates an FTPS
             connection, and takes care of getting and putting files in the
             correct locations.
            NOTE: This script obviously requires that the server in question have
             the FTP port open. This class can use an FTPS connection (which is
             an FTP connection encrypted with SSL on port 21), but CANNOT CREATE
             an SFTP connection (an FTP connection using an SSH pipe, which connects
             to port 22).
             To open an SFTP connection, you must install a third-party application,
             like 'paramiko'.
FUNCTIONS
    ..
------------------------------------------------------------------------
"""
#IMPORTS
import ssl
import ftplib
import sys
import os
import traceback
import datetime
#END IMPORTS


class FTPConnection(object):

    """
    ..
    ..
    """

    def __init__(self, **kwargs):
        """Basic class initialization"""
        self.CONN = None
        self.remoteDir = ""
        self.localDir = ""
        self.cfg = {"host":     "",
                    "username": ""
                    }
        self.cfg.update(kwargs)
        if all( [attr in self.cfg for attr in ["host","username"]] ) and \
                ("password" in self.cfg or "keyfile" in self.cfg):
            self.connect()
    #END DEF

    def __del__(self):
        """Safely destroys the object, closing FTPS connections"""
        self.cfg = {}
        if isinstance(self.CONN, ftplib.FTP_TLS.__class__):
            self.CONN.quit()
            print("FTPS connection closed.")
        self.CONN = None
    #END DEF


# Functions for establishing and using an FTPS connection ----------------------

    def connect(self):
        """
        Using the object attributes 'recipients', 'MESSAGE', 'SUBJECT', and
         'ATTACHMENTS', sends an email
        RETURNS:
            None
        RAISES:
            None. Prints error message if email was not sent
        """
        assert ("username" in self.cfg and "host" in self.cfg,
                "The necessary configuration information has not been set.\n"+
                "'host' and 'username' must be set.")
        assert ("password" in self.cfg or "keyfile" in self.cfg,
                "The necessary configuration information has not been set.\n"+
                "'password' or 'keyfile' must be set.")
        #END IF
        context = ssl.create_default_context()
        try:
            if "keyfile" in self.cfg:
                self.CONN = ftplib.FTP_TLS(host=self.cfg["host"],
                                           user=self.cfg["username"],
                                           keyfile=self.cfg["keyfile"],  #---> "/path/to/keyfile.pem"
                                           context=context)
            elif "password" in self.cfg:
                self.CONN = ftplib.FTP_TLS(host=self.cfg["host"],
                                           user=self.cfg["username"],
                                           passwd=self.cfg["password"],
                                           context=context)
            #END IF/ELIF
            #Removing the password from the object so that it doesn't stay
            # around any longer than it needs to
            self.cfg["password"] = None
            #Logging in and adding the encryption
            self.CONN.login()
            self.CONN.auth()
            self.CONN.prot_p()
            print("FTPS Connection established.")
            #Setting some class attributes to save where we are both locally and remotely
            self.remoteDir = self.CONN.pwd()
            self.localDir = os.getcwd()
        except:
            print("Current information was not sufficient to establish an FTPS connection")
            self.CONN = None
            self.remoteDir = None
            self.localDir = None
            return False
        return True
    #END DEF

    def __checkConnected(func):
        def checkConnectedWrapper(*args, **kwargs):
            if not isinstance(args[0].CONN, ftplib.FTP_TLS.__class__):
                print("You must establish an FTPS connection before using this functions.\n"+
                      "Attempting to connect with existing information...")
                if args[0].connect():
                    return func(*args, **kwargs)
                else:
                    return False
            else:
                return func(*args, **kwargs)
            #END IF/ELSE
        #END DEF
        return checkConnectedWrapper
    #END DEF

# FTPS Attribute accessors and modifiers ---------------------------------------

    def __hasNecessaryInfo(func):
        def objectHasNecessaryInfo(*args, **kwargs):
            for attribute in ["host", "username", "remoteDir", "localDir"]:
                if attribute not in args[0].cfg:
                    raise AttributeError("This object cannot conduct any FTP actions until the necessary information is set.")
            return func(*args, **kwargs)
        #END DEF
        return objectHasNecessaryInfo
    #END DEF

    def printCurrentInfo(self):
        """Prints the current connection information"""
        print("Connected to '{}' as '{}'".format(self.cfg["host"], self.cfg["username"]))
        print("Current LOCAL directory: {}".format(self.localDir))
        print("Current REMOTE directory: {}".format(self.remoteDir))
        return False
    #END DEF

    def getCurrentInfo(self):
        """Returns a list of the current connection information"""
        return ["{}@{}".format(self.cfg["username"], self.cfg["host"]),
                self,localDir,
                self.remoteDir]
    #END DEF

    @__checkConnected
    @__hasNecessaryInfo
    def getFile(self, filename):
        """."""
        fullFilename = os.path.abspath(os.path.join(self.remoteDir, filename))
        contentInRemote = self.CONN.nlst(self.remoteDir)
        contentInRemote = [os.path.abspath(os.path.join(self.remoteDir, FILE)) for FILE in contentInRemote]
        if fullFilename not in contentInRemote:
            print("'{}' could not be found in the remote directory, '{}'".format(filename, self.remoteDir))
            return False
        else:
            fileLocal = os.path.abspath(os.path.join(self.localDir, filename))
            if os.path.isfile(fileLocal):
                choice = input("The file '{}' will be overwritten. Continue? (Y/n)".format(filename))
            else:
                choice = "Y"
            if choice.upper() is "Y":
                try:
                    with open(fileLocal, "wb") as output:
                        self.CONN.retrbinary("RETR {}".format(fullFilename), output.write)
                except:
                    return False
                else:
                    return True
            #END IF
        return False
    #END DEF

    @__checkConnected
    @__hasNecessaryInfo
    def putfile(self, filename):
        """."""
        fullFilename = os.path.abspath(os.path.join(self.localDir, filename))
        contentInLocal = os.listdir(self.localDir)
        contentInLocal = [os.path.abspath(os.path.join(self.localDir, FILE)) for FILE in contentInLocal]
        if fullFilename not in contentInLocal:
            print("'{}' could not be found in the remote directory, '{}'".format(filename, self.localDir))
            return False
        else:
            fileRemote = os.path.abspath(os.path.join(self.remoteDir, filename))
            if filename in self.CONN.nlst(self.remoteDir):
                choice = input("The file '{}' will be overwritten. Continue? (Y/n)".format(filename))
            else:
                choice = "Y"
            if choice.upper() is "Y":
                try:
                    with open(fileRemote, "rb") as output:
                        self.CONN.storbinary("STOR {}".format(fullFilename), output)
                except:
                    return False
                else:
                    return True
            #END IF
        return False
    #END DEF
#END CLASS

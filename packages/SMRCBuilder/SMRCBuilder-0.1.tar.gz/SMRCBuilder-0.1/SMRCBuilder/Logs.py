from SMRCBuilder import Exceptions
import datetime
import os

class Logs():
    def createfile(directory):
        fh = open(f"{directory}/{name}",'w')
        fh.close()

    def datelog(name, info, directory, time):
        if info == "":
            raise Exceptions.ArgError("Message Cannot Be Blank")
        else:
            Logs.createfile(directory)
            fh = open(f"{directory}/{name}",'a')
            fh.write(f"{info},{time}\n")
            fh.close()

    def notimelog(name, info, directory):
        if name == "":
            raise Exceptions.ArgError("File Name Cannot Be Blank")
        if info == "":
            raise Exceptions.ArgError("Message Cannot Be Blank")
        else:
            Logs.createfile(directory)
            fh = open(f"{directory}/{name}",'a')
            fh.write(f"{info}\n")
            fh.close()
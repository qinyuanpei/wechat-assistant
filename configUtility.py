import ConfigParser

class Config:

    def __init__(self,fileName):
        self.fileName = fileName
        self.cf = ConfigParser.ConfigParser()
        self.cf.read(fileName)

    def readConfigItem(self,section,item):
        return self.cf.get(section,item)
    
    def writeConfigItem(self,section,item,value):
        self.cf.set(section,item,value)
        self.cf.write(open(self.fileName, "w"))
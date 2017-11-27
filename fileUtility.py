#!/usr/bin/python
#-*- coding: utf-8 -*-

import os
import sys

class FileUtility:

    def getCurrentPath(self):
        path = sys.path[0]
        if os.path.isdir(path):
           return path
        elif os.path.isfile(path):
           return os.path.dirname(path)

    def createFolder(self,filePath):
        if(os.path.exists(filePath) == False): 
            os.mkdir(filePath)
        
    def readAllTexts(self,filePath):
        texts = []
        for text in open(filePath):
            texts.append(text)
        return texts


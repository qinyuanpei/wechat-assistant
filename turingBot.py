#!/usr/bin/python
#-*- coding: utf-8 -*-

import requests
from configUtility import Config
from fileUtility import FileUtility

class TuringBot:

    def __init__(self,apiKey):
        self.apiKey = apiKey
        self.reqURL = 'http://www.tuling123.com/openapi/api'

    def getInfo(self,info):

        data = {
            'key' : self.apiKey,
            'info' : info,
            'userid' : 'wechat-assistant'
        }

        try:
            response = requests.post(self.reqURL, data=data).json()
            return response.get('text')
        except Exception,e:
            print repr(e)
            return

if __name__ == "__main__":
    filePath = FileUtility().getCurrentPath() + "/config.ini"
    config = Config(filePath)
    apiKey = config.readConfigItem("tulingConfig","apiKey")
    bot = TuringBot(apiKey)
    info = bot.getInfo("你好")
    print info
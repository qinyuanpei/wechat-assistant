#!/usr/bin/python
#-*- coding: utf-8 -*-

import random
import requests
from bs4 import BeautifulSoup
from fileUtility import FileUtility
import os
import sys
reload(sys)
sys.setdefaultencoding('utf8')


class ImageService:

    def __init__(self):
        self.reqURL = 'http://www.doutula.com/search?keyword='
        self.currPath = FileUtility().getCurrentPath()

    def search(self,keyword):
        headers = {
            'User-Agent':'Mozilla/5.0 (X11; Ubuntu; Linu…) Gecko/20100101 Firefox/56.0',
            'Refer':'http://www.doutula.com/so/'
        }

        response = requests.get(self.reqURL + keyword, headers=headers)

        #extract images
        html = response.text
        soup = BeautifulSoup(html,"html.parser")
        imgs = soup.find('div',class_='random_picture').find_all('img',class_='img-responsive lazy image_dtb')
        urls = map(lambda e:e['data-original'],imgs)
        gifs = filter(lambda e:str(e)[-4]=='.gif',urls)
        
        #return random image
        if(len(gifs)>0):
            return gifs[0]
        else:
            length = len(urls)
            return urls[random.randint(0,length)]
    
    def download(self,resURL,fileName=None):
        if(fileName == None):
            fileName = resURL.split('/')[-1]

        FileUtility().createFolder(self.currPath + '/images/')
        filePath = self.currPath + '/images/' + fileName
        if(os.path.exists(filePath)):
            return filePath

        response = requests.get(resURL)
        with open(filePath, 'wb') as f:
            f.write(response.content)

        return filePath

if __name__ == "__main__":
    service = ImageService()
    resURL = service.search('叫我爸爸')
    print service.download(resURL)
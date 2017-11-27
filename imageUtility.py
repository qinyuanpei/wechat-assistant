#!/usr/bin/python
#-*- coding: utf-8 -*-

import time
import random
import requests
from bs4 import BeautifulSoup
from fileUtility import FileUtility
import TencentYoutuyun
from PIL import Image
import os
import sys
reload(sys)
sys.setdefaultencoding('utf-8')


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

        folder = unicode(os.path.join(self.currPath,'images'),'utf-8')
        FileUtility().createFolder(folder)
        filePath = folder + '\\' + fileName
        if(os.path.exists(filePath)):
            return filePath

        response = requests.get(resURL)
        with open(filePath, 'wb') as f:
            f.write(response.content)

        return filePath
    
    def matchText(self,fileName):
        appid = '10109383'
        userId = '875974254'
        secretId = 'AKIDd3D8rKrzCAsKXXKn8E5i6EAsLYVCuoiP'
        secretKey = 'ZtwjGYbP1PYT9anmV3MRGrCKDuPffOr4'
        endPoint = TencentYoutuyun.conf.API_YOUTU_END_POINT
        youtu = TencentYoutuyun.YouTu(appid, secretId, secretKey, userId, endPoint)
        extenName = os.path.splitext(fileName)[1]
        if(extenName == '.gif'):
            newFile = fileName.replace('.gif','.jpg')
            self.convertFormat(fileName,newFile)
            fileName = newFile
        retocr = youtu.generalocr(fileName, data_type = 0)
        items = retocr['items']
        return map(lambda x:x['itemstring'].encode('iso-8859-1'),items)
    
    def convertFormat(self,input,output):
        image = Image.open(input)
        image = image.convert('RGB')
        image.save(output)

if __name__ == "__main__":
    service = ImageService()
    resURL = service.search('叫我爸爸')
    print resURL
    resFile = service.download(resURL)
    print resFile
    print service.matchText(resFile)[0]
    

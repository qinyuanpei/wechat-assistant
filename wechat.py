#!/usr/bin/python
#-*- coding: utf-8 -*-

import itchat
from turingBot import TuringBot
from fileUtility import FileUtility
from configUtility import Config
from imageUtility import ImageService
from botState import BotState
import sys
reload(sys)
sys.setdefaultencoding('utf8')

msg_sender = None
bot_state = BotState.default
current = FileUtility().getCurrentPath()

@itchat.msg_register(itchat.content.TEXT, isFriendChat=True, isGroupChat=True, isMpChat=False)
def autoReplyText(msg):
    is_At = True
    if(msg.has_key('isAt')):
        is_At = msg['isAt']
    filePath = current + "/config.ini"
    config = Config(filePath)
    apiKey = config.readConfigItem("tulingConfig","apiKey")
    if(is_At):
        bot = TuringBot(apiKey)
        info = bot.getInfo(msg['Text'])
        return info

@itchat.msg_register(itchat.content.PICTURE,isFriendChat=True, isGroupChat=True, isMpChat=False)
def autoReplyPicture(msg):
    global msg_sender
    msg_sender = msg['FromUserName']
    service = ImageService()
    resURL = service.search(msg['Text'])
    resRow = service.download(resURL)
    itchat.send_image(resRow,msg['FromUserName'])

@itchat.msg_register(itchat.content.PICTURE,isFriendChat=True, isGroupChat=True, isMpChat=False)
def forwardMessage(msg):
    global msg_sender
    msg_sender = msg['FromUserName']
    msg['Text'](msg['FileName'])
    itchat.send('@%s@%s' % ({'Picture': 'img'}.get(msg['Type'], 'fil'), msg['FileName']), xiaoice)

@itchat.msg_register([itchat.content.PICTURE,itchat.content.TEXT],isMpChat=True)
def interceptMessage(msg):
    if(msg['FromUserName'] == xiaoice):
        msg_type = msg['Type']
        if(msg_type == 'Picture'):
            msg['Text'](msg['FileName'])
            itchat.send('@%s@%s' % ({'Picture': 'img'}.get(msg['Type'], 'fil'), msg['FileName']), msg_sender)
        else:
            msg_text = msg['Text']
            itchat.send(msg_text, msg_sender)

itchat.auto_login(hotReload=True)
xiaoice = itchat.search_mps(name='小冰')[0]['UserName']
itchat.run(debug=True)
    
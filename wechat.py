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

bot_state = BotState.default
msg_sender = None

@itchat.msg_register(itchat.content.TEXT, isFriendChat=True, isGroupChat=True, isMpChat=False)
def autoReplyText(msg):
    filePath = FileUtility().getCurrentPath() + "/config.ini"
    config = Config(filePath)
    apiKey = config.readConfigItem("tulingConfig","apiKey")
    bot = TuringBot(apiKey)
    info = bot.getInfo(msg['Text'])
    return info

@itchat.msg_register(itchat.content.PICTURE,isFriendChat=True, isGroupChat=True, isMpChat=False)
def autoReplyPicture(msg):
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
    print msg['FromUserName']
    print xiaoice
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
chatroom = itchat.search_chatrooms(name='神一样的队友')[0]
chatroom = itchat.update_chatroom(chatroom['UserName'])
qrcode = FileUtility().getCurrentPath() + "/qrcode.jpeg"
itchat.run(debug=True)
    
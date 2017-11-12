#encoding: utf-8
import itchat
import requests
import ConfigParser

def msg_register(msgType):
    def decorator(func):
        def wrapper(self,args):
            register = itchat.msg_register(msgType)
            register(args)
        return func
    return decorator

class BotState:
    default,autoReply,autoChat,autoPicture = range(0,4)

class WeChatAssistant:
    def __init__(self):
        self.state = BotState.default
        self.config = ConfigParser.ConfigParser()
        self.config.read('config.ini')

    @msg_register(itchat.content.TEXT)
    def handle_TextInput(self,msg):
        print msg
        if msg['Text'] == '--help':
            return '''欢迎使用个人微信助手
                      您可以输入下列指令：
                      --exit:退出微信助手模式
                      --help：显示命令帮助信息
                      --autoChat:进入自动聊天模式
                      --autoReply：进入自动回复模式
                      --autoPicture：进入自动斗图模式'''
        elif msg['Text'] == '--exit':
            self.state = BotState.default
        elif msg['Text'] == '--autoChat':
            self.state = BotState.autoChat
        elif msg['Text'] == '--autoReply':
            self.state = BotState.autoReply

        if(self.state == BotState.autoChat): 
            return autoChat(msg)
        if(self.state == BotState.autoReply): 
            return autoReply()

    @msg_register(itchat.content.PICTURE)
    def handle_PictureInput(self,msg):
        self.state = BotState.autoPicture
        return autoPicture(msg)

    def autoChat(msg):
        APIKey = readConfigItem('tulingConfig','apiKey')
        reqURL = readCOnfigItem('tulingConfig','reqURL')
        data = {
            'key' : APIKey,
            'info' : msg,
            'userid' : 'wechat-assistant',
        }

        try:
            response = requests.post(reqURL, data=data).json()
            return response.get('text')
        except:
            return

    def autoReply():
        return u'[自动回复]我有事不在，稍后再回复您，谢谢'
    
    def autoPicture(msg):
        return u'表情包正在准备中...'

    def readConfigItem(cf,section,item):
        return cf.get(section,item)
    
    def writeConfigItem(cf,section,item,value):
        cf.set(section,item,value)
        cf.write(open("config.ini", "w"))
    
    def getBotState(cf):
        cf.read('config.ini')
        return readConfigItem(cf,'baseConfig','botState')
    
    def setBotState(cf,state):
        writeConfigItem(cf,'baseConfig','botState',state)
    
    def getCurrntPath(self):
        path = sys.path[0]
        if os.path.isdir(path):
           return path
        elif os.path.isfile(path):
           return os.path.dirname(path)

    def Run(self):
        itchat.auto_login(hotReload=True)
        itchat.run(debug=True)
    


if __name__ == "__main__":
    wechat = WeChatAssistant()
    wechat.Run()


        
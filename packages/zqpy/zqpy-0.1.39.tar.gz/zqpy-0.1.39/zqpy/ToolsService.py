from HttpService import HttpServiceClass
from FileService import FileServiceClass
import json

class ToolsServiceClass(object):
    def __init__(self):
        self.httpService = HttpServiceClass()
        self.fileService = FileServiceClass()
        #region 企业微信
        self.corpid = "wwb6ec4438ccc388c3"      # Corpid是企业号的标识
        self.secret = "_surPYo0SLVcxPKzAnHdWBwpGl2woxWKWpSTMvbZvnw"     # Secret是管理组凭证密钥
        self.agentid = "1000002"        # 应用ID
        self.tokenConfig = r'./temp/zabbix_wechat_config.json'     # token_config文件放置路径
        self.fileService.CreateDir(self.tokenConfig)
        self.bot = "https://qyapi.weixin.qq.com/cgi-bin/webhook/send?key=c2ae20ef-9a26-4791-abb5-962e07f97144"
        #endregion
    def ToNumberCompany(self, number):
        if number > 100000000:
            return number/100000000 + '亿'
        elif number > 10000000:
            return number/10000000 + '千万'
        elif number > 1000000:
            return number/1000000 + '百万'
        elif number > 100000:
            return number/100000 + '十万'
        elif number > 10000:
            return number/10000 + '万'
        else:
            return number
    
    #https://www.runoob.com/markdown/md-block.html
    def SendNotify(self, title='zq_python', desc='', isMerge=True, key=None):
        if len(title + '-->' + desc) < 256 and isMerge:
            title = title + '-->'  + desc
        params = {'text': title, 'desp': desc}
        print('方糖发送内容：{}'.format(params))
        try:
            urlRequest = self.httpService.GetUrlResetByRequests('https://sctapi.ftqq.com/%s.send'%(key or "SCT2361TYPGLyA6TP4dX6jCmnSnDklkO"), params=params, headers={'Connection':'close'}, verify = False)
            urlRequest.close()
        except BaseException as e:
            print('方糖内容发送出错： ', str(e))
        finally:
            pass
    
    def SendQQMsg(self, message_type:str, id:int, message):
        '''
        message_type: private、group、discuss
        '''
        try:
            if False:
                params = {'message_type':message_type, 'id':id, 'message':message}
                urlRequest = self.httpService.GetUrlResetByRequests('http://43.226.146.76:9004/send_msg', params=params, verify = False)
                urlRequest.close()
        except BaseException as e:
            print('方糖内容发送出错： ', str(e))
    
    def _GetTokenFromServer(self, corpid, secret, tokenConfig):
        """ 获取 token """
        token = False
        try:
            file = open(tokenConfig, 'r')
            token = json.load(file)['access_token']
            file.close()
        except:
            url = "https://qyapi.weixin.qq.com/cgi-bin/gettoken"
            data = {
                "corpid": corpid,
                "corpsecret": secret
            }
            r = self.httpService.PostUrlResetByRequests(url=url, params=data, verify=False)
            print("企业微信Token: %s"%r.json())
            if r.json()['errcode'] != 0:
                token = False
            else:
                token = r.json()['access_token']
                file = open(tokenConfig, 'w')
                file.write(r.text)
                file.close()
        return token

    def SendWorkWX(self, data, corpid=None, secret=None, errorNum=3):
        """ 
        发送消息到企业微信
        API文档： https://work.weixin.qq.com/api/doc/90000/90135/90236
        """
        if not corpid or not secret:
            corpid = self.corpid
            secret = self.secret
            tokenConfig = self.tokenConfig
        else:
            tokenConfig = r'./temp/%s_wechat_config.json'%(corpid)
        # 获取token信息
        token = self._GetTokenFromServer(corpid, secret, tokenConfig)
        # 发送消息
        if not "agentid" in data:
            data["agentid"] = self.agentid
        if not "touser" in data:
            data["touser"] = "@all"
        if not "toparty" in data:
            data["toparty"] = "1"
        url = "https://qyapi.weixin.qq.com/cgi-bin/message/send?access_token=%s" % token
        result = self.httpService.PostUrlResetByRequests(url=url, data=json.dumps(data), verify=False)
        print("企业微信应用消息： %s"%result.json())
        # 如果发送失败，将重试多次if
        if result.json()['errcode'] != 0 and errorNum and errorNum > 0:
            return self.SendWorkWX(data, corpid, secret, errorNum-1)
        else:
            return result.json()
    
    def SendWorkWXBot(self, data, url=None):
        """
        发送企业微信消息，机器人群
        API文档： https://work.weixin.qq.com/api/doc/90000/90136/91770
        """
        url = url or self.bot
        if not "mentioned_list" in data["text"]:
            data["text"]["mentioned_list"] = ["@all"]
        if not "mentioned_mobile_list" in data["text"]:
            data["text"]["mentioned_mobile_list"] = ["@all"]
        print(json.dumps(data))
        result = self.httpService.PostUrlResetByRequests(url=url, data=json.dumps(data), verify=False)
        print("企业微信应用消息： %s"%result.json())

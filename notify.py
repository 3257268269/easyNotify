'''
  模板测试号注册地址：https://mp.weixin.qq.com/debug/cgi-bin/sandbox?t=sandbox/login
'''
# coding=utf-8
import json, requests

class Notify:
    def __init__(self, appid = '', appsecret = '', template_id = ''):
        self.appid = appid
        self.appsecret = appsecret
        self.template_id = template_id
        self.access_token = ''

        self.get_access_token()

    # 获取access_token
    def get_access_token(self):
        url = 'https://api.weixin.qq.com/cgi-bin/token?grant_type=client_credential&appid=%s&secret=%s' % (self.appid, self.appsecret)
        self.access_token = json.loads(requests.get(url).text)['access_token']

    # 获取用户列表(关注该测试号的用户的openid)
    def get_openids(self):
        if self.access_token == '':
            self.get_access_token()

        url = 'https://api.weixin.qq.com/cgi-bin/user/get?access_token=%s&next_openid=' % str(self.access_token)
        return json.loads(requests.get(url).text)['data']['openid']

    def send_msg(self, openid, notify_msg):
        msg = {
            'touser': openid,
            'template_id': self.template_id,
            #'url':'',#点击详情会跳转至的页面
            'data': notify_msg
        }
        if self.access_token == '':
            self.get_access_token()
        url = 'https://api.weixin.qq.com/cgi-bin/message/template/send?access_token=%s' % str(self.access_token)
        result = requests.post(url, data = json.dumps(msg)).text
        return json.loads(result)


    def notify(self, msg, openids = []):
        if openids == []:
            openids = self.get_openids()
        for openid in openids:
            result = self.send_msg(openid, msg)
            if result['errcode'] == 0:
                print('OK')
            else:
                print('ERROR')


if __name__ == '__main__':

    # 微信配置
    appid = 'wx9f6ac9208a3ea223'
    appsecret = 'd178054816bdc7f756a3eb5cc5744abb'
    template_id = 'pdHHR6IKjVoTQVTyUR_mBhjEzsXifE6FPbd5zN6dbQU'

    test_msg = {
        'key_1':{
            "value":"2019-1 11:13:23:48",
            'color': '#FF0000'
        },
        'key_2':{
            "value":"【数据异常】",
            'color': '#FF0000'
        },
        'key_3': {
            "value": "Traceback (most recent call last):",
            'color': '#FF0000'
        },
        'key_4': {
            "value": "didn't match because some of the arguments have invalid types: (!torch.cuda.FloatTensor!)",
            'color': '#FF0000'
        }
    }

    nt = Notify(appid, appsecret, template_id)
    nt.notify(test_msg)
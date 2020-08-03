# coding=utf-8
import json
import requests

class Notify:
    def __init__(self, wechat_config):
        self.appid = wechat_config['appid']
        self.appsecret = wechat_config['appsecret']
        self.template_id = wechat_config['template_id']
        self.access_token = ''

    # 获取access_token
    def get_access_token(self, appid, appsecret):
        url = 'https://api.weixin.qq.com/cgi-bin/token?grant_type=client_credential&appid=%s&secret=%s' % (appid, appsecret)

        response = requests.get(url)
        json_data = response.text
        data = json.loads(json_data)
        access_token = data['access_token']
        self.access_token = access_token
        return self.access_token

    # 获取用户列表
    def get_user_list(self):
        if self.access_token == '':
            self.get_access_token(self.appid, self.appsecret)

        access_token = self.access_token
        url = 'https://api.weixin.qq.com/cgi-bin/user/get?access_token=%s&next_openid=' % str(access_token)
        response = requests.get(url)
        result = response.text
        return json.loads(result)

    def send_msg(self, openid, template_id, notify_msg):
        msg = {
            'touser': openid,
            'template_id': template_id,
            #'url':'',#点击详情会跳转至的页面
            'data':notify_msg
        }

        json_data = json.dumps(msg)
        self.access_token = self.get_access_token(self.appid, self.appsecret)
        access_token = self.access_token
        url = 'https://api.weixin.qq.com/cgi-bin/message/template/send?access_token=%s' % str(access_token)

        print(json_data)
        response = requests.post(url, data = json_data)
        result = response.text
        
        print(result)
        
        return json.loads(result)

    # 发送消息
    def notify(self, msg, openids = []):
        if openids == []:
            result = self.get_user_list()
            openids = result['data']['openid']
        for openid in openids:
            result = self.send_msg(openid, self.template_id, msg)
            if result['errcode'] == 0:
                print(' [INFO] send to %s is success' % openid)
            else:
                print(' [ERROR] send to %s is error' % openid)


if __name__ == '__main__':
    # 微信配置
    wechat_config = {
        'appid': '111',
        'appsecret': '111',
        'template_id': "111"
    }

    # 接收者
    openids = ['111']


    ##################程序异常通知###########################
    test_msg_2 = {
        'key_1':{
            "value":"2019-1 11:13:23:48",
            'color': '#FF0000'
        },
        'key_2':{
            "value":"【123】",
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

    notify = Notify(wechat_config)
    notify.notify(test_msg_2)
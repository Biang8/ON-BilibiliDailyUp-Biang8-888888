"""
push the task info in social communication app
"""

import requests
import json


def pushplus_push(token, content, title='Bilibili助手提醒', template='markdown'):
    url = 'http://www.pushplus.plus/send'
    data = {
        "token": token,
        "title": title,
        "content": content,
        "template": template
    }
    body = json.dumps(data).encode(encoding='utf-8')
    headers = {'Content-Type': 'application/json'}
    try:
        response = requests.post(url, data=body, headers=headers)
        response.raise_for_status()  # 检查响应状态码
        try:
            result = response.json()
            print(result)
            return 1
        except json.JSONDecodeError:
            print(f"响应内容不是有效的 JSON 格式: {response.text}")
    except requests.RequestException as e:
        print(f"请求出错: {e}")
    return None


def sever_push(msg, token):
    data = {
        "title": "Bilibili助手提醒",
        "desp": msg
    }
    headers = {
        "Content-Type": "application/json;charset=utf-8"
    }
    try:
        res = requests.post(url=f"https://sctapi.ftqq.com/{token}.send",
                            headers=headers,
                            data=json.dumps(data))
        res.raise_for_status()  # 检查响应状态码
        try:
            res_json = res.json()
            print(res_json)
        except json.JSONDecodeError:
            print(f"响应内容不是有效的 JSON 格式: {res.text}")
    except requests.RequestException as e:
        print(f"请求出错: {e}")


def wechat_push(msg, wechat_id, wechat_app_secret, wechat_app_id):
    access_token_url = f"https://qyapi.weixin.qq.com/cgi-bin/gettoken?corpid={wechat_id}&corpsecret={wechat_app_secret}"
    try:
        access_token_res = requests.get(url=access_token_url)
        access_token_res.raise_for_status()  # 检查响应状态码
        try:
            access_token_data = access_token_res.json()
        except json.JSONDecodeError:
            print(f"获取访问令牌时，响应内容不是有效的 JSON 格式: {access_token_res.text}")
            return
        send_headers = {
            "Content-Type": "application/json",
            "Accept": "application/json"
        }
        send_data = {
            "touser": "@all",
            "msgtype": "text",
            "agentid": wechat_app_id,
            "text": {
                "content": msg
            }
        }
        if "access_token" in access_token_data:
            access_token = access_token_data["access_token"]
            send_url = f"https://qyapi.weixin.qq.com/cgi-bin/message/send?access_token={access_token}"
            if len(msg) <= 1024:
                try:
                    send_res = requests.post(url=send_url,
                                             headers=send_headers,
                                             data=json.dumps(send_data))
                    send_res.raise_for_status()  # 检查响应状态码
                    try:
                        print(send_res.json())
                    except json.JSONDecodeError:
                        print(f"发送消息时，响应内容不是有效的 JSON 格式: {send_res.text}")
                except requests.RequestException as e:
                    print(f"发送消息请求出错: {e}")
            else:
                # 消息超过1024个字符，分多次发送
                split_msg = [msg[i:i + 1024] for i in range(0, len(msg), 1024)]
                for msgs in split_msg:
                    send_data["text"]["content"] = msgs
                    try:
                        res = requests.post(url=send_url,
                                            headers=send_headers,
                                            data=json.dumps(send_data))
                        res.raise_for_status()  # 检查响应状态码
                        try:
                            print(res.json())
                        except json.JSONDecodeError:
                            print(f"发送消息时，响应内容不是有效的 JSON 格式: {res.text}")
                    except requests.RequestException as e:
                        print(f"发送消息请求出错: {e}")
    except requests.RequestException as e:
        print(f"获取访问令牌请求出错: {e}")

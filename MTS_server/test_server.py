import requests

# 定义请求的URl
url = "http://127.0.0.1:5000/MTS_server/main_serve/"


while True:
    data = {"type": "0", "description": '"鼻塞", "呼吸困难"'}
    res = requests.post(url, data=data)
    print(res.text, end="\n\n")

    data = {"type": "1", "description": '我是傻逼，胸2痛，肚子疼，咳嗽呼吸困难'}
    res = requests.post(url, data=data)
    print(res.text)

    break

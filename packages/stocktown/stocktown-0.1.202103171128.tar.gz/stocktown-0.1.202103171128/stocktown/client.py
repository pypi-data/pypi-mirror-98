import requests

sess = requests.session()
headers = {"user-agent": "maro"}
sess.get("https://www.xueqiu.com", headers=headers)

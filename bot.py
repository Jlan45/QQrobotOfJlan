from flask import Flask, request
import time
from apscheduler.schedulers.blocking import BlockingScheduler
'''注意，这里的import api是另一个py文件，下文会提及'''
import requests
import pymysql
import api
app = Flask(__name__)

'''监听端口，获取QQ信息'''
@app.route('/', methods=["POST"])
def post_data():
    '下面的request.get_json().get......是用来获取关键字的值用的，关键字参考上面代码段的数据格式'
    if request.get_json().get('message_type')=='private':
        uid = request.get_json().get('sender').get('user_id')
        message = request.get_json().get('raw_message')
        note=f"{uid}给你发送了{message}"
        requests.get(f"http://192.168.123.112:5700/send_msg?user_id=405454586&message={note}")
        api.keywordForPerson(message,uid)
    if request.get_json().get('message_type')=='group':
        gid = request.get_json().get('group_id')
        uid = request.get_json().get('sender').get('user_id')
        message = request.get_json().get('raw_message')
        print(gid,uid,message)
        api.keywordForGroup(message, uid, gid)
    return 'OK'


if __name__ == '__main__':
    app.run(debug=True, host='127.0.0.1', port=5701)
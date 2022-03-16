from flask import request
import requests
import re
import os
import pymysql
import random
from datetime import date
from pydub import AudioSegment

def whoToAt(me):
    return re.findall(r'\d+',me)[0]
def wallpaper(message,uid,gid):
    photo=requests.get("https://api.sunweihu.com/api/bing1/api.php").url
    requests.get(f"http://127.0.0.1:5700/send_msg?group_id={gid}&message=[CQ:image,file={photo},type=show,id=40000]")
def weather(message,uid,gid):
    we=requests.get("http://wthrcdn.etouch.cn/weather_mini?city=徐州").json()['data']['forecast'][0]
    forecast=f"今日天气{we['type']}，最高{we['high'][3:]}，最低{we['low'][3:]}"
    url=f"http://127.0.0.1:5700/send_msg?group_id={gid}&message={forecast}"
    requests.get(url)
    print("kkkk")
def answer(message,uid,gid):
    if re.search(r'别理涣梦了',message):
        requests.get(f"http://127.0.0.1:5700/send_msg?group_id={gid}&message=好嘞！[CQ:at,qq=2189115140]不和你玩，哼")
def music(message,uid,gid):
    if message[0:2]=="搜索":
        keywords=message[2:]
        print(keywords)
        musicList=requests.get(f"http://localhost:3000/search?keywords={keywords}&limit=10").json()['result']
        if musicList['songCount']==0:
            sen="对不起，我也找不到有关的歌呜呜[CQ:face,id=5]"
        else:
            sen = "这些是我找到的歌："
            for index in range(len(musicList['songs'])):
                sen = sen+"\n" + musicList['songs'][index]['name'] + "——"
                for na in range(len(musicList['songs'][index]['artists'])):
                    if na==len(musicList['songs'][index]['artists'])-1:
                        sen = sen + musicList['songs'][index]['artists'][na]['name']
                    else:
                        sen = sen + musicList['songs'][index]['artists'][na]['name']+","
                sen =sen+" ID：" +str(musicList['songs'][index]['id'])
            sen=sen+"\n提示：发送 音乐 ID 对应歌曲的ID即可获取歌曲"
            sen=sen.replace('&','%26')
            requests.get(f"http://127.0.0.1:5700/send_msg?group_id={gid}&message={sen}")
    elif message[0:2]=="ID" or message[0:2]=="id" or message[0:2]=="Id":
        number = re.findall(r'\d+',message)
        for mu in number:
            requests.get(f"http://127.0.0.1:5700/send_msg?group_id={gid}&message=[CQ:music,type=163,id={mu}]")
            mus=requests.get(f"https://api.sunweihu.com/api/wyy/api.php?id={mu}").url
            filePath = f'music/{mu}.mp3'
            c = f"wget {mus} -c -T 10 -t 10 -O {filePath} --no-check-certificate"
            print(c)
            os.system(c)
            mp3 = AudioSegment.from_mp3(filePath)
            mp3[:60*1000].export(filePath, format="mp3")
            filePath="file:///root/QQrobot/py/"+filePath
            requests.get(f"http://127.0.0.1:5700/send_msg?group_id={gid}&message=[CQ:record,file={filePath}]")
def setu(message,uid,gid):
    db = pymysql.connect(host='localhost',user='root',password='56602388',database='QQ')
    cursor = db.cursor()
    cursor.execute(f"SELECT * from QQS where QQ='{uid}' and QQG='{gid}'")
    data = cursor.fetchone()
    print(data)
    if data==None:
        me=f"[CQ:at,qq={uid}]请先签到后再试"
        requests.get(f"http://127.0.0.1:5700/send_msg?group_id={gid}&message={me}")
        db.commit()
        db.close()
        return
    if data[3]<10:
        me=f"[CQ:at,qq={uid}]您当前剩余积分不够兑换涩图"
        requests.get(f"http://127.0.0.1:5700/send_msg?group_id={gid}&message={me}")
        db.commit()
        db.close()
        return
    for i in os.walk("/root/QQrobot/pho/"):
        num=random.randint(0,486)
        local=f"file:///root/QQrobot/pho/{i[2][num]}"
        me=f"[CQ:at,qq={uid}]LSP你的涩图[CQ:image,file={local},id=40000]"
        requests.get(f"http://127.0.0.1:5700/send_msg?group_id={gid}&message={me}")
        cursor.execute(f"update QQS set Score={data[3]-10} where QQ='{uid}' and QQG='{gid}'")
        db.commit()
        db.close()
# def setu18(message,uid,gid):
#     data=requests.get("https://api.lolicon.app/setu/v2?r18=1").json()['data'][0]
#     num=data['pid']
#     url=data['urls']['original']
#     ext=data['ext']
#     os.system(f"wget {url} -c -T 10 -t 10 -O photo/{num}.{ext} --no-check-certificate")
#     local=f"file:///root/QQrobot/py/photo/{num}.{ext}"
#     me=f"[CQ:at,qq={uid}]LSP你的涩图[CQ:image,file={local},id=40000]"
#     requests.get(f"http://127.0.0.1:5700/send_msg?group_id={gid}&message={me}")
def qiandao(uid,gid):
    db = pymysql.connect(host='localhost',user='root',password='56602388',database='QQ')
    cursor = db.cursor()
    cursor.execute(f"SELECT * from QQS where QQ='{uid}' and QQG='{gid}'")
    data = cursor.fetchone()
    if data==None:
        cursor.execute(f"insert into QQS (QQ,QQG) values('{uid}','{gid}')")
        db.commit()
    cursor.execute(f"SELECT * from QQS where QQ='{uid}' and QQG='{gid}'")
    data = cursor.fetchone()
    s=data[3]
    d=str(date.today())
    if(str(data[4])==d):
        sen="你今天签过到了，不可以重复白嫖哦"
        requests.get(f"http://127.0.0.1:5700/send_msg?group_id={gid}&message=[CQ:at,qq={uid}]{sen}")
        return
    cursor.execute(f"update QQS set Score={s+10},Date='{d}' where QQ='{uid}' and QQG='{gid}'")
    sen=f"签到成功，现有积分：{s+10}分"
    requests.get(f"http://127.0.0.1:5700/send_msg?group_id={gid}&message=[CQ:at,qq={uid}]{sen}")
    db.commit()
    db.close()
def chaxun(message,uid,gid):
    print(message)
    if message=='':
        requests.get(f"http://127.0.0.1:5700/send_msg?group_id={gid}&message=请按照查询 QQ号的格式进行查询")
        return
    db = pymysql.connect(host='localhost',user='root',password='56602388',database='QQ')
    cursor = db.cursor()
    cursor.execute(f"SELECT * from QQS where QQ='{message}' and QQG='{gid}'")
    db.commit()
    data = cursor.fetchone()
    sen=f"现有积分：{data[3]}分"
    requests.get(f"http://127.0.0.1:5700/send_msg?group_id={gid}&message=[CQ:at,qq={uid}]{sen}")
def unban(message,gid):
    uid=whoToAt(message)
    db = pymysql.connect(host='localhost',user='root',password='56602388',database='QQ')
    com=f"select ban from ban where uid='{uid}' and gid='{gid}'"
    cursor = db.cursor()
    cursor.execute(com)
    db.commit() 
    data=cursor.fetchone()
    requests.get(f"http://127.0.0.1:5700/send_msg?group_id={gid}&message=好吧，我不生你气了")
    if data==None:
        com=f"insert into ban values('{uid}','{gid}',0)"
        cursor.execute(com)
        db.commit()
        db.close()
        return
    com=f"update ban set ban=0 where uid='{uid}' and gid='{gid}'"
    cursor.execute(com)
    db.commit()
    db.close()
    print("unban")
def ban(message,gid):
    uid=whoToAt(message)
    db = pymysql.connect(host='localhost',user='root',password='56602388',database='QQ')
    com=f"select ban from ban where uid='{uid}' and gid='{gid}'"
    cursor = db.cursor()
    cursor.execute(com)
    db.commit() 
    data=cursor.fetchone()
    requests.get(f"http://127.0.0.1:5700/send_msg?group_id={gid}&message=好的我们不和他玩")
    if data==None:
        com=f"insert into ban values('{uid}','{gid}',1)"
        cursor.execute(com)
        db.commit()
        db.close()
        return
    com=f"update ban set ban=1 where uid='{uid}' and gid='{gid}'"
    cursor.execute(com)
    db.commit()
    db.close()
    print("ban")
    
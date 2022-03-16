from tokenize import group
import groupAPI
import re
import pymysql

def isInBanList(uid,gid):
    db = pymysql.connect(host='localhost',user='root',password='56602388',database='QQ')
    cursor = db.cursor()
    cursor.execute(f"SELECT ban from ban where uid='{uid}' and gid='{gid}'")
    data = cursor.fetchone()
    db.close()
    print(data)
    if data==None:
        return 0
    if data[0]==1:
        print("ban")
        return 1
    return 0
def keywordForGroup(message,uid,gid):
    if isInBanList(uid,gid):
        return
    elif re.search(r'天气',message):
        groupAPI.weather(message,uid,gid)
    elif message[0:2]=="音乐":
        groupAPI.music(message[3:],uid,gid)
    elif re.search(r'壁纸',message):
        groupAPI.wallpaper(message,uid,gid)
    elif re.search(r'setu18',message):
        groupAPI.setu18(message,uid,gid)
    elif message=='无内鬼':
        groupAPI.setu(message,uid,gid)
    elif message=='签到':
        groupAPI.qiandao(uid,gid)
    elif message[0:2]=='查询':
        groupAPI.chaxun(message[3:],uid,gid)
    elif message[0:3]=='ban' and uid==405454586:
        groupAPI.ban(message,gid)
    elif message[0:5]=='unban' and uid==405454586:
        groupAPI.unban(message,gid)
    else:
        groupAPI.answer(message,uid,gid)
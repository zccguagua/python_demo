import itchat
import json
import requests
import codecs
import pymysql
import re
import time
from apscheduler.schedulers.blocking import BlockingScheduler

my_UserName = "my_UserName"
message_dict = {
    "你最帅": "消息",
    "祝福": "消息",
    "佩奇": "消息",
}
# 记录消息数
message_record = {
    "userName": 1
}

reply_group = {1: "消息测试", 2: "疯狂找媳妇儿", 3: "不准时下班小组"}


def timed_message():
    user_info = itchat.search_friends(name='新雪初霁')
    if len(user_info) > 0:
        user_name = user_info[0]['UserName']
        itchat.send_msg('生日快乐哦！', toUserName=user_name)


def after_login():
    print("您已登录")
    # sched.add_job(timed_message, 'cron', year=2019, month=10, day=23, hour=13, minute=0, second=0)
    # sched.start()
    db = pymysql.connect(host='localhost',
                         user='root',
                         password='lonbon',
                         db='wechat',
                         charset='utf8mb4',
                         cursorclass=pymysql.cursors.DictCursor)
    cursor = db.cursor()  # 使用cursor()方法获取操作游标
    friends = itchat.get_friends(update=True)[0:]  # 获取好友信息
    print("好友:" + str(friends))

    for friend in friends:
        #     item = {'NickName': friend['NickName'],  # 昵称
        #             'UserName': friend['UserName'],  # 名称id（变化）
        #             'RemarkName': friend['RemarkName'],  # 备注名
        #             'Signature': friend['Signature'],  # 个性签名
        #             'Province': friend['Province'],
        #             'City': friend['City'],
        #             'MemberCount': friend['MemberCount'],
        #             'Sex': friend['Sex'],  # 0：其他，1：男，2：女
        #             'AttrStatus': friend['AttrStatus'],
        #             'SnsFlag': friend['SnsFlag'],
        #             'ContactFlag': friend['ContactFlag'],
        #             'HeadImgUrl': friend['HeadImgUrl']  # 头像地址
        #             }

        sql_select = "SELECT nickname,remarkname FROM contacts WHERE nickname =%s"
        try:
            cursor.execute(sql_select, (friend['NickName']))  # 查询群昵称在数据库是否存在
            result = cursor.fetchall()
            db.commit()
            if (len(result) > 0):
                sql = "UPDATE contacts SET username =%s,time=%s  WHERE nickname = %s"
                try:
                    cursor.execute(sql, (friend['UserName'], time.strftime("%Y-%m-%d %H:%M:%S", time.localtime()),
                                         friend['NickName']))  # 更新群id
                    db.commit()  # 提交到数据库执行
                except Exception as e:

                    # db.rollback()# 发生错误时回滚
                    print("sql_select_Error", e)
            else:
                sql_insert = """INSERT INTO contacts (nickname,username, remarkname
                   , signature, province,city,membercount,sex
                   ,attrstatus,snsflag,contactflag,headimgurl,time) VALUES ('%s','%s'
                   ,'%s','%s','%s','%s','%s','%s','%s','%s','%s','%s','%s')""" % (
                    str(friend['NickName']), str(friend['UserName']), str(friend['RemarkName'])
                    , str(friend['Signature']), str(friend['Province']), str(friend['City']), str(friend['MemberCount'])
                    , str(friend['Sex']), str(friend['AttrStatus']), str(friend['SnsFlag']), str(friend['ContactFlag'])
                    , str(friend['HeadImgUrl']), time.strftime("%Y-%m-%d %H:%M:%S", time.localtime()))

                cursor.execute(sql_insert)  # 执行sql语句
                db.commit()  # 提交到数据库执行

        except Exception as e:
            # db.rollback() # 发生错误时回滚
            print("sql_insert_Error", e)
        # finally:
        # 关闭数据库连接
        # cursor.close()
        # db.close()

    # 获得完整的群聊列表
    groups = itchat.get_chatrooms()
    print("获得完整的群聊列表:" + str(groups))
    for item in groups:
        sql_select_group = "SELECT nickname,remarkname FROM groups WHERE nickname =%s"
        try:
            cursor.execute(sql_select_group, (item['NickName']))  # 查询好友昵称在数据库是否存在
            result = cursor.fetchall()
            db.commit()
            if (len(result) > 0):
                print("已存在群：" + item['NickName'])
                sql_update_group = "UPDATE groups SET username =%s,time=%s  WHERE nickname = %s"  # 更新好友的id
                try:
                    cursor.execute(sql_update_group, (
                        item['UserName'], time.strftime("%Y-%m-%d %H:%M:%S", time.localtime()), item['NickName']))
                    db.commit()
                except Exception as e:
                    # 发生错误时回滚
                    # db.rollback()
                    print("发生了错误")
                    print("Error", e)
            else:
                sql_insert_group = """INSERT INTO groups (nickname,username, remarkname
                , signature, province,city,membercount,sex
                ,attrstatus,snsflag,contactflag,headimgurl,time) VALUES ('%s','%s'
                ,'%s','%s','%s','%s','%s','%s','%s','%s','%s','%s','%s')""" % (
                    str(item['NickName']), str(item['UserName']), str(item['RemarkName'])
                    , str(item['Signature']), str(item['Province']), str(item['City']), str(item['MemberCount'])
                    , str(item['Sex']), str(item['AttrStatus']), str(item['SnsFlag']), str(item['ContactFlag'])
                    , str(item['HeadImgUrl']), time.strftime("%Y-%m-%d %H:%M:%S", time.localtime()))

                cursor.execute(sql_insert_group)
                db.commit()

        except Exception as e:
            # db.rollback() # 发生错误时回滚
            print("sql_select_group_Error", e)
        # finally:
        # 关闭数据库连接
    cursor.close()
    db.close()


def after_logout():
    print("已退出")


def save_data(frined_list):
    out_file_name = "./data/xiaohao.json"
    with codecs.open(out_file_name, 'w', encoding='utf-8') as json_file:
        json_file.write(json.dumps(frined_list, ensure_ascii=False))


# @itchat.msg_register(itchat.content.MAP)  # 位置文本
# @itchat.msg_register(itchat.content.NOTE)  # 通知文本
# @itchat.msg_register(itchat.content.PICTURE)  # 监听图片/表情
# @itchat.msg_register(itchat.content.FRIENDS)  # 好友邀请
# @itchat.msg_register(itchat.content.VIDEO)  # 监听视频
@itchat.msg_register(itchat.content.TEXT)  # 监听文本内容
def print_content(msg):
    print("msg是：" + str(msg))
    NickName = msg['User']['NickName']  # 对方名字
    FromUserName = msg['FromUserName']  # 发送人的id
    user = itchat.search_friends(name=NickName)[0]  # 获取特定UserName的用户信息
    text = msg['Text']  # 发送的文字消息
    print("my_UserName:" + my_UserName)
    if FromUserName != my_UserName:
        hasKey = False
        theKey = ""
        for key in message_dict.keys():
            if (key in text):
                hasKey = True
                theKey = key
        if (hasKey):
            print("找到关键字:" + str(theKey))
            user.send("检测到关键字：" + str(theKey))  # message_dict[theKey]
            # user.send_image("./image/209717696.jpg")  # 发送图片
            # user.send_file("cat.py")  # 发送文件
            # user.send_file("cat.mp4")  # 发送视频
        else:
            print("字典里没有关键字")
            if (NickName in message_record.keys()):
                print("已经发送过了")
                message_record.update({str(NickName): 2})
            else:
                message_record.update({str(NickName): 1})
                user.send(u"亲爱的 %s,你好啊" % NickName)
                user.send_image("./image/2.jpg")
    else:
        print("yourself")


@itchat.msg_register(itchat.content.TEXT, isGroupChat=True)
def reply_msg(msg):
    # print("收到一条群信息：", msg['ActualNickName'], msg['Content'])
    print("收到一条群信息：", str(msg))
    # chat_rooms = itchat.search_chatrooms(name='消息测试')
    # if len(chat_rooms) > 0:
    #     itchat.send_msg('测试：这是一条自动回复消息,您发的消息是：%s' % msg['Content'], chat_rooms[0]['UserName'])

    from_user = msg['FromUserName']  # 来自谁的消息（自己发的是自己的id,其他人发的是群id）
    content = msg['Content']
    print(content)
    db_conn = pymysql.connect(host='localhost',
                              user='root',
                              password='lonbon',
                              db='wechat',
                              charset='utf8mb4',
                              cursorclass=pymysql.cursors.DictCursor)

    cursor = db_conn.cursor()
    sql_select = "SELECT nickname,remarkname FROM groups WHERE username =%s"
    try:
        cursor.execute(sql_select, (from_user))  # 查询群昵称在数据库是否存在
        result = cursor.fetchall()
        db_conn.commit()
        if (len(result) > 0):
            print("已存在：" + str(result))
            groups_name = str(result[0]['nickname'])
            print("已存在：" + groups_name)  # 群名称
            if (groups_name in reply_group.values()):
                # chat_rooms = itchat.search_chatrooms(name=groups_name)
                # if (len(chat_rooms) > 0):
                #     itchat.send_msg('测试：这是一条自动回复消息,群昵称：%s,消息是：%s' % (content, groups_name), chat_rooms[0]['UserName'])
                # else:
                #     print("chat_rooms_len==0")
                try:
                    itchat.send_msg('测试：这是一条自动回复消息,群昵称：%s,消息是：%s' % (content, groups_name), from_user)
                except:
                    print("发送失败")
            else:
                print("不在自动恢复列表里")

        else:
            print("未找到群")
            # sql_insert_group = """INSERT INTO groups (nickname,username, remarkname
            #                 , signature, province,city,membercount,sex
            #                 ,attrstatus,snsflag,contactflag,headimgurl,time) VALUES ('%s','%s'
            #                 ,'%s','%s','%s','%s','%s','%s','%s','%s','%s','%s','%s')""" % (
            #     str(msg['NickName']), str(msg['UserName']), str(msg['RemarkName'])
            #     , str(msg['Signature']), str(msg['Province']), str(msg['City']), str(msg['MemberCount'])
            #     , str(msg['Sex']), str(msg['AttrStatus']), str(msg['SnsFlag']), str(msg['ContactFlag'])
            #     , str(msg['HeadImgUrl']), time.strftime("%Y-%m-%d %H:%M:%S", time.localtime()))
            # cursor.execute(sql_insert_group)
            # db_conn.commit()
    except Exception as e:
        # db.rollback() # 发生错误时回滚
        print("Error", e)
    finally:
        # 关闭数据库连接
        cursor.close()
        db_conn.close()


if __name__ == '__main__':
    # sched = BlockingScheduler()
    itchat.auto_login(loginCallback=after_login, exitCallback=after_logout)
    result = itchat.search_friends()  # 获取自己的用户信息，返回自己的属性字典
    # my_name = result.NickName
    my_UserName = result.UserName  # 我的id（用于判断是否是我发的消息）
    itchat.run()

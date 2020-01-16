"""
author : Levi
email : lvze@tedu.cn
env : python3.6
AID1911: socket  fork
"""

from socket import *
import os
import sys

# 有特定意义的变量，或者很多函数/类中都会频繁使用的变量
ADDR = ('0.0.0.0', 8888)

# 创建用户存储字典 {name:address}
user = {}


# 用户登录
def do_login(s, name, addr):
    if name in user or '管理' in name:
        s.sendto("该用户存在".encode(), addr)
        return
    else:
        s.sendto(b'OK', addr)
        # 通知其他人
        msg = "\n欢迎'%s'加入群聊" % name
        for i in user:
            s.sendto(msg.encode(), user[i])
        user[name] = addr  # 加入user字典


# 聊天
def do_chat(s, name, text):
    msg = "\n%s : %s" % (name, text)
    for i in user:
        # 刨除本人
        if i != name:
            s.sendto(msg.encode(), user[i])


# 退出
def do_quit(s, name):
    msg = "\n%s 离开聊天室" % name
    for i in user:
        if i != name:
            # 其他人
            s.sendto(msg.encode(), user[i])
        else:
            s.sendto(b'QUIT', user[i])
    del user[name]  # 删除用户


# 接受请求，分发任务
def do_request(s):
    while True:
        # 所有请求都在这里接受
        data, addr = s.recvfrom(1024)
        tmp = data.decode().split(' ', 2)  # 拆分请求
        # 任务分发 (LOGIN CHAT QUIT)
        if tmp[0] == "LOGIN":
            do_login(s, tmp[1], addr)
        elif tmp[0] == "CHAT":
            do_chat(s, tmp[1], tmp[2])
        elif tmp[0] == "QUIT":
            if tmp[1] in user:
                do_quit(s, tmp[1])


# 搭建网络
def main():
    # udp服务端网络
    s = socket(AF_INET, SOCK_DGRAM)
    s.bind(ADDR)

    pid = os.fork()
    if pid < 0:
        return
    elif pid == 0:
        # 发送管理员消息
        while True:
            text = input("管理员消息:")
            msg = "CHAT 管理员 " + text
            s.sendto(msg.encode(),ADDR)
    else:
        # 请求处理函数
        do_request(s)


if __name__ == '__main__':
    main()

#!/usr/bin/env python
# -*- coding:utf-8 -*-

import json
import tornado.web
import tornado.websocket
import tornado.httpserver
import tornado.ioloop
import tornado.options
from uuid import uuid4

#服务器与客户端连接实例
class ChatRoom(object):
    '''
    users字典关键字表示聊天室，值表示用户
    newUser()创建连接
    exit()删除连接
    receiveMessage()接受消息
    sendMessage()发送消息
    '''

    users={}
    #history={'1':[],'2':[]}
    history={}
    #聊天室加入新人，建立客户端的连接，提示给聊天室内全员新用户加入
    def newUser(self,newMan):
        username = str(newMan.get_argument('username'))  # 获取用户名
        room = str(newMan.get_argument('n'))     #获取所在聊天室
        if room in self.users:
           self.users[room].append(newMan)         #加入聊天室
        else:
            self.users[room]=[newMan]
        message = {
            'from': 'system',
            'message' : '%s 加入聊天室（%s）' % (username, room)
        }
        self.sendMessage(room,message)
        self.loadHistory(newMan)

    #客户端用户退出聊天室，删除该聊天室内该用户的连接，提示聊天室内全员有用户离开
    def exit(self,quitter):
        room = str(quitter.get_argument('n'))
        self.users[room].remove(quitter)
        if self.users[room]:
            message = {
                'from': 'system',
                'message': '%s 离开聊天室（%s）' % (str(quitter.get_argument('username')), room)
            }
            self.sendMessage(room, message)

    #接受个体用户端的消息，并发送给聊天室内全体用户端
    def receiveMessage(self,sender,message):
        room = str(sender.get_argument('n'))
        username = str(sender.get_argument('username'))
        message = {
            'from': username,
            'message': message
        }
        self.sendMessage(room, message)

        if room in self.history:
            self.history[room].append(message)
        else:
            self.history[room]=[message]


    #发送一条消息给所有客户端
    def sendMessage(self,room,message):
        for user in self.users[room]:
            user.write_message(json.dumps(message))

    def loadHistory(self,man):
        room = man.get_argument('n')
        if room in self.history:
            for ms in self.history[room]:
                man.write_message(json.dumps(ms))


class LoginHandler(tornado.web.RequestHandler):
    '''进行登陆'''
    def get(self):
        self.render('login.html')

class RoomHandler(tornado.web.RequestHandler):
    room = ["1","2"]
    def get(self):
        session = uuid4()
        username = str(self.get_argument('username'))
        self.render(r'basic.html',room=self.room,session=session,username=username)
    def post(self):
        self.room.append(str(len(self.room)+1))
        self.get()

class ChatHandler(tornado.web.RequestHandler):
    def get(self):
        n = self.get_argument('n')      #聊天室
        u = self.get_argument('u')      #用户
        username = self.get_argument('username')
        self.render(r'chat.html',n=n,u=u,username=username)

class UpdatesMssageHandler(tornado.websocket.WebSocketHandler):
    '''
        websocket， 记录客户端连接，删除客户端连接，接收最新消息
    '''
    def open(self):
        self.application.chatroom.newUser(self)    #记录客户端连接

    def on_close(self):
        self.application.chatroom.exit(self)  #删除客户端连接

    def on_message(self, message):
        self.application.chatroom.receiveMessage(self, message)   #处理客户端提交的最新消息


class Application(tornado.web.Application):
    def __init__(self):
        self.chatroom = ChatRoom()
        handlers=[
            (r'/', LoginHandler),
            (r'/room', RoomHandler),
            (r'/chat/', ChatHandler),
            (r'/chat/update/', UpdatesMssageHandler),
        ]
        settings = {
            'template_path': 'templates',
            'static_path': 'static',
        }
        tornado.web.Application.__init__(self, handlers, **settings)

if __name__ == "__main__":
    tornado.options.parse_command_line()
    server = tornado.httpserver.HTTPServer(Application())
    server.listen(8888)
    tornado.ioloop.IOLoop.instance().start()

#!/usr/bin/env python
# -*- coding:utf-8 -*-

import tornado.ioloop
import tornado.web
import numpy as np


namelist = []
luckyList1 = []
luckyList2 = []
luckyList3 = []

class indexHandler(tornado.web.RequestHandler):
    def get(self):
        self.render('index.html')

class lotteryHandler(tornado.web.RequestHandler):
    def get(self):
        self.render('lottery.html',count=len(namelist))
    def post(self):
        names = self.get_argument('namelist')
        global namelist
        for i in names.split('\n'):
            if i:
                namelist.append(i)
        temp = namelist
        self.redirect('/lottery')


class showHandler(tornado.web.RequestHandler):
    def post(self):
        global namelist,luckyList1,luckyList2,luckyList3
        firstNum = int(self.get_argument('first'))  # 内部调用的self.request（）模块
        secondNum = int(self.get_argument('second'))
        thirdNum = int(self.get_argument('third'))
        #抽取幸运者,np.random.choice()返回的类型是<class 'numpy.ndarray'>
        #这个类型可以强制改变类型为集合，列表，replace=False,表示元素不可重复
        if (firstNum+secondNum+thirdNum)>len(namelist):
            self.write("""<script>alert("剩余人数不够抽奖。")</script>""")
        else:
            luckyList1 = np.random.choice(namelist, firstNum,replace=False)
            namelist = list(set(namelist) - set(luckyList1))
            luckyList2 = np.random.choice(namelist, secondNum,replace=False)
            namelist = list(set(namelist) - set(luckyList2))
            luckyList3 = np.random.choice(namelist, thirdNum,replace=False)
            namelist = list(set(namelist) - set(luckyList3))
            self.render('show.html', winners1=luckyList1, winners2=luckyList2, winners3=luckyList3)

application = tornado.web.Application([
    (r"/", indexHandler),
    (r"/lottery",lotteryHandler),
    (r"/show",showHandler),]
)

# 开启服务器，监听
if __name__ == "__main__":
    application.listen(8888)
    tornado.ioloop.IOLoop.instance().start()
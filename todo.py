#!/usr/bin/env python
# -*- coding: utf-8 -*-

# set local-packages into python path
import sys
import os
root = os.path.dirname(__file__)
sys.path.insert(0, os.path.join(root, 'local-packages'))
#end

import tornado.web
import tornado.ioloop
from tornado.options import options, define
import redis
import Base
import time
import hashlib
import uuid



class BaseHandler(tornado.web.RequestHandler):
    def get_current_user(self):
        username =  self.get_secure_cookie("todo_username")
        return username #这里由于本程序直接用username生成cookie，直接有get_secure_cookie即可得用户名，实际项目中应用userid来生成cookie，再用userid查数据库找出对应username

    @property
    def redis(self):
        return self.application.redis

    def _encrypt_passwd(self, username, password):
        md5 = hashlib.md5(username+password+'cm_Lighters')      #"cm_Lighters as 'the-Salt'"
        return md5.hexdigest()

    def write_error(self, status_code, **kwargs):
        if status_code == 404:
            self.render('404.html')


# 注册模块，记录用户名和密码，校验用户名和密码正确性，密码加密存储
class SignUpHandler(BaseHandler):
    def get(self):
        self.render("join.html", error_hints=None)

    def post(self):
        username = self.get_argument("username", None)
        password1 = self.get_argument("password1", None)
        password2 = self.get_argument("password2", None)
        print username + '*'*20 + password1 + '*'*20 + password2
        if password1 != password2:
            self.render("join.html", error_hints="两次密码输入不同！")
            return
        if self.redis.hexists('todo_user', username):
            self.render("join.html", error_hints="用户名已经存在！")
            return
        encry_passwd = self._encrypt_passwd(username, password1)
        self.redis.hset('todo_user', username, encry_passwd)
        self.redirect("/login")


class SignInHandler(BaseHandler):
    def get(self):
        self.render("login.html", error_hints=None)

    def post(self):
        username = self.get_argument("username", None)
        password = self.get_argument("password", None)
        if self.redis.hexists('todo_user', username) and self.redis.hget('todo_user', username) == self._encrypt_passwd(username, password):
            self.set_secure_cookie("todo_username", username)
            self.redirect("/")
        else:
            self.render("login.html", error_hints="username or password error, please relogin again")


class SignOutHandler(BaseHandler):
    def get(self):
        self.clear_cookie("todo_username")
        self.redirect("/")


class MainHandler(BaseHandler):
    @tornado.web.authenticated
    def get(self):
        entries = self.redis.lrange('todo_'+ self.current_user+'_entries', 0, -1)
        self.render("home.html", user = self.current_user, entries=entries)

    @tornado.web.authenticated
    def post(self):
        print str(self.request.arguments) + '*'*40 + '\n'
        content = self.get_argument("todo_entry")
        self.redis.rpush('todo_'+self.current_user+'_entries', content)
        self.redirect('/')


class DeleteHandler(BaseHandler):
    @tornado.web.authenticated
    def get(self):
        id = self.get_argument("id", None)
        if id:
            self.redis.lset('todo_'+self.current_user+'_entries', int(id), "*del*entry*")
            self.redis.lrem('todo_'+self.current_user+'_entries', "*del*entry*", 0)
        self.redirect('/')


class Application(tornado.web.Application):
    def __init__(self):
        handlers = [
            (r"/", MainHandler),
            (r"/del", DeleteHandler),
            (r"/join", SignUpHandler),
            (r"/login", SignInHandler),
            (r"/logout", SignOutHandler),
        ]
        settings = dict(
            debug= True,
            template_path = os.path.join(os.path.dirname(__file__), "templates"),
            static_path = os.path.join(os.path.dirname(__file__), "static"),
            cookie_secret = "3AVYlROKQU+dAETGAwgvducr8z1DAUkvlLV6guVnBcc=",         # base64.b64encode(uuid.uuid4().bytes + uuid.uuid4().bytes)
            login_url = "/login",
        )
        super(Application, self).__init__(handlers, **settings)

        self.redis = redis.Redis('localhost', 6379)


if __name__ == '__main__':
    application = Application()
    application.listen(8888)
    tornado.ioloop.IOLoop.instance().start()

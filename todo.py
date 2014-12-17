#!/usr/bin/env python
# -*- coding: utf-8 -*-


import sys
import os
root = os.path.dirname(__file__)
sys.path.insert(0, os.path.join(root, 'local-packages'))

print sys.path        


import tornado.web 
import tornado.ioloop
from tornado.options import options, define
import redis
import Base
import time




"""
封装application
class MyApplication(tornado.web.Application):
    def __init__(self):
        handlers = [
            (r"/", MainHandler),
        ]

        settings = dict(
            debug = True,
            template_path = os.path.join(os.path.dirname(__file__), "templates"

db_conn = torndb.Connection(options.mysql_host, options.mysql_database,
        options.mysql_user, options.mysql_password)     #time_zone='+08:00'
"""

cache = redis.Redis('localhost', 6379)
#cache.set('entry_id', 0)      #entry_id 用于记录entry项的标识，第一项从1开始


class MainHandler(tornado.web.RequestHandler):
    def get(self):
     #   entries = db_conn.query("select * from entries order by sub_time")
        entries_list = cache.keys('entry:*')
        entries = [ Base.Storage(cache.hgetall(i)) for i in entries_list ]
        entries.sort(key = lambda entry: entry.id)
        print entries
        self.render("home.html", entries=entries)

    def post(self):
        print str(self.request.arguments) + '*'*40 + '\n'
        content = self.get_argument("todo_entry")
        entry_id = cache.incr('entry_id')
        cache.hmset("entry:"+ str(entry_id), Base.Storage({'id': entry_id, 'content': content, 'sub_time': time.ctime()}))
        self.redirect('/')


class DeleteHandler(tornado.web.RequestHandler):
    def get(self):
        id = self.get_argument("id", None)
        if id:
         #   db_conn.execute("delete from entries where entry_id=%s", id)
            cache.delete("entry:"+id)
        self.redirect('/')


settings = dict(
    debug= True,
    template_path = os.path.join(os.path.dirname(__file__), "templates"),
    static_path = os.path.join(os.path.dirname(__file__), "static"),
)

application = tornado.web.Application([
    (r"/", MainHandler),
    (r"/del", DeleteHandler),
    ], **settings
)

if __name__ == '__main__':
    application.listen(8888)
    tornado.ioloop.IOLoop.instance().start()

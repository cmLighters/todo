#!/usr/bin/env python
# -*- coding: utf-8 -*-

import tornado.web 
import tornado.ioloop
from tornado.options import options, define
import os
import torndb


define("mysql_host", default="127.0.0.1:3306", help="mysql host and port")
define("mysql_database", default="todo", help="my todo list")
define("mysql_user", default="cm", help="mysql user name")
define("mysql_password", default=" ", help="mysql user cm's password")


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
"""

db_conn = torndb.Connection(options.mysql_host, options.mysql_database,
        options.mysql_user, options.mysql_password)     #time_zone='+08:00'

class MainHandler(tornado.web.RequestHandler):
    def get(self):
        entries = db_conn.query("select * from entries order by sub_time desc")
        self.render("home.html", entries=entries)

settings = dict(
    debug= True,
    template_path = os.path.join(os.path.dirname(__file__), "templates"),
    static_path = os.path.join(os.path.dirname(__file__), "static"),
)

application = tornado.web.Application([
    (r"/", MainHandler),
    ], **settings
)

if __name__ == '__main__':
    application.listen(8888)
    tornado.ioloop.IOLoop.instance().start()

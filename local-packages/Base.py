#/usr/bin/env python
# -*- coding: utf-8

class Storage(dict):
    def __getattr__(self, key):
        try:
            return self[key]
        except KeyError, e:
            raise AttributeError, e

    def __setattr__(self, key, val):
        self[key] = val

    def __delattr__(self, key):
        try:
            del self[key]
        except KeyError, e:
            raise AttributeError, e

    def __repr__(self):
        return '<Storage ' + super(Storage, self).__repr__() + '>'

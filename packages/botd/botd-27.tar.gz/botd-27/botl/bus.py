# This file is placed in the Public Domain.

from . import Object, save

class Bus(Object):

    objs = []

    def __call__(self, *args, **kwargs):
        return Bus.objs

    def __iter__(self):
        return iter(Bus.objs)

    @staticmethod
    def add(obj):
        Bus.objs.append(obj)

    @staticmethod
    def announce(txt):
        for h in Bus.objs:
            h.announce(txt)

    @staticmethod
    def by_orig(orig):
        for o in Bus.objs:
            if repr(o) == orig:
                return o
    @staticmethod
    def resume():
        for o in Bus.objs:
            o.resume()

    @staticmethod
    def save():
        for o in Bus.objs:
            save(o)

    @staticmethod
    def say(orig, channel, txt):
        for o in Bus.objs:
            if repr(o) == orig and not o.stopped:
                o.say(channel, str(txt))

    @staticmethod
    def wait(t=None, timeout=5.0):
        for h in Bus.objs:
            if t and not isinstance(h, t):
                continue
            h.wait(timeout)

def by_orig(o):
    return Bus.by_orig(o)

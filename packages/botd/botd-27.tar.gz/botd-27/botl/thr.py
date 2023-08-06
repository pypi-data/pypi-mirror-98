# This file is placed in the Public Domain.

import queue
import threading
import time
import types

from botl import Default

starttime = time.time()

class Thr(threading.Thread):

    def __init__(self, func, *args, thrname="", daemon=True):
        super().__init__(None, self.run, thrname, (), {}, daemon=daemon)
        self._name = thrname or get_name(func)
        self._result = None
        self._queue = queue.Queue()
        self._queue.put_nowait((func, args))
        self.sleep = 0

    def __iter__(self):
        return self

    def __next__(self):
        for k in dir(self):
            yield k

    def join(self, timeout=None):
        ""
        super().join(timeout)
        return self._result

    def run(self):
        ""
        func, args = self._queue.get_nowait()
        if args:
            try:
                target = Default(vars(args[0]))
                self._name = (target and target.txt and target.txt.split()[0]) or self._name
            except TypeError:
                pass
        self.setName(self._name)
        self._result = func(*args)

    def wait(self, timeout=None):
        super().join(timeout)
        return self._result

def get_name(o):
    t = type(o)
    if t == types.ModuleType:
        return o.__name__
    try:
        n = "%s.%s" % (o.__self__.__class__.__name__, o.__name__)
    except AttributeError:
        try:
            n = "%s.%s" % (o.__class__.__name__, o.__name__)
        except AttributeError:
            try:
                n = o.__class__.__name__
            except AttributeError:
                n = o.__name__
    return n

def launch(func, *args, **kwargs):
    name = kwargs.get("name", get_name(func))
    t = Thr(func, *args, thrname=name, daemon=True)
    t.start()
    return t

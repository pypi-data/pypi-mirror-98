# This file is placed in the Public Domain.

import os
import queue
import sys
import threading
import time
import _thread

from . import Object, ObjectList, cfg, direct, j, spl, update
from .bus import Bus
from .evt import Command
from .thr import launch
from .itr import find_cmds, scan
from .utl import locked, has_mod

loadlock = _thread.allocate_lock()

class Handler(Object):

    table = Object()
    pnames = Object()
    modnames = Object()
    names = ObjectList()

    def __init__(self, *args, **kwargs):
        super().__init__()
        self._connected = threading.Event()
        self.cbs = Object()
        self.cmds = Object()
        self.pkgs = "botl,botl.cmd"
        self.queue = queue.Queue()
        self.started = False
        self.stopped = False
        if not args:
            from .tbl import tbl
        else:
            tbl = args[0]
        Handler.names.update(tbl["names"])
        update(Handler.modnames, tbl["modnames"])
        update(Handler.pnames, tbl["pnames"])

    def add(self, cmd, func):
        self.cmds[cmd] = func
        Handler.modnames[cmd] = func.__module__

    def announce(self, txt):
        pass

    def cmd(self, txt):
        c = Command(txt)
        c.orig = repr(self)
        cb_cmd(self, c)
        c.wait()

    def clone(self, hdl):
        update(self.cmds, hdl.cmds)

    def direct(self, txt):
        pass

    def dispatch(self, event):
        if event.type and event.type in self.cbs:
            self.cbs[event.type](self, event)

    def get_cmd(self, cmd):
        if cmd not in self.cmds:
            mn = getattr(Handler.modnames, cmd, None)
            if mn:
                self.load(mn)
        return getattr(self.cmds, cmd, None)

    def get_mod(self, mn):
        if mn in Handler.table:
            return Handler.table[mn]

    def get_names(self, nm):
        return getattr(Handler.names, nm, [nm,])

    def init(self, mns):
        thrs = []
        result = []
        for mn in spl(mns):
            mn = getattr(Handler.pnames, mn, mn)
            mod = self.load(mn)
            if mod and "init" in dir(mod):
                thrs.append(launch(mod.init, self))
        for thr in thrs:
            result.append(thr.join())
        return result

    @locked(loadlock)
    def load(self, mn):
        if not "." in mn:
            return None
        mnn = getattr(Handler.pnames, mn, mn)
        mod = direct(mnn)
        cmds = find_cmds(mod)
        update(self.cmds, cmds)
        Handler.table[mn] = mod
        return mod

    def load_mod(self, mns):
        mods = []
        for mn in spl(mns):
            mods.append(self.load(mn))
        return [x for x in mods if x]

    def load_all(self):
        for mn in self.pnames:
            self.load(mn)

    def handler(self):
        self.running = True
        while not self.stopped:
            e = self.queue.get()
            if not e:
                break
            if not e.orig:
                e.orig = repr(self)
            e.thrs.append(launch(self.dispatch, e))

    def put(self, e):
        if not self.started:
            self.start()
        self.queue.put_nowait(e)

    def register(self, name, callback):
        self.cbs[name] = callback

    def resume(self):
        pass

    def say(self, channel, txt):
        if not self.stopped:
            self.direct(txt)

    def scandir(self, path, name=""):
        if not os.path.exists(path):
            return
        if not name:
            name = path.split(os.sep)[-1]
        r = os.path.dirname(path)
        if r not in sys.path:
            sys.path.insert(0, r)
        for mn in [x[:-3] for x in os.listdir(path)
                   if x and x.endswith(".py")
                   and not x.startswith("__")
                   and not x == "setup.py"]:
            fqn = "%s.%s" % (name, mn)
            if not has_mod(fqn):
                continue
            mod = self.load(fqn)
            scan(self, mod)

    def scandirs(self):
        for p in cfg.pkgs:
            self.scandir(j(cfg.wd, p))

    def start(self):
        self.started = True
        launch(self.handler)
        return self

    def stop(self):
        self.stopped = True
        self.queue.put(None)

    def wait(self, timeout=5.0):
        while not self.stopped:
            time.sleep(timeout)

class Core(Handler):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.register("cmd", cb_cmd)
        Bus.add(self)

def cb_cmd(hdl, obj):
    obj.parse()
    f = hdl.get_cmd(obj.cmd)
    res = None
    if f:
        res = f(obj)
        obj.show()
    obj.ready()
    return res

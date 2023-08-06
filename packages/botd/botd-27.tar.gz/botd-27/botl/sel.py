# This file is placed in the Public Domain.

import os
import selectors

from . import get_name
from .evt import Event
from .hdl import Handler
from .thr import launch

class EDISCONNECT(Exception):

    pass

class Select(Handler):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self._select = selectors.DefaultSelector()
        self.stopped = False

    def select(self, once=False):
        while not self.stopped:
            try:
                sel = self._select.select(1.0)
            except OSError:
                if once:
                    break
                continue
            for fd, mask in sel:
                e = self.poll(fd.fd)
                self.put(e)
                e.wait()
            if once:
                break

    def poll(self, fd):
        f = os.fdopen(fd, "r")
        e = Event()
        e.txt = f.readline()
        return e

    def register_fd(self, fd):
        #try:
        #    fd = fd.fileno()
        #except AttributeError:
        #    fd = fd
        self._select.register(fd, selectors.EVENT_READ|selectors.EVENT_WRITE)
        return fd

    def stop(self):
        self._select.close()
        super().stop()

    def start(self):
        launch(self.select, name="%s.select" % get_name(self), daemon=True)
        super().start()

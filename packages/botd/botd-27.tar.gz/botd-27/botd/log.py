# This file is in the Public Domain.

from botl import Object, save

class Log(Object):

    def __init__(self):
        super().__init__()
        self.txt = ""

def log(event):
    if not event.rest:
        return
    o = Log()
    o.txt = event.rest
    save(o)
    event.reply("ok")

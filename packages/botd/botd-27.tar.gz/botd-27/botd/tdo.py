# This file is in the Public Domain.

from botl import Object, save
from botl.dbs import find

class Todo(Object):

    def __init__(self):
        super().__init__()
        self.txt = ""

def dne(event):
    if not event.args:
        return
    selector = {"txt": event.args[0]}
    for fn, o in find("mod.tdo.Todo", selector):
        o._deleted = True
        save(o)
        event.reply("ok")
        break

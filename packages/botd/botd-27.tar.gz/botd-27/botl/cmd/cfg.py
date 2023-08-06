# This file is in the Public Domain.

from botl import edit, format, save
from botl.dbs import last
from botl.irc import Cfg

def cfg(event):
    c = Cfg()
    last(c)
    if not event.sets:
        return event.reply(format(c, skip=["username", "realname"]))
    edit(c, event.sets)
    save(c)
    event.reply("ok")

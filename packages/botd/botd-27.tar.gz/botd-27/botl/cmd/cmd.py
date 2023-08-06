# This file is in the Public Domain.

from botl.bus import by_orig

def cmd(event):
    b = by_orig(event.orig)
    event.reply(",".join(sorted(b.modnames)))


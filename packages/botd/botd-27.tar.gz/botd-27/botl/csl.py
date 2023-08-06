# This file is in the Public Domain.

import atexit
import os
import readline
import sys
import termios

from . import cdir, cfg, j, op, update
from .evt import Command, Event
from .hdl import Core
from .prs import parse as myparse
from .sel import Select
from .thr import launch

cmds = []
resume = {}

def init(hdl):
    c = Console()
    c.clone(hdl)
    c.start()
    return c

class Shell(Core):

    def direct(self, txt):
        if not self.stopped:
            print(txt)

    def input(self):
        while not self.stopped:
            try:
                e = self.poll()
            except EOFError:
                break
            if e.cmd == "stop":
                break
            self.put(e)
            e.wait()

class Console(Shell):

    def poll(self):
        return Command(input("> "))

    def start(self):
        super().start()
        launch(self.input)
        return self

class SelectConsole(Select, Shell):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.register_fd(sys.stdin)

    def poll(self, fd):
        return Command(input("> "))

class Test(Core):

    def direct(self, txt):
        if op("v") and not self.stopped:
            print(txt)

def termsetup(fd):
    return termios.tcgetattr(fd)

def termreset():
    if "old" in resume:
        try:
            termios.tcsetattr(resume["fd"], termios.TCSADRAIN, resume["old"])
        except termios.error:
            pass

def termsave():
    try:
        resume["fd"] = sys.stdin.fileno()
        resume["old"] = termsetup(sys.stdin.fileno())
        atexit.register(termreset)
    except termios.error:
        pass

def complete(text, state):
    matches = []
    if text:
        matches = [s for s in cmds if s and s.startswith(text)]
    else:
        matches = cmds[:]
    try:
        return matches[state]
    except IndexError:
        return None

def exec(main):
    termsave()
    try:
        main()
    except (KeyboardInterrupt, PermissionError):
        pass
    finally:
        termreset()

def parse():
    myparse(cfg, " ".join(sys.argv[1:]))
    update(cfg, cfg.sets)
    sd = j(cfg.wd, "store")
    if not os.path.exists(sd):
        cdir(sd)
    return cfg

def setcompleter(commands):
    cmds.extend(commands)
    readline.set_completer(complete)
    readline.parse_and_bind("tab: complete")
    atexit.register(lambda: readline.set_completer(None))

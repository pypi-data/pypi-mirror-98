import readline
readline.parse_and_bind('tab: complete')
readline.parse_and_bind('set editing-mode vi')

from cmd import Cmd

from setux.main import banner
from setux.logger import logger
from .helps import helps
from . import commands


def help(cmd=None):
    def title(txt):
        print(txt)
        print('-'*len(txt))

    if cmd:
        hlp = helps.get(cmd)
        if hlp:
            title(cmd)
            print(hlp)
        else:
            print(f'unkown command "{cmd}"')
    else:
        title('commands')
        width = len(max(helps.keys(), key=len))+4
        for cmd, hlp in sorted(helps.items()):
            first = hlp.split('\n')[0]
            print(f'{cmd:>{width}} {first}')


def safe(cmd, target):
    def wrapper(arg):
        try:
            cmd(target, arg)
        except Exception as x:
            print(type(x).__name__, x)
    return wrapper


def prompt(target):
    user = target.login.name
    return f'{user}@{target.name} > '


class Repl(Cmd):
    def __init__(self, target):
        self.prompt = prompt(target)
        for name, cmd in commands.items():
            setattr(self, f'do_{name}', safe(cmd, target))
        self.modules = target.modules.items.keys()
        super().__init__()

    def do_help(self, cmd):
        help(cmd)

    def do_logs(self, level=None):
        log = logger.logs(level or 'info')
        print(open(log).read())

    def preloop(self):
        print(banner)
        self.onecmd('infos')
        print()

    def default(self, line):
        module = line.split()[0]
        if module in self.modules:
            self.onecmd(f'deploy {line}')
        else:
            self.onecmd(f'run {line}')

    def do_EOF(self, arg):
        return True


def repl(target):
    Repl(target).cmdloop()

# Author: Lusqueta
# Discord: Lusqueta#0001

import hacks
import logging

from SDK.entity import Entity
from SDK.process import Process
from SDK.utils.time import sleep

from threading import Thread
from keyboard import is_pressed
from update_offsets import update_offsets

from rich import pretty, traceback
from rich.logging import RichHandler
from rich.console import Console

def bootstrap():
    pretty.install()
    traceback.install()
    format_ = '%(message)s.'
    logging.basicConfig(format=format_, level='INFO', handlers=[RichHandler()])

def wrapper(func, handler: Process, ms):
    try:
        while sleep(ms):
            if handler.window_active(): func(handler)
    except Exception as e:
        Console().print_exception()

def main():
    
    logging.info('Updating offsets')
    if not update_offsets():
        return logging.error('Failed to update offsets. Exiting.')
    logging.info('Offsets updated sucessfully!')

    handler = Process('csgo.exe')
    def load_module(fun, ms): return lambda: wrapper(fun, handler, ms)
    Entity.handler = handler

    modules = [
        load_module(hacks.glow.main, 1),
        load_module(hacks.bhop.main, 1),
        load_module(hacks.trigger.main, 1),
        load_module(hacks.radarhack.main, 1000),
        load_module(hacks.aimbot.main, 1),
        load_module(hacks.rcs.main, 10),
    ]

    for module in modules:
        Thread(target=module, daemon=True).start()

    while not is_pressed("insert"):
        sleep(10)

    exit(0)


if __name__ == "__main__":
    try:
        bootstrap()
        main()
    except KeyboardInterrupt:
        exit(0)
    except Exception as e:
        print(e)

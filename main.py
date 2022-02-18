# Author: Lusqueta
# Discord: Lusqueta#0001

from keyboard import is_pressed

from SDK.entity import Entity
from SDK.module import start_modules
from SDK.process import Process
from SDK.utils.time import sleep

from bootstrap import bootstrap


def main():
    handler = Process('csgo.exe')
    Entity.handler = handler
    start_modules(handler)
    while not is_pressed("insert"): sleep(10)

if __name__ == "__main__":
    try:
        bootstrap()
        main()
    except KeyboardInterrupt:
        exit(0)

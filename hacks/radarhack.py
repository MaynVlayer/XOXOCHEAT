from SDK.entity import Entity
from SDK.process import Process


def main(csgo: Process):
    for entity in Entity.get_valid():
        entity.spotted = True

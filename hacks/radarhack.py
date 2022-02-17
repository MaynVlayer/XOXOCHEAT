from SDK.entity import Entity
from SDK.module import register_module
from SDK.process import Process


@register_module('radar')
def main(csgo: Process):
    for entity in Entity.get_valid():
       entity.spotted = True
from keyboard import is_pressed

from SDK.entity import Player
from SDK.module import ModuleConfig, ModuleEntry, register_module
from SDK.process import Process
from SDK.utils import get_mouse


config = ModuleConfig(
    1,
    key = 'shift'
)

@register_module('trigger', config)
def main(csgo: Process):
    player = Player()
    entity = player.in_crosshair
    if entity.is_valid and entity.team != player.team:
        if config.key and is_pressed(config.key) or not config.key:
            player.start_shooting()
    elif not get_mouse(1):
        player.stop_shooting()

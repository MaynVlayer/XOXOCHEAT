from keyboard import is_pressed

from SDK.entity import Player
from SDK.module import register_module
from SDK.process import Process


@register_module('bhop')
def main(csgo: Process):
    player = Player()
    if is_pressed('space') and player.in_ground:
        player.jump()
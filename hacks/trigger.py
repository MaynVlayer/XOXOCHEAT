from keyboard import is_pressed

from SDK.entity import Player
from SDK.process import Process
from SDK.utils import get_mouse


class Config:
    key = 'shift'

def main(csgo: Process):
    player = Player()
    entity = player.in_crosshair
    if entity.is_valid and entity.team != player.team:
        if Config.key and is_pressed(Config.key) or not Config.key:
            player.start_shooting()
    elif not get_mouse(1):
        player.stop_shooting()

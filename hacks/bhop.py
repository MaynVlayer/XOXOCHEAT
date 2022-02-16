from keyboard import is_pressed

from SDK.entity import Player
from SDK.process import Process


def main(csgo: Process):
    player = Player()
    if is_pressed('space') and player.in_ground:
        player.jump()

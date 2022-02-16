from vectormath import Vector3

from offsets import *

from SDK.entity import Player
from SDK.process import Process


class Config:
    force = 2

class Store:
    old_punch = Vector3()

def main(csgo: Process):
    player = Player()
    punch = player.punch
    angle = player.aim
    if player.shots_fired > 1:
        correct_punch = punch - Store.old_punch
        correct_angle = Vector3(
            angle.x - correct_punch.x * Config.force,
            angle.y - correct_punch.y * Config.force,
            0.0
        )
        player.aim = correct_angle
    Store.old_punch = punch

from vectormath import Vector3

from offsets import *

from SDK.entity import Player
from SDK.module import ModuleConfig, ModuleStore, register_module
from SDK.process import Process

        
config = ModuleConfig(
    1,
    force = 2,
)

store = ModuleStore(
    old_punch = Vector3(),
)

@register_module('rcs', config, store)
def main(csgo: Process):
    player = Player()
    punch = player.punch
    angle = player.aim
    if player.shots_fired > 1:
        correct_punch = punch - store.old_punch
        correct_angle = Vector3(
            angle.x - correct_punch.x * config.force,
            angle.y - correct_punch.y * config.force,
            0.0
        )
        player.aim = correct_angle
    store.old_punch = punch

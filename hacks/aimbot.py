from math import inf
from offsets import *

from SDK.entity import Player, Entity
from SDK.math import calc_angle
from SDK.enums import Bones
from SDK.process import Process
from SDK.utils import get_mouse
from SDK.module import ModuleConfig, register_module


def get_closest_enemy(player: Player, bone: int, max_distance: float = inf):
    angles = None
    closest_dist = inf

    for entity in Entity.get_valid():
        if player.has_spotted(entity) and entity.team != player.team:
            enemy_pos = entity.get_bone_pos(bone)
            player_pos = player.pos
            desired = calc_angle(player_pos, enemy_pos)
            current_aim = player.aim
            dist = (current_aim - desired) * -1

            if dist.length < closest_dist and dist.length <= max_distance:
                closest_dist = dist.length
                angles = dist

    return angles


config = ModuleConfig(
    1, 
    bone = Bones.head, 
    smoothing = 0.7,
)


@register_module('aimbot', config)
def main(csgo: Process):
    player = Player()

    if get_mouse(1):
        aim_distance = get_closest_enemy(player, config.bone, 2.0)

        if aim_distance is None:
            return

        correct_aim = player.aim + aim_distance * config.smoothing

        player.aim = correct_aim - player.punch * 2
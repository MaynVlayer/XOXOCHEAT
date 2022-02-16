from math import inf
from offsets import *

from SDK.entity import Player, Entity
from SDK.math import calc_angle
from SDK.enums import Bones
from SDK.process import Process
from SDK.utils import get_mouse


class Config:
    bone = Bones.head
    smoothing = 0.7


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

def main(csgo: Process):
    player = Player()

    if get_mouse(1):
        aim_distance = get_closest_enemy(player, Config.bone, 2.0)

        if aim_distance is None:
            return

        correct_aim = player.aim + aim_distance * Config.smoothing

        player.aim = correct_aim - player.punch * 2

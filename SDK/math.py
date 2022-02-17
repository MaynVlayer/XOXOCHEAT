
from vectormath import Vector3
from numpy import fmod, pi, sqrt, arctan, min, max, abs

from SDK.entity import Entity, Player

def clamp(value, min_v, max_v):
    return min([max([value, min_v]), max_v])

def fix_angle(angle: Vector3):

    # Normalize yaw to -180, 180
    angle.y = fmod(angle.y, 360)
    if angle.y > 180:
        angle.y -= 360
    elif angle.y < -180:
        angle.y += 360

    # Clamp pitch to -89, 89
    angle.x = clamp(angle.x, -89, 89)

    # Roll = 0
    # This is due some bug, need investigation
    angle.z = 0.0

    return angle


def distance(player: Player, enemy: Entity):
    diff = Vector3(0.0, 0.0, 0.0)
    diff.x = enemy.x - player.x
    diff.y = enemy.y - player.y
    diff.z = enemy.z - player.z

    distance = sqrt(
        diff.x ** 2 +
        diff.y ** 2 +
        diff.z ** 2
    )

    return abs(distance)


def calc_angle(player_pos: Vector3, entity_pos: Vector3):
    delta = player_pos - entity_pos
    angle = Vector3()

    hyp = sqrt(delta.x ** 2 + delta.y ** 2 + angle.z ** 2)
    angle.x = arctan(delta.z / hyp) * 180 / pi  # |
    angle.y = arctan(delta.y / delta.x) * 180 / pi  # -

    if delta.x >= 0.0:
        angle.y += 180.0

    angle = fix_angle(angle)

    return angle

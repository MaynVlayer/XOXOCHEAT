import vectormath
from ctypes import *

from offsets import *

from SDK.process.Structures import Vector3
from SDK.entity import Entity


class Player(Entity):

    def jump(self):
        self._write_client(dwForceJump, 0x6, c_int)

    def shoot(self):
        self._write_client(dwForceAttack, 0x6, c_int)

    def start_shooting(self):
        self._write_client(dwForceAttack, 0x5, c_int)

    def stop_shooting(self):
        self._write_client(dwForceAttack, 0x4, c_int)

    @property
    def pos(self):
        vec_origin = self.read(m_vecOrigin, Vector3)
        vec_view_offset = self.read(m_vecViewOffset, Vector3)

        sum = vectormath.Vector3(
            vec_origin.x + vec_view_offset.x,
            vec_origin.y + vec_view_offset.y,
            vec_origin.z + vec_view_offset.z
        )

        return sum

    @property
    def in_crosshair(self):
        return Entity(self.read(m_iCrosshairId, c_int))

    @property
    def is_valid(self):
        return self.base > 0 and self.health > 0 and not self.dormant

    def __init__(self):
        client_state = self._read_engine(dwClientState, c_int)
        self.index = Entity.handler.read(
            client_state + dwClientState_GetLocalPlayer, c_int) + 1

        Entity.__init__(self, self.index)

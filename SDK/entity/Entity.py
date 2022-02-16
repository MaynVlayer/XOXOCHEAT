from ctypes import *
import vectormath

from offsets import *

from SDK.process import Process, Vector3, BoneMatrix


class Entity:

    handler: Process = None

    def _read_client(self, address, c_type):
        return Entity.handler.read(Entity.handler.modules['client.dll'] + address, c_type)

    def _write_client(self, address, data, c_type):
        return Entity.handler.write(Entity.handler.modules['client.dll'] + address, data, c_type)

    def _read_engine(self, address, c_type):
        return Entity.handler.read(Entity.handler.modules['engine.dll'] + address, c_type)

    def _write_engine(self, address, data, c_type):
        return Entity.handler.write(Entity.handler.modules['engine.dll'] + address, data, c_type)

    def _get_base(self, index):
        return self._read_client(dwEntityList + ((index - 1) * 0x10), c_int)

    def read(self, address, c_type):
        return Entity.handler.read(self.base + address, c_type)

    def write(self, address, data, c_type):
        return Entity.handler.write(self.base + address, data, c_type)

    def get_bone_pos(self, bone_id: int):
        pointer_bone_matrix = self.read(m_dwBoneMatrix, c_int)
        bone_pos = Entity.handler.read(
            pointer_bone_matrix + 0x30 * bone_id + 0x0C, BoneMatrix)
        return vectormath.Vector3(bone_pos.x, bone_pos.y, bone_pos.z)

    def has_spotted(self, entity):
        mask = entity.spotted_by_mask
        return (mask & (1 << (self.index - 1)))

    @staticmethod
    def get_valid():
        entities = {Entity(i) for i in range(1, 33)}
        for e in entities:
            if e.is_valid:
                yield e

    @property
    def shots_fired(self):
        return self.read(m_iShotsFired, c_int)

    @property
    def punch(self):
        vec_ = self.read(m_aimPunchAngle, Vector3)
        return vectormath.Vector3(vec_.x, vec_.y, vec_.z)

    @punch.setter
    def punch(self, v: vectormath.Vector3):
        v = Vector3(*v)
        self.write(m_aimPunchAngle, v, Vector3)

    @property
    def aim(self):
        pointer_client_state = self._read_engine(dwClientState, c_int)
        vec_ = Entity.handler.read(
            pointer_client_state + dwClientState_ViewAngles, Vector3)
        return vectormath.Vector3(vec_.x, vec_.y, vec_.z)

    @aim.setter
    def aim(self, vec_value: vectormath.Vector3):
        pointer_client_state = self._read_engine(dwClientState, c_int)
        vec_value = Vector3(*vec_value)
        Entity.handler.write(pointer_client_state +
                             dwClientState_ViewAngles, vec_value, Vector3)

    @property
    def view_offset(self):
        pointer_vec_origin = self.read(m_vecOrigin, c_int)
        vec_ = Entity.handler.read(
            pointer_vec_origin + m_vecViewOffset, Vector3)
        return vectormath.Vector3(vec_.x, vec_.y, vec_.z)

    @property
    def health(self):
        return self.read(m_iHealth, c_int)

    @property
    def flag(self):
        return self.read(m_fFlags, c_int)

    @property
    def team(self):
        return self.read(m_iTeamNum, c_int)

    @property
    def dormant(self):
        return self.read(m_bDormant, c_int) == 1

    @property
    def spotted(self):
        return self.read(m_bSpotted, c_int) > 0

    @spotted.setter
    def spotted(self, value):
        if type(value) is bool:
            value = 1 if value else 0
        return self.write(m_bSpotted, value, c_int)

    @property
    def spotted_by_mask(self):
        return self.read(m_bSpottedByMask, c_long)

    # Flags
    #
    #	256 - Air           | 0001 0000 0000
    #	257 - Floor         | 0001 0000 0001
    #	261 - Mid Crouch    | 0001 0000 0101
    #	262 - Air Crouched  | 0001 0000 0110
    #	263 - Crouched      | 0001 0000 0111
    @property
    def in_ground(self):
        return self.flag & 1 == 1

    @property
    def is_valid(self):
        return self.base > 0 and self.health > 0 and not self.dormant

    @property
    def pos(self):
        _pos = self.read(m_vecOrigin, Vector3)
        return vectormath.Vector3(_pos.x, _pos.y, _pos.z)

    @property
    def speed(self):
        _speed = self.read(m_vecVelocity, Vector3)
        return vectormath.Vector3(_speed.x, _speed.y, _speed.z)

    def __init__(self, index):
        self.index: int = index
        self.base: int = self._get_base(index)

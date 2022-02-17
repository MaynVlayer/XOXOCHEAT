from ctypes import *

from offsets import *

from SDK.entity import Entity, Player
from SDK.module import register_module
from SDK.process import Process, GlowObject


@register_module('glow')
def main(csgo: Process):
    client: int = csgo.modules["client.dll"]
    player = Player()
    glow_base: c_int = csgo.read(client + dwGlowObjectManager, c_int)

    for entity in Entity.get_valid():
        if entity.team != player.team:
            e_health = entity.health / 100
            index = csgo.read(entity.base + m_iGlowIndex, c_int)
            address = glow_base + (index * 0x38)
            g_object: GlowObject = csgo.read(address, GlowObject)
            g_object.r = 1.0 - e_health
            g_object.g = e_health
            g_object.b = 0.0
            g_object.a = 0.65
            g_object.renderWhenOccluded = False
            g_object.renderWhenUnoccluded = True
            g_object.fullBloom = False
            csgo.write(address, g_object, GlowObject)
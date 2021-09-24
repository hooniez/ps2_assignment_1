from Village import Village

from mcpi.minecraft import Minecraft

mc = Minecraft.create()

pos = mc.player.getTilePos()

mc.player.setPos(pos.x + 500, 100, pos.z + 500)

if __name__ == '__main__':
    mc = Minecraft.create()
    pos = mc.player.getTilePos()
    mc.player.setPos(pos.x + 1000, 100, pos.z + 1000)
    village = Village(mc)
    village.foundation_generator(mc)
    village.road_generator(mc, 'row')
    village.road_generator(mc, 'column')
    village.spawn_houses(mc)


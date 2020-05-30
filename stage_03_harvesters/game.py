# -*- coding: utf-8 -*-

# pip install -r requirements.txt

from astrobox.space_field import SpaceField
from stage_03_harvesters.reaper import ReaperDrone
from stage_03_harvesters.driller import DrillerDrone
from kochetov import KochetovDrone
from vader import VaderDrone

NUMBER_OF_DRONES = 5


class KochetovDrone2(KochetovDrone):
    pass


if __name__ == '__main__':
    scene = SpaceField(
        speed=5,
        asteroids_count=20,
    )
    my_team = [KochetovDrone() for _ in range(NUMBER_OF_DRONES)]
    team_3 = [DrillerDrone() for _ in range(NUMBER_OF_DRONES)]
    team_2 = [ReaperDrone() for _ in range(NUMBER_OF_DRONES)]
    team_1 = [KochetovDrone2() for _ in range(NUMBER_OF_DRONES)]
    scene.go()

# зачёт!

# -*- coding: utf-8 -*-

# pip install -r requirements.txt

from astrobox.space_field import SpaceField
from stage_03_harvesters.driller import DrillerDrone
from stage_03_harvesters.reaper import ReaperDrone
from stage_04_soldiers.devastator import DevastatorDrone
from kochetov import KochetovDrone
from vader import VaderDrone

NUMBER_OF_DRONES = 5

if __name__ == '__main__':
    scene = SpaceField(
        field=(1200, 900),
        speed=10,
        asteroids_count=17,
        can_fight=True,
    )
    # team_2 = [ReaperDrone() for _ in range(NUMBER_OF_DRONES)]
    my_team = [KochetovDrone() for _ in range(NUMBER_OF_DRONES)]
    team_4 = [DevastatorDrone() for _ in range(NUMBER_OF_DRONES)]
    # team_3 = [DrillerDrone() for _ in range(NUMBER_OF_DRONES)]

    scene.go()

# Зачёт!

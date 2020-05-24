# -*- coding: utf-8 -*-

# pip install -r requirements.txt

from astrobox.space_field import SpaceField
from vader import VaderDrone
from kochetov import KochetovDrone

if __name__ == '__main__':
    scene = SpaceField(
        speed=3,
        asteroids_count=5,
    )
    # d = [VaderDrone() for _ in range(5)]
    k = [KochetovDrone() for _ in range(5)]
    scene.go()


# Первый этап: зачёт!

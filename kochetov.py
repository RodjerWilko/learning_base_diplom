from astrobox.core import Drone
from robogame_engine.geometry import Point

index = 0


class KochetovDrone(Drone):
    asteroid_list = []
    my_drones_list = []
    center = ''

    def __init__(self, **kwargs):
        global index
        self.distance = 0
        self.empty_distance = 0
        self.part_load_distance = 0
        self.full_load_distance = 0
        index += 1
        self.index = index
        self.type = ''
        super().__init__(**kwargs)

    def on_born(self):
        global index
        self.asteroid_list = self.get_sorted_asteroid_list()
        self.my_drones_list.append(self)
        x = (self.asteroid_list[0][1].coord.x + self.my_mothership.coord.x) / 2
        y = (self.asteroid_list[0][1].coord.y + self.my_mothership.coord.y) / 2
        self.center = Point(x, y)
        if self.index == 1:
            self.type = 'transport'
            self.target = self.center
        else:
            self.target = self.get_my_asteroid()
        self.stat(self.target)
        self.move_at(self.target)

    def get_sorted_asteroid_list(self):
        """"получаем список астероидов, отсортированных по расстояния от базы"""
        a_list = []
        for a in self.asteroids:
            dist = a.distance_to(self.my_mothership)
            a_list.append([dist, a, 0])
            a_list.sort(reverse=True)
        return a_list

    def get_my_asteroid(self):
        for i, asteroid in enumerate(self.asteroid_list[::-1]):
            if asteroid[1].payload == 0:
                continue
            elif i % 2 == 0 and self.index % 2 == 0:
                return asteroid[1]
            elif i % 2 == 0 and self.index % 2 != 0:
                continue
            elif i % 2 == 1 and self.index % 2 == 1:
                return asteroid[1]
            else:
                continue

    def print_stat(self):
        print(f'№: {self.index}, '
              f'Вся дистанция: {int(self.distance)}, '
              f'дальность полета не загруженными:'
              f' {int((self.empty_distance / self.distance) * 100)} %, '
              f'дальность полета загруженными полностью: '
              f'{int((self.full_load_distance / self.distance) * 100)} %, '
              f'дальность  полета загруженными не полностью: '
              f'{int((self.part_load_distance / self.distance) * 100)} % ')

    def on_stop_at_point(self, target):
        if self.near(self.my_drones_list[0]):
            self.unload_to(self.my_drones_list[0])
        else:
            self.stat(self.my_mothership)
            self.move_at(self.my_mothership)

    def on_stop_at_asteroid(self, asteroid):
        if asteroid.is_empty:
            self.on_wake_up()
        else:
            self.load_from(asteroid)

    def on_load_complete(self):
        if self.is_full:
            if self.index == 4:
                if self.distance_to(self.my_mothership) > self.distance_to(self.center):
                    if self.my_drones_list[0].near(self.center):
                        self.target = self.center
                        self.stat(self.target)
                        self.move_at(self.target)
                    else:
                        self.stat(self.my_mothership)
                        self.move_at(self.my_mothership)
                else:
                    self.stat(self.my_mothership)
                    self.move_at(self.my_mothership)
            else:
                self.stat(self.my_mothership)
                self.move_at(self.my_mothership)
        else:
            self.on_wake_up()

    def on_stop_at_mothership(self, mothership):
        if self.type == 'transport':
            if self.payload == 0:
                self.print_stat()
        self.unload_to(mothership)

    def on_unload_complete(self):
        if self.type == 'transport':  # если дрон транспорт
            if not all(asteroid.is_empty for asteroid in self.asteroids):  # если не все астероиды пустые
                for asteroid in self.asteroid_list:
                    if not asteroid[1].is_empty:
                        if self.distance_to(asteroid[1]) > self.distance_to(self.center):
                            self.target = self.center
                            self.stat(self.center)
                            self.move_at(self.target)
                            break
                        else:
                            self.target = asteroid[1]
                            self.stat(asteroid[1])
                            self.move_at(self.target)
                            break
                    else:
                        continue
            else:
                self.print_stat()
        else:
            if self.payload == 0:
                self.on_wake_up()
            else:
                if self.target == self.center:
                    self.on_wake_up()
                elif self.target.is_empty:
                    self.on_wake_up()
                else:
                    self.stat(self.target)
                    self.move_at(self.target)

    def stat(self, target):
        distance = self.distance_to(target)
        self.distance += distance
        if self.is_empty:
            self.empty_distance += distance
        elif self.is_full:
            self.full_load_distance += distance
        else:
            self.part_load_distance += distance

    def on_wake_up_transport(self):
        if self.is_full:
            self.stat(self.my_mothership)
            self.move_at(self.my_mothership)
        else:
            if all(asteroid.is_empty for asteroid in self.asteroids):
                self.stat(self.my_mothership)
                self.move_at(self.my_mothership)
            else:
                pass

    def on_wake_up(self):
        if self.type == 'transport':
            self.on_wake_up_transport()
        else:
            if self.target:
                if self.target == self.center:
                    self.target = self.get_my_asteroid()
                    if self.target:
                        self.stat(self.target)
                        self.move_at(self.target)
                    else:
                        self.print_stat()
                elif self.target.is_empty:
                    self.target = self.get_my_asteroid()
                    if self.target:
                        self.stat(self.target)
                        self.move_at(self.target)
                    else:
                        self.print_stat()
                else:
                    self.stat(self.target)
                    self.move_at(self.target)
            else:
                self.target = self.get_my_asteroid()
                if self.target:
                    self.stat(self.target)
                    self.move_at(self.target)
                else:
                    self.stat(self.my_mothership)
                    self.move_at(self.my_mothership)

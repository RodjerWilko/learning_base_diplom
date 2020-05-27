from astrobox.core import Drone

index = 0


class KochetovDrone(Drone):
    asteroid_list = []
    my_drones_list = []
    asteroid_pick_list = []

    def __init__(self, **kwargs):
        global index
        index += 1
        self.index = index
        super().__init__(**kwargs)

    def on_born(self):

        self.asteroid_list = self.get_sorted_asteroid_list()
        self.my_drones_list.append(self)
        self.target = self.get_my_asteroid()
        self.move_at(self.target)

    def get_sorted_asteroid_list(self):
        """"получаем список астероидов, отсортированных по расстояния от базы"""
        a_list = []
        for a in self.asteroids:
            dist = a.distance_to(self.my_mothership)
            a_list.append([dist, a])
            a_list.sort(reverse=False)
        return a_list

    def get_my_asteroid(self):
        for i, asteroid in enumerate(self.asteroid_list):
            if asteroid[1].is_empty:
                continue
            elif asteroid[1] not in self.asteroid_pick_list:
                if asteroid[1].payload > 35:  # 35
                    self.asteroid_pick_list.append(asteroid[1])
                    return asteroid[1]
                else:
                    continue
            elif i == len(self.asteroid_list) - 1:
                ast = self.get_any_asteroid()
                return ast

    def get_any_asteroid(self):
        for asteroid in self.asteroid_list:
            if asteroid[1].is_empty:
                continue
            else:
                return asteroid[1]

    def on_stop_at_asteroid(self, asteroid):
        self.turn_to(self.my_mothership)
        if asteroid.is_empty:
            self.on_wake_up()
        else:
            self.load_from(asteroid)

    def on_load_complete(self):
        if self.is_full:
            self.move_at(self.my_mothership)
        else:
            if self.fullness > 0.7:
                self.move_at(self.my_mothership)
            else:
                self.on_wake_up()

    def on_stop_at_mothership(self, mothership):
        if self.target:
            self.turn_to(self.target)
            self.unload_to(mothership)
        else:
            self.unload_to(mothership)

    def on_unload_complete(self):
        self.on_wake_up()

    def on_wake_up(self):
        if self.target:
            if self.target.is_empty:
                self.target = self.get_my_asteroid()
                if self.target:
                    self.move_at(self.target)
                else:
                    self.move_at(self.my_mothership)
            else:
                if self.target.payload < 15:  # 15
                    self.target = self.get_my_asteroid()
                    if self.target:
                        self.move_at(self.target)
                    else:
                        self.move_at(self.my_mothership)
                else:
                    self.move_at(self.target)
        else:
            pass

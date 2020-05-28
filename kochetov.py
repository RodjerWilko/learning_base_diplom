from astrobox.core import Drone


class KochetovDrone(Drone):
    asteroid_list = []
    lil_asteroid_list = []
    my_drones_list = []
    asteroid_pick_list = []
    index = 0

    def __init__(self, **kwargs):
        self.index += 1
        self.index = self.index
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
                if asteroid[1].payload > 40:  # 35
                    self.asteroid_pick_list.append(asteroid[1])
                    return asteroid[1]
                else:
                    continue
            else:
                pass

    def get_any_asteroid(self):
        for asteroid in self.asteroid_list:
            if asteroid[1].is_empty:
                continue
            elif asteroid[1] not in self.lil_asteroid_list:
                self.lil_asteroid_list.append(asteroid[1])
                return asteroid[1]
            else:
                pass

    def on_stop_at_asteroid(self, asteroid):
        self.turn_to(self.my_mothership)
        if asteroid.is_empty:
            self.get_target()
        else:
            self.load_from(asteroid)

    def on_load_complete(self):
        if self.is_full:
            self.move_at(self.my_mothership)
        else:
            if self.fullness > 0.7:
                self.move_at(self.my_mothership)
            else:
                self.get_target()

    def on_stop_at_mothership(self, mothership):
        if self.target:
            self.turn_to(self.target)
            self.unload_to(mothership)
        else:
            self.unload_to(mothership)

    def on_unload_complete(self):
        self.get_target()

    def get_target(self):
        if self.target:
            if self.target.is_empty:
                self.target = self.get_my_asteroid()
                if self.target:
                    self.move_at(self.target)
                else:
                    self.target = self.get_any_asteroid()
                    if self.target:
                        self.move_at(self.target)
                    else:
                        self.move_at(self.my_mothership)
            else:
                if self.target.payload < 40:  # 15
                    self.target = self.get_my_asteroid()
                    if self.target:
                        self.move_at(self.target)
                    else:
                        self.target = self.get_any_asteroid()
                        if self.target:
                            self.move_at(self.target)
                        else:
                            self.move_at(self.my_mothership)
                else:
                    self.move_at(self.target)
        else:
            pass

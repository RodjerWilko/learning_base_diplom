from astrobox.core import Drone


class KochetovDrone(Drone):
    asteroid_dict = []

    def on_born(self):
        self.target = self._get_my_asteroid()
        self.move_at(self.target)
        self.asteroid_dict = self.get_list()

    def get_list(self):  # получаем список астероидов, отсортированных по расстояния от базы
        a_dict = []
        for asteroid in self.asteroids:
            distance = asteroid.distance_to(self.my_mothership)
            a_dict.append([distance, asteroid])
            a_dict.sort(reverse=True)
        return a_dict

    def _get_my_asteroid(self):
        for asteroid in self.asteroid_dict:
            if asteroid[1].payload == 0:
                continue
            else:
                return asteroid[1]

    def on_stop_at_asteroid(self, asteroid):
        self.load_from(asteroid)

    def on_load_complete(self):
        if self.is_full:
            self.move_at(self.my_mothership)
        else:
            self.on_wake_up()

    def on_stop_at_mothership(self, mothership):
        self.unload_to(mothership)

    def on_unload_complete(self):
        if self.target:
            if self.target.payload == 0:
                self.target = self._get_my_asteroid()
            self.move_at(self.target)

    def on_wake_up(self):
        self.target = self._get_my_asteroid()
        if self.target:
            self.move_at(self.target)
        else:
            self.move_at(self.my_mothership)

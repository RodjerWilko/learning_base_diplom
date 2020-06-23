import math

from astrobox.core import Drone
from robogame_engine.geometry import Point
from robogame_engine.theme import theme

DICT_CORNERS = {
    'llc': [(195, -40), (193, 50), (147, 135), (50, 120), (-45, 155)],
    'ulc': [(195, 40), (193, -50), (147, -135), (50, -120), (-45, -155)],
    'urc': [(-195, 40), (-193, -50), (-147, -135), (-50, -120), (45, -155)],
    'lrc': [(-195, -40), (-193, 50), (-147, 135), (-50, 120), (45, 155)]
}


class KochetovDrone(Drone):
    """
    Роли дронов:
    - 'defender' : защитник базы
    - 'base_killer' : убийца чужжой базы
    - 'harvester' : сборщик элириума
    - 'harvester_first' : первый сборщик

    """
    asteroid_list = []  # Список астероидов
    my_drones_list = []  # Список моих дронов
    asteroid_pick_list = []  # Список уже взятых астероидов
    enemies_list = []  # Список врагов дронов
    enemies_motherships_list = []  # Список вражеских баз
    die_enemies_motherships_list = []  # Список мертвых вражеских баз
    amount_team = 0  # Количество команд в игре
    enemy = None  # Цель
    index = 0  # Порядковый номер дрона
    step = 0  # Шаг
    type = ''  # Тип дрона
    my_mothership_corner = ''  # Угол в котором появилась база

    def on_born(self):

        self.my_mothership_corner = self.check_my_mothership_corner()
        self.asteroid_list = self.get_sorted_asteroid_list()
        self.my_drones_list.append(self)
        self.index = self.my_drones_list.index(self)
        self.enemies_motherships_list = self.get_enemies_motherships()
        self.amount_team = len(self.scene.motherships)
        x = self.my_mothership.coord.x + DICT_CORNERS[self.my_mothership_corner][self.index][0]
        y = self.my_mothership.coord.y + DICT_CORNERS[self.my_mothership_corner][self.index][1]
        self.target = Point(x, y)
        self.step = 1
        self.move_at(self.target)

        if self.amount_team == 2:
            self.on_born_2_team()
        else:
            self.on_born_more_2_team()

    def on_born_2_team(self):
        """Распределение ролей при 2-х командах в игре"""
        if self.index == 0 or self.index == 1 or self.index == 2:
            self.type = 'defender'
        else:
            self.type = 'harvester'

    def on_born_more_2_team(self):
        """Распределение ролей при больше чем 2-х командах в игре"""
        if self.index == 2 or self.index == 3 or self.index == 4:
            self.type = 'base_killer'
            self.enemy = self.get_enemies_motherships()[0][0]
            self.target = self.get_enemies_motherships()[0][0]
        else:
            self.type = 'defender'

    def check_my_mothership_corner(self):
        """узнаем в каком углу наша база"""
        if self.my_mothership.coord.x < theme.FIELD_WIDTH//2 and self.my_mothership.coord.y < theme.FIELD_HEIGHT // 2:
            return 'llc'  # 'lower_left_corner'
        elif self.my_mothership.coord.x < theme.FIELD_WIDTH//2 and self.my_mothership.coord.y > theme.FIELD_HEIGHT // 2:
            return 'ulc'  # 'upper_left_corner'
        elif self.my_mothership.coord.x > theme.FIELD_WIDTH//2 and self.my_mothership.coord.y > theme.FIELD_HEIGHT // 2:
            return 'urc'  # 'upper_right_corner'
        else:
            return 'lrc'  # 'lower_right_corner'

    def get_enemies_list(self):
        """Получаем спиок живых вражеских дронов"""
        enemies = [(enemy_drone, self.distance_to(enemy_drone)) for enemy_drone in self.scene.drones if
                   self.team != enemy_drone.team and enemy_drone.is_alive]
        enemies.sort(key=lambda x: x[1])
        return enemies

    def get_die_enemies_list(self):
        """Получение списка мертвых но не пустых вражских дронов"""
        enemies = [(enemy_drone, self.distance_to(enemy_drone)) for enemy_drone in self.scene.drones if
                   self.team != enemy_drone.team and not enemy_drone.is_empty and not enemy_drone.is_alive]
        enemies.sort(key=lambda x: x[1])
        return enemies

    def get_enemies_motherships(self):
        """Получение списка вражеских баз"""
        enemies_mships = [(m, self.distance_to(m)) for m in self.scene.motherships
                          if self.mothership != m]
        enemies_mships.sort(key=lambda x: x[1])
        return enemies_mships

    def get_die_enemies_motherships_list(self):
        """Получение списка мертвых вражеских баз"""
        enemies_mships = [(m, self.distance_to(m)) for m in self.scene.motherships
                          if self.mothership != m and not m.is_empty and not m.is_alive]
        enemies_mships.sort(key=lambda x: x[1])
        return enemies_mships

    def get_sorted_asteroid_list(self):
        """"получаем список астероидов, отсортированных по расстояния от базы"""
        a_list = []
        for a in self.asteroids:
            dist = a.distance_to(self.my_mothership)
            a_list.append([dist, a])
            a_list.sort(reverse=False)
        return a_list

    def check_drone_my_team_on_line_fire(self, enemy):
        """Проверяем есть ли на линии огня корабли нашей команды"""
        for i in range(int(self.distance_to(enemy))):
            rab = math.sqrt((int(enemy.coord.x) - int(self.coord.x)) ** 2
                            + (int(enemy.coord.y) - int(self.coord.y)) ** 2)
            k = i / rab
            c_x = int(self.coord.x) + (int(enemy.coord.x) - int(self.coord.x)) * k
            c_y = int(self.coord.y) + (int(enemy.coord.y) - int(self.coord.y)) * k
            drone_list_copy = self.my_drones_list.copy()
            drone_list_copy.remove(self)
            for drone in drone_list_copy:
                drone.radius = 50
                if drone.near(Point(c_x, c_y)) or self.my_mothership.near(Point(c_x, c_y)):
                    return True
                else:
                    continue
        return False

    def defender_action(self):
        """Логика роли 'defender' """
        self.enemies_list = self.get_enemies_list()
        self.enemies_motherships_list = self.get_enemies_motherships()
        self.die_enemies_motherships_list = self.get_die_enemies_motherships_list()

        if self.enemies_list:
            if any(enemy[1] <= 590 for enemy in self.enemies_list):
                # TODO - Для повышения читаемости кода, здесь нужно код ветки выделить в метод с красноречивым названием
                for enemy in self.enemies_list:
                    if enemy[1] > 590 or self.check_drone_my_team_on_line_fire(enemy[0]):
                        continue
                    elif self.check_drone_my_team_on_line_fire(enemy[0]):
                        continue
                    else:
                        self.enemy = enemy[0]
                        self.turn_to(self.enemy)
                        self.gun.shot(self.enemy)
                        break

            elif any(base[1] <= 590 for base in self.enemies_motherships_list):
                # TODO - Для повышения читаемости кода, здесь нужно код ветки выделить в метод с красноречивым названием
                for base in self.enemies_motherships_list:
                    if base[1] > 590 or not base[0].is_alive:
                        continue
                    if self.check_drone_my_team_on_line_fire(base[0]):
                        continue
                    else:
                        self.enemy = base[0]
                        self.turn_to(self.enemy)
                        self.gun.shot(self.enemy)
                        break
            else:
                pass  # self.move_ahead()
        else:
            self.type = 'harvester'

    def on_stop_at_asteroid(self, asteroid):
        if self.type == 'defender':
            self.defender_action()
        elif self.type == 'base_killer':
            if self.enemy.is_alive:
                self.turn_to(self.enemy)
                self.gun.shot(self.enemy)
        else:
            if isinstance(self.target, Point) or self.target.is_empty:
                self.check_new_target()
            else:
                self.turn_to(self.my_mothership)
                self.load_from(asteroid)

    def check_health(self):
        """Проверяем здоровье"""
        if self.health < theme.DRONE_MAX_SHIELD * 0.7:
            return True
        else:
            return False

    def on_load_complete(self):
        if self.type == 'harvester_first':
            if self.is_full:
                self.move_at(self.my_mothership)
            else:
                self.move_at(self.my_mothership)
        else:
            if self.is_full:
                self.move_at(self.my_mothership)
            else:
                self.check_new_target()

    def on_stop_at_mothership(self, mothership):
        if mothership != self.my_mothership:
            self.turn_to(self.my_mothership)
            self.load_from(mothership)
        else:
            # TODO - Для повышения читаемости кода, здесь нужно код ветки выделить в метод с красноречивым названием
            if self.type == 'defender' or self.type == 'base_killer':
                self.move_at(self.target)
            elif self.type == 'harvester_first':
                if self.is_empty:
                    self.harvester_first_action()
                else:
                    self.turn_to(self.target)
                    self.unload_to(mothership)
            else:
                self.turn_to(self.target)
                self.unload_to(mothership)

    def on_unload_complete(self):
        self.harvester_action()

    def harvester_action(self):
        """Логика роли 'harvester' """

        if isinstance(self.target, Point):
            self.check_new_target()
        elif self.target.is_empty:
            self.check_new_target()
        else:
            self.move_at(self.target)

    def check_new_target(self):
        """Находим новую цель для сбора элириума"""
        if any(not aster[1].is_empty for aster in self.asteroid_list):
            # TODO - Для повышения читаемости кода, здесь нужно код ветки выделить в метод с красноречивым названием
            for asteroid in self.asteroid_list:
                if asteroid[1].is_empty:
                    continue
                elif asteroid[1] in self.asteroid_pick_list:
                    continue
                else:
                    self.target = asteroid[1]
                    self.asteroid_pick_list.append(asteroid[1])
                    self.move_at(self.target)
                    break

        elif any(not die_em[0].is_empty for die_em in self.get_enemies_motherships()):
            # TODO - Для повышения читаемости кода, здесь нужно код ветки выделить в метод с красноречивым названием
            for die_em in self.get_enemies_motherships():
                if die_em[0].is_empty:
                    continue
                else:
                    self.target = die_em[0]
                    self.move_at(self.target)
                    break

        elif any(not die_e[0].is_empty for die_e in self.get_die_enemies_list()):
            # TODO - Для повышения читаемости кода, здесь нужно код ветки выделить в метод с красноречивым названием
            for die_e in self.get_die_enemies_list():
                if die_e[0].is_empty:
                    continue
                else:
                    self.target = die_e[0]
                    self.move_at(self.target)
                    break
        else:
            self.move_at(self.my_mothership)

    def base_killer_action(self):
        """Логика роли 'base_killer' """
        if self.enemy.is_alive:
            self.turn_to(self.enemy)
            self.gun.shot(self.enemy)
        else:
            if self.index == 2:
                self.type = 'defender'
            else:
                self.type = 'harvester_first'

    def harvester_first_action(self):
        """Логика роли 'harvester_first' """
        if not self.enemy.is_empty:
            self.move_at(self.target)
        else:
            self.type = 'harvester'

    def on_wake_up(self):
        if self.check_health():
            self.move_at(self.my_mothership)
        else:
            if self.type == 'defender':
                self.defender_action()

            elif self.type == 'base_killer':
                self.base_killer_action()

            elif self.type == 'harvester':
                self.harvester_action()

            elif self.type == 'harvester_first':
                self.harvester_first_action()

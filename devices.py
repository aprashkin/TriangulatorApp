import math

class Devices:
    def __init__(self, x, y):
        self.x = x  # x устройства
        self.y = y  # y устройства

    def is_clicked(self, x, y):
        # проверка на нажатие
        return math.sqrt((x - self.x)**2 + (y - self.y)**2) <= 5

    def is_inside_all_towers(self, towers):
        # проверка на нахождение внутри радиуса башен
        return all(math.sqrt((self.x - tower.x) ** 2 + (self.y - tower.y) ** 2) <= tower.r for tower in towers)
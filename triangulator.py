import math

def triangulate_func(towers, device_x, device_y):
    """
    Функция триангуляции для определения координат устройства на основе расстояний до трех башен.

    :param towers: Список объектов Tower, каждый из которых содержит координаты (x, y) и радиус (r).
    :param device_x: Координата x устройства.
    :param device_y: Координата y устройства.
    :return: Координаты устройства (x_calc, y_calc) или None, если устройство вне зоны радиуса какой-либо башни.
    """
    if len(towers) < 3:
        raise ValueError("Недостаточно башен для триангуляции. Требуется минимум три башни.")

    # Проверка, находится ли устройство в зоне радиуса каждой башни
    for tower in towers:
        distance = math.sqrt((device_x - tower.x) ** 2 + (device_y - tower.y) ** 2)
        if distance > tower.r:
            return None

    # Координаты башен
    x1, y1 = towers[0].x, towers[0].y
    x2, y2 = towers[1].x, towers[1].y
    x3, y3 = towers[2].x, towers[2].y

    # Расстояния до башен
    d1 = towers[0].r
    d2 = towers[1].r
    d3 = towers[2].r

    # Вычисление координат устройства
    A = 2 * (x2 - x1)
    B = 2 * (y2 - y1)
    C = d1**2 - d2**2 - x1**2 + x2**2 - y1**2 + y2**2
    D = 2 * (x3 - x2)
    E = 2 * (y3 - y2)
    F = d2**2 - d3**2 - x2**2 + x3**2 - y2**2 + y3**2

    x_calc = (C * E - F * B) / (E * A - B * D)
    y_calc = (C * D - A * F) / (B * D - A * E)

    return x_calc, y_calc

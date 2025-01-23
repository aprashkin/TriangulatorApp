def triangulate_func(towers):

    x1, y1, r1 = towers[0].x, towers[0].y, towers[0].r
    x2, y2, r2 = towers[1].x, towers[1].y, towers[1].r
    x3, y3, r3 = towers[2].x, towers[2].y, towers[2].r

    A = 2 * (x2 - x1)
    B = 2 * (y2 - y1)
    C = r1 ** 2 - r2 ** 2 - x1 ** 2 + x2 ** 2 - y1 ** 2 + y2 ** 2

    D = 2 * (x3 - x2)
    E = 2 * (y3 - y2)
    F = r2 ** 2 - r3 ** 2 - x2 ** 2 + x3 ** 2 - y2 ** 2 + y3 ** 2

    x = (C * E - F * B) / (E * A - B * D)
    y = (C * D - A * F) / (B * D - A * E)

    return x, y
def get_trajectory(symbol, scale=120, offset=(400, 300)):
    ox, oy = offset

    if symbol == "A":
        points = [(0, 1), (0.5, 0), (1, 1), (0.75, 0.5), (0.25, 0.5)]

    elif symbol == "B":
        points = [(0, 0), (0, 1), (0.5, 0.8), (0, 0.6), (0.5, 0.4), (0, 0)]

    elif symbol == "PEACE":
        points = [(0, 1), (0.5, 0), (1, 1)]

    elif symbol == "C":
        points = [(1, 0.2), (0.7, 0), (0.3, 0), (0, 0.5), (0.3, 1), (0.7, 1), (1, 0.8)]

    else:
        return []

    return [(ox + x * scale, oy + y * scale) for x, y in points]
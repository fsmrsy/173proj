import math


def scale_and_offset(points, scale=120, offset=(400, 300)):
    ox, oy = offset
    return [(ox + x * scale, oy + y * scale) for x, y in points]


def make_heart_points(num_points=80):
    points = []

    for i in range(num_points):
        t = 2 * math.pi * i / (num_points - 1)

        x = 16 * math.sin(t) ** 3
        y = (
            13 * math.cos(t)
            - 5 * math.cos(2 * t)
            - 2 * math.cos(3 * t)
            - math.cos(4 * t)
        )

        # normalize and flip y
        x = x / 32 + 0.5
        y = -y / 32 + 0.5

        points.append((x, y))

    return points


def make_c_points(num_points=50):
    points = []

    start = math.radians(60)
    end = math.radians(300)

    for i in range(num_points):
        t = start + (end - start) * i / (num_points - 1)
        x = 0.5 + 0.45 * math.cos(t)
        y = 0.5 + 0.45 * math.sin(t)
        points.append((x, y))

    return points


def get_trajectory(symbol, scale=120, offset=(400, 300)):
    if symbol == "A":
        points = [
            (0.0, 1.0),
            (0.5, 0.0),
            (1.0, 1.0),
            (0.75, 0.5),
            (0.25, 0.5),
        ]

    elif symbol == "B":
        points = [
            (0.0, 1.0),
            (0.0, 0.0),
            (0.45, 0.10),
            (0.60, 0.25),
            (0.45, 0.42),
            (0.0, 0.50),
            (0.50, 0.58),
            (0.65, 0.78),
            (0.45, 0.95),
            (0.0, 1.0),
        ]

    elif symbol == "C":
        points = make_c_points()

    elif symbol == "PEACE":
        points = make_heart_points()

    else:
        return []

    return scale_and_offset(points, scale=scale, offset=offset)

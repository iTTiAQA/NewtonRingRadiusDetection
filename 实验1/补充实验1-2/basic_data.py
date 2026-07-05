import math

lamda = 589.3e-6        # unit: mm
dscale = 0.2            # unit: mm


class Dot:
    def __init__(self, position, n, scale=dscale):
        self.position = position
        self.n = n
        self.scale = scale

    def get_dx(self, another_dot):
        distance = math.sqrt((self.position[0] - another_dot.position[0]) ** 2
                             + (self.position[1] - another_dot.position[1]) ** 2)
        return self.scale * self.n / distance


dot1 = Dot((257, 69), 5, 0.2)
dot2 = Dot((333, 83), 5, 0.2)

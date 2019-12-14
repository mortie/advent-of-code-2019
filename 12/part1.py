import math

class Vec3:
    def __init__(self, x = 0, y = 0, z = 0):
        self.x = x
        self.y = y
        self.z = z

    def __add__(self, other):
        return Vec3(self.x + other.x, self.y + other.y, self.z + other.z)

    def __sub__(self, other):
        return Vec3(self.x - other.x, self.y - other.y, self.z - other.z)

    def __mul__(self, num):
        return Vec3(self.x * num, self.y * num, self.z * num)

    def __div__(self, num):
        return Vec3(self.x / num, self.y / num, self.z / num)

    def __repr__(self):
        return f"({self.x},{self.y},{self.z})"

    def __eq__(self, other):
        return self.x == other.x and self.y == other.y and self.z == other.z

    def __neq__(self, other):
        return not self.__eq__(other)

    def squared_length(self):
        return self.x ** 2 + self.y ** 2 + self.z ** 2

    def length(self):
        return math.sqrt(self.squared_length())

    def tuple(self):
        return (self.x, self.y, self.z)

    def clone(self):
        return Vec3(self.x, self.y, self.z)

class Moon:
    def __init__(self, pos, vel = None):
        self.pos = pos
        self.vel = vel if vel is not None else Vec3()

    def __repr__(self):
        return f"(pos: {self.pos}, vel: {self.vel})"

    def kinetic_energy(self):
        return abs(self.vel.x) + abs(self.vel.y) + abs(self.vel.z)

    def potential_energy(self):
        return abs(self.pos.x) + abs(self.pos.y) + abs(self.pos.z)

    def total_energy(self):
        return self.kinetic_energy() * self.potential_energy()

    def gravity(self, others):
        before = self.vel.clone()
        for other in others:
            if other == self: continue

            if self.pos.x > other.pos.x: self.vel.x -= 1
            elif self.pos.x < other.pos.x: self.vel.x += 1
            if self.pos.y > other.pos.y: self.vel.y -= 1
            elif self.pos.y < other.pos.y: self.vel.y += 1
            if self.pos.z > other.pos.z: self.vel.z -= 1
            elif self.pos.z < other.pos.z: self.vel.z += 1

    def update(self):
        self.pos += self.vel

# Input
moons = [ Moon(Vec3(15, -2, -6)), Moon(Vec3(-5, -4, -11)), Moon(Vec3(0, -6, 0)), Moon(Vec3(5, 9, 6)) ]

# Example 1
#moons = [ Moon(Vec3(-1, 0, 2)), Moon(Vec3(2, -10, -7)), Moon(Vec3(4, -8, 8)), Moon(Vec3(3, 5, -1)) ]

# Example 2
#moons = [ Moon(Vec3(-8, -10, 0)), Moon(Vec3(5, 5, 10)), Moon(Vec3(2, -7, 3)), Moon(Vec3(9, -8, -3)) ]

print(moons)
for i in range(1000):
    for moon in moons:
        moon.gravity(moons)
    for moon in moons:
        moon.update()
    print(f"{i+1}: {moons}")

print("Energies after all those steps:")
for moon in moons:
    print("pot:", moon.potential_energy(), "kin:", moon.kinetic_energy(), "total:", moon.total_energy())
print("Sum total:", sum(map(lambda moon: moon.total_energy(), moons)))

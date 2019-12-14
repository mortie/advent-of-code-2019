import math
import sys

class Vec2:
    def __init__(self, x = 0, y = 0):
        self.x = x
        self.y = y

    def __add__(self, other):
        return Vec2(self.x + other.x, self.y + other.y)

    def __sub__(self, other):
        return Vec2(self.x - other.x, self.y - other.y)

    def __mul__(self, num):
        return Vec2(self.x * num, self.y * num)

    def __div__(self, num):
        return Vec2(self.x / num, self.y / num)

    def __repr__(self):
        return f"({self.x},{self.y})"

    def __eq__(self, other):
        return self.x == other.x and self.y == other.y

    def __neq__(self, other):
        return not self.__eq__(other)

    def squared_length(self):
        return self.x * self.x + self.y * self.y

    def angle(self):
        return math.atan2(self.y, self.x)

def progresser(total):
    count = 0
    while True:
        yield
        count += 1
        sys.stdout.write(f"\r{count}/{total} ")

asteroids = []
with open("input") as f:
    y = 0
    for line in f:
        x = 0
        for ch in line:
            if ch == '#':
                asteroids.append(Vec2(x, y))
            x += 1
        y += 1

def line_of_sight(origin, target):
    diff = target - origin
    angle = diff.angle()
    dist = diff.squared_length()
    for ast in asteroids:
        if ast == origin or ast == target: continue
        d = target - ast
        if d.squared_length() < dist and d.angle() == angle:
            return False
    return True

progress = progresser(len(asteroids))

def num_visible_from(origin):
    count = 0
    for ast in asteroids:
        if ast == origin: continue
        if line_of_sight(origin, ast):
            count += 1
    next(progress)
    return count

ast = max(asteroids, key=lambda ast: num_visible_from(ast))
print(ast, num_visible_from(ast))

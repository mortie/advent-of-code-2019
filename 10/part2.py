import math
import sys
#import pygame
#import time

def angleDiff(a1, a2):
    diff = a2 - a1;
    while diff < -math.pi: diff += math.tau;
    while diff > math.pi: diff -= math.tau;
    return diff

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
        return math.atan2(self.y, self.x) % math.tau

    def tuple(self):
        return self.x, self.y

def progresser(total):
    count = 0
    while True:
        count += 1
        sys.stdout.write(f"\r{count}/{total} ")
        yield

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

def num_visible_from(origin, cb = None):
    count = 0
    for ast in asteroids:
        if ast == origin: continue
        if line_of_sight(origin, ast):
            count += 1
    if cb is not None: cb()
    return count

progress = progresser(len(asteroids))
#laser = Vec2(11, 13)
laser = max(asteroids, key=lambda ast: num_visible_from(ast, lambda: next(progress)))
print("Laser position:", laser, "with", num_visible_from(laser), "visible")

def nextTarget(laser, angle):
    def minKey(ast):
        if ast == laser: return (float("inf"), float("inf"))
        diff = angleDiff(angle, (ast - laser).angle())
        if diff <= 0: return (float("inf"), float("inf"))
        return (diff, (ast - laser).squared_length())

    nearest = min(asteroids, key = minKey)
    return nearest, (nearest - laser).angle()

#pygame.init()
#screen = pygame.display.set_mode((600, 800))

laserAngle = -math.tau / 4 - 0.000001
index = 0
while len(asteroids) > 0:
    target, laserAngle = nextTarget(laser, laserAngle)
    index += 1
    if index == 200:
        print(f"The {index}th asteroid to be vaporized is {target}")
    asteroids.remove(target)

    #for evt in pygame.event.get():
    #    if evt.type == pygame.QUIT:
    #        asteroids = []
    #screen.fill((0, 0, 0))
    #for ast in asteroids:
    #    pygame.draw.circle(screen, (0, 155, 255), (ast * 15).tuple(), 3)
    #pygame.draw.circle(screen, (13, 255, 120), (laser * 15).tuple(), 5)
    #pygame.draw.line(screen, (255, 50, 30), (laser * 15).tuple(), (target * 15).tuple())
    #pygame.display.flip()
    #time.sleep(0.1)

import numpy as np

class MoonAxis:
    def __init__(self, pos, vel = None):
        self.pos = pos
        self.vel = vel if vel is not None else 0

    def gravity(self, others):
        for o in others:
            if o is self: continue
            if self.pos > o.pos: self.vel -= 1
            elif self.pos < o.pos: self.vel += 1

    def update(self):
        self.pos += self.vel

    def __repr__(self):
        return f"({self.pos}, {self.vel})"

axieses = (
    [ MoonAxis(15),  MoonAxis(-5),  MoonAxis(0),  MoonAxis(5)  ],
    [ MoonAxis(-2), MoonAxis(-4),  MoonAxis(-6), MoonAxis(9) ],
    [ MoonAxis(-6),   MoonAxis(-11), MoonAxis(0),  MoonAxis(6) ],
)

def period_length(axies):
    initial = str(axies)
    iters = 0
    while True:
        for ax in axies:
            ax.gravity(axies)
        for ax in axies:
            ax.update()
        iters += 1
        if str(axies) == initial:
            return iters

periods = [period_length(axies) for axies in axieses]
print(periods, np.lcm.reduce(periods))

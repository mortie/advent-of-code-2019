import time
import sys
import os
import atexit

def eval(intcode):
    memory = { i: intcode[i] for i in range(len(intcode)) }
    rbase = 0

    def val(mode, v):
        if mode == 0:
            return memory.get(v, 0)
        if mode == 1:
            return v
        elif mode == 2:
            return memory.get(v + rbase, 0)

    def set(mode, addr, v):
        if mode == 0 or mode == 1:
            memory[addr] = v
        elif mode == 2:
            memory[rbase + addr] = v

    iptr = 0
    while True:
        instr = [memory.get(iptr+i, 0) for i in range(4)]
        opstr = str(instr[0]).zfill(5)
        mode1 = int(opstr[2])
        mode2 = int(opstr[1])
        mode3 = int(opstr[0])
        opr = int(opstr[3:])

        if opr == 1: # ADD
            set(mode3, instr[3], val(mode1, instr[1]) + val(mode2, instr[2]))
            iptr += 4
        elif opr == 2: # MUL
            set(mode3, instr[3], val(mode1, instr[1]) * val(mode2, instr[2]))
            iptr += 4
        elif opr == 3: # INPUT
            v = yield
            set(mode1, instr[1], int(v))
            iptr += 2
        elif opr == 4: # OUTPUT
            yield val(mode1, instr[1])
            iptr += 2
        elif opr == 5: # JUMP IF TRUE
            if val(mode1, instr[1]) != 0:
                iptr = val(mode2, instr[2])
            else:
                iptr += 3
        elif opr == 6: # JUMP IF FALSE
            if val(mode1, instr[1]) == 0:
                iptr = val(mode2, instr[2])
            else:
                iptr += 3
        elif opr == 7: # LESS
            set(mode3, instr[3], 1 if val(mode1, instr[1]) < val(mode2, instr[2]) else 0)
            iptr += 4
        elif opr == 8: # EQUAL
            set(mode3, instr[3], 1 if val(mode1, instr[1]) == val(mode2, instr[2]) else 0)
            iptr += 4
        elif opr == 9: # RBASE
            rbase += val(mode1, instr[1])
            iptr += 2
        elif opr == 99: # HALT
            return
        else:
            raise Exception("Unknown op code: "+str(opr)+" (in opstr "+opstr+")")

with open("input") as f:
    intcode = list(map(lambda x: int(x), f.read().split(",")))

tiles = {
    "nothing": "\033[90m⌽",
    "wall": "\033[95m█",
    "oxygen": "\033[96mO",
    "robot_up": "\033[92m^",
    "robot_down": "\033[92mv",
    "robot_left": "\033[92m<",
    "robot_right": "\033[92m>",
}

keys = {
    "\x1b[A": "up",
    "\x1b[B": "down",
    "\x1b[D": "left",
    "\x1b[C": "right",
    "\x7f\x7f\x7f": "undo",
}

class Robot:
    def __init__(self, computer):
        self.computer = computer
        next(self.computer)
        self.direction = "up"
        self.pos = (0, 0)
        self.map = { self.pos: tiles["nothing"] }

    def dir_to_num(self, dir):
        if dir == "up": return 1
        elif dir == "down": return 2
        elif dir == "left": return 3
        else: return 4

    def rotated_right(self, dir):
        if dir == "up": return "right"
        elif dir == "down": return "left"
        elif dir == "left": return "up"
        else: return "down"

    def turned_right(self):
        return self.rotated_right(self.direction)

    def rotated_left(self, dir):
        if dir == "up": return "left"
        elif dir == "down": return "right"
        elif dir == "left": return "down"
        else: return "up"

    def turned_left(self):
        return self.rotated_left(self.direction)

    def rel_pos(self, dir):
        if dir == "up": return (self.pos[0], self.pos[1] - 1)
        elif dir == "down": return (self.pos[0], self.pos[1] + 1)
        elif dir == "left": return (self.pos[0] - 1, self.pos[1])
        else: return (self.pos[0] + 1, self.pos[1])

    def tile_at(self, pos):
        return self.map.get(pos, None)

    def move(self, dir):
        ret = self.computer.send(self.dir_to_num(dir))
        next(self.computer)
        rpos = self.rel_pos(dir)
        if ret == 0:
            self.map[rpos] = tiles["wall"]
        elif ret == 1:
            self.map[rpos] = tiles["nothing"]
            self.pos = rpos
        elif ret == 2:
            self.map[rpos] = tiles["oxygen"]
            self.pos = rpos
        return ret

    def draw(self, grid):
        hw = grid[0] // 2
        hh = grid[1] // 2
        sys.stdout.write("\033[2J")
        for pos in self.map:
            rpos = pos
            sys.stdout.write(f"\033[{hh + rpos[1] + 1};{hw + rpos[0] + 1}H{self.map[rpos]}")

        sys.stdout.write(f"\033[{hh + self.pos[1] + 1};{hw + self.pos[0] + 1}H{tiles['robot_' + self.direction]}")
        sys.stdout.write(f"\033[{grid[1] + 1};0H\033[0m")
        sys.stdout.flush()

grid = (91, 61)
rob = Robot(eval(intcode))
rob.draw(grid)

# First, we wanna get to a wall
while rob.move("right") != 0: pass
startpos = rob.pos

# Now that we're at a wall, we can use the "keep right" algorithm for solving the maze
while True:
    if rob.move(rob.direction) == 0: # wall
        rob.direction = rob.turned_left()
    else: # not a wall
        if rob.move(rob.turned_right()) != 0: # There's no wall to our right
            rob.direction = rob.turned_right()
    if rob.pos == startpos:
        break

rob.draw(grid)

# Now, let's make the monkey manually go to the oxygen tank
steps = 0
os.system("stty -icanon min 1 time 0")
rob.pos = (0, 0)
rob.direction = "up"
rob.draw(grid)
print(steps)
try:
    done = False
    while not done:
        rd = sys.stdin.read(3)
        if keys[rd] == "undo":
            steps -= 1
        else:
            ret = rob.move(keys[rd])
            if ret != 0: steps += 1
            if ret == 2: done = True
        rob.draw(grid)
        print(steps)
finally:
    os.system("stty sane")

print("That took", steps, "steps.")

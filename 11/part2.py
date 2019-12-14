import sys

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

grid = {}
grid[(0, 0)] = 1

pos = (0, 0)
dir = (0, -1)
computer = eval(intcode)

count = 0

try:
    while True:
        next(computer)
        newcolor = computer.send(grid.get(pos, 0))
        turn = next(computer)
        if turn == 0:
            if dir == (0, -1): dir = (-1, 0)
            elif dir == (-1, 0): dir = (0, 1)
            elif dir == (0, 1): dir = (1, 0)
            elif dir == (1, 0): dir = (0, -1)
        elif turn == 1:
            if dir == (0, -1): dir = (1, 0)
            elif dir == (1, 0): dir = (0, 1)
            elif dir == (0, 1): dir = (-1, 0)
            elif dir == (-1, 0): dir = (0, -1)

        if not pos in grid:
            count += 1

        newpos = (pos[0] + dir[0], pos[1] + dir[1])
        grid[pos] = newcolor
        pos = newpos
except StopIteration: pass

sys.stdout.write("\033[2J")
for key in grid:
    ch = '#' if grid[key] == 1 else ' '
    sys.stdout.write(f"\033[{key[1] + 2};{key[0] + 2}H{ch}")

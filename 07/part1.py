def eval(memory, readInput = lambda: int(input("> ")), writeOutput = print):
    def val(mode, v):
        if mode:
            return v
        else:
            return memory[v]

    iptr = 0
    while True:
        instr = memory[iptr:]
        opstr = str(instr[0]).zfill(5)
        mode1 = int(opstr[2])
        mode2 = int(opstr[1])
        mode3 = int(opstr[0])
        opr = int(opstr[3:])

        if opr == 1: # ADD
            memory[instr[3]] = val(mode1, instr[1]) + val(mode2, instr[2])
            iptr += 4
        elif opr == 2: # MUL
            memory[instr[3]] = val(mode1, instr[1]) * val(mode2, instr[2])
            iptr += 4
        elif opr == 3: # INPUT
            memory[instr[1]] = readInput()
            iptr += 2
        elif opr == 4: # OUTPUT
            writeOutput(val(mode1, instr[1]))
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
            memory[instr[3]] = 1 if val(mode1, instr[1]) < val(mode2, instr[2]) else 0
            iptr += 4
        elif opr == 8: # EQUAL
            memory[instr[3]] = 1 if val(mode1, instr[1]) == val(mode2, instr[2]) else 0
            iptr += 4
        elif opr == 99: # HALT
            return
        else:
            raise Exception("Unknown op code: "+str(opr)+" (in opstr "+opstr+")")

    return output

class ArrayReader:
    def __init__(self, arr):
        self.arr = arr
        self.i = 0
    def __call__(self):
        tmp = self.arr[self.i]
        self.i += 1
        return tmp

class ArrayWriter:
    def __init__(self, arr):
        self.arr = arr
    def __call__(self, val):
        self.arr.append(val)

def ampChain(intcode, phases):
    prevOutput = 0
    for phase in phases:
        out = []
        eval(intcode[::], ArrayReader([ phase, prevOutput ]), ArrayWriter(out))
        prevOutput = out[0]
    return prevOutput

with open("input") as f:
    intcode = list(map(lambda x: int(x), f.read().split(",")))

import itertools

biggestPerm = None
biggestOut = None
for perm in itertools.permutations([ 0, 1, 2, 3, 4 ]):
    out = ampChain(intcode, perm)
    if biggestPerm is None or out > biggestOut:
        biggestPerm = perm
        biggestOut = out
print(f"Permutation {biggestPerm} gives the biggest output {biggestOut}")

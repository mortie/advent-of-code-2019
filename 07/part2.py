def eval(memory):
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
            memory[instr[1]] = yield
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
            memory[instr[3]] = 1 if val(mode1, instr[1]) < val(mode2, instr[2]) else 0
            iptr += 4
        elif opr == 8: # EQUAL
            memory[instr[3]] = 1 if val(mode1, instr[1]) == val(mode2, instr[2]) else 0
            iptr += 4
        elif opr == 99: # HALT
            return
        else:
            raise Exception("Unknown op code: "+str(opr)+" (in opstr "+opstr+")")

def ampChain(intcode, phases):
    amps = [eval(intcode[::]) for _ in phases]
    for amp, phase in zip(amps, phases):
        next(amp)
        amp.send(phase)

    prevOutput = 0
    lastIteration = False
    while not lastIteration:
        for amp in amps:
            prevOutput = amp.send(prevOutput)
            try:
                next(amp)
            except StopIteration:
                lastIteration = True

    return prevOutput

with open("input") as f:
    intcode = list(map(lambda x: int(x), f.read().split(",")))

import itertools
import sys

biggestPerm = None
biggestOut = None
for perm in itertools.permutations([ 5, 6, 7, 8, 9 ]):
    out = ampChain(intcode, perm)
    if biggestPerm is None or out > biggestOut:
        biggestPerm = perm
        biggestOut = out
print(f"Permutation {biggestPerm} gives the biggest output {biggestOut}")

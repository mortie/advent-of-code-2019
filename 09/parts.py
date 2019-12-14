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

computer = eval(intcode)
try:
    out = next(computer)
    while True:
        if out == None:
            out = computer.send(input("> "))
        else:
            print(out)
            out = next(computer)
except StopIteration: pass

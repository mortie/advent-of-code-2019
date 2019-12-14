def eval(memory, input = lambda: int(input("> ")), output = print):
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

        if opr == 1:
            memory[instr[3]] = val(mode1, instr[1]) + val(mode2, instr[2])
            iptr += 4
        elif opr == 2:
            memory[instr[3]] = val(mode1, instr[1]) * val(mode2, instr[2])
            iptr += 4
        elif opr == 3:
            memory[instr[1]] = input()
            iptr += 2
        elif opr == 4:
            output(val(mode1, instr[1]))
            iptr += 2
        elif opr == 99:
            return
        else:
            raise Exception("Unknown op code: "+str(opr)+" (in opstr "+opstr+")")

    return output

with open("input") as f:
    intcode = list(map(lambda x: int(x), f.readline().split(",")))
eval(intcode)

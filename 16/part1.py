def patgen(num):
    n = num + 1
    return [0]*n + [1]*n + [0]*n + [-1]*n

def phase(lst):
    new = []
    pat = [0, 1, 0, -1]
    for it in range(len(lst)):
        pat = patgen(it)
        sum = 0
        for i in range(len(lst)):
            elem = lst[i]
            mul = pat[(i + 1) % len(pat)]
            sum += elem * mul
        sum = int(str(sum)[-1])
        new.append(sum)

    return new

def fft(lst, phases):
    for i in range(phases):
        lst = phase(lst)
    return lst

with open("input") as f:
    print("".join([str(x) for x in fft([int(x) for x in f.readline().strip()], 100)[:8]]))

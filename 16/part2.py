import sys

def patgen(num):
    n = num + 1
    while True:
        for i in range(n):
            yield 0
        for i in range(n):
            yield 1
        for i in range(n):
            yield 0
        for i in range(n):
            yield -1

def phase(lst, temp):
    pat = [0, 1, 0, -1]
    for it in range(len(lst)):
        pat = patgen(it)
        next(pat)
        next(pat)
        sum = 0
        for i in range(len(lst)):
            elem = lst[i]
            sum += elem * next(pat)
        sum = int(str(sum)[-1])
        temp[it] = sum
        if it % 100 == 0:
            sys.stdout.write(f"\r  {(it + 1) / len(lst)}%")
    print()

def fft(lst, phases):
    out = [0] * len(lst)
    for i in range(phases):
        print(f"{i + 1}/{phases}")
        phase(lst, out)
        t = lst
        lst = out
        out = t

    return out

with open("input") as f:
    message = [int(x) for x in f.readline().strip()] * 10000

msgoffset = int("".join([str(x) for x in message[:7]]))
print("Message offset:", msgoffset)
output = fft(message, 100)
print(output[msgoffset:msgoffset+8])

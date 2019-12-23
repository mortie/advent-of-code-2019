def pattern(n, k):
	return [0, 1, 0, -1][(n // k) % 4]

def fft_once(message, patidx):
    print("fft_once'ing message of len", len(message), "skipped", patidx)
    for i in range(len(message)):
        sum = 0
        for j in range(len(message)):
            elem = message[j]
            mul = pattern(i + patidx, j + patidx)
            sum += elem * mul

        if i % 50 == 0:
            print(f"\r{(i / len(message)) * 100:.5}%   ", end="")
        yield int(str(sum)[-1])
    print()

def fft(message, patidx, count):
    for i in range(count):
        message = list(fft_once(message, patidx))
    return message

with open("input") as f:
    message = [int(x) for x in f.readline().strip()] * 10000
startidx = int("".join([str(x) for x in message[:7]]))

fft(message[startidx:], startidx, 1)
